/** Parameterized PostgreSQL adapter for the isolated Neon card/evidence schemas.
 *
 * The host injects a database query(sql, params) function and authenticates/
 * authorizes the actor independently. Never pass a model-controlled SQL string.
 * Schema is applied only on separate Neon development branches.
 */
const KINDS = new Set(["evidence","seat_charter","tool","route_ticket",
  "communication","action","approval_reference","authority_stamp",
  "detour","lexical_context"]);

function rowsOf(result) {
  return Array.isArray(result) ? result : result?.rows || [];
}
async function one(query, sql, values) {
  return rowsOf(await query(sql, values))[0] || null;
}
export function createNeonDataAdapter(query, {dictionaryEnabled=false} = {}) {
  if (typeof query !== "function") throw new TypeError("trusted Postgres query function required");
  return {
    async getCard({card_id,revision}) {
      return one(query,
        "SELECT card_id,revision,card_kind,title,body,provenance,review_state,created_at FROM card_protocol.card_revisions WHERE card_id=$1 AND revision=$2",
        [card_id,revision]);
    },
    async resolveConfiguration({config_id,revision}) {
      const rows=rowsOf(await query(
        "SELECT m.ordinal,m.card_id,m.card_revision,c.card_kind,c.body,c.provenance,c.review_state FROM card_protocol.configuration_members m JOIN card_protocol.card_revisions c ON c.card_id=m.card_id AND c.revision=m.card_revision WHERE m.config_id=$1 AND m.config_revision=$2 ORDER BY m.ordinal",
        [config_id,revision]));
      return {config_id,revision,cards:rows,execute:false,authorization_granted:false};
    },
    async proposeCard(args,context) {
      if (!KINDS.has(args.card_kind)) throw new Error("unknown card type");
      const body = JSON.stringify(args.body);
      const provenance = JSON.stringify({
        ...args.provenance, proposed_by:String(context.authenticated_principal),
        mission_ref:String(context.mission_id),
      });
      const row=await one(query, 
        "INSERT INTO card_protocol.card_revisions (card_id,revision,card_kind,title,body,provenance,review_state) SELECT $1,$2+1,$3,$4,$5::jsonb,$6::jsonb,'proposed' WHERE (SELECT COALESCE(MAX(revision),0) FROM card_protocol.card_revisions WHERE card_id=$1)=$2 ON CONFLICT DO NOTHING RETURNING card_id,revision,card_kind,review_state",
        [args.card_id,args.expected_revision,args.card_kind,args.title,body,provenance]);
      if (!row) throw new Error("stale version, duplicate or missing permission");
      return {...row, authority_granted:false};
    },
    async getNode({node_id}) {
      return one(query,"SELECT node_id,node_kind,label,details,attribution_ref,evidence_state FROM evidence_net.nodes WHERE node_id=$1",[node_id]);
    },
    async traceEdges({node_id,max_edges=20}) {
      const edges=rowsOf(await query(
        "SELECT edge_id,source_node,target_node,relation_type,relation_domain,evidence_state,supporting_card_id,supporting_card_revision,source_ref FROM evidence_net.edges WHERE source_node=$1 OR target_node=$1 ORDER BY edge_id LIMIT $2",
        [node_id,Math.min(50,Math.max(1,max_edges))]));
      return {node_id,edges,independently_verified:false};
    },
    async proposeEdge(args,context) {
      const row=await one(query,
        "INSERT INTO evidence_net.edges(edge_id,source_node,target_node,relation_type,relation_domain,evidence_state,supporting_card_id,supporting_card_revision,source_ref) VALUES($1,$2,$3,$4,$5,'proposed',$6,$7,$8) ON CONFLICT DO NOTHING RETURNING edge_id,evidence_state,relation_type,relation_domain",
        [args.edge_id,args.source_node,args.target_node,args.relation_type,
         args.relation_domain,args.supporting_card_id||null,args.supporting_card_revision||null,
         args.source_ref]);
      if (!row) throw new Error("duplicate edge or missing source records");
      return {...row, proposed_by:context.authenticated_principal,
              authority_granted:false, fact_verified:false};
    },
    async dictionaryPath({word}) {
      if (!dictionaryEnabled) throw new Error("dictionary unavailable");
      const row=await one(query,
        "SELECT word,synset,definition,chain,depth FROM echo_dictionary.wordnet_context WHERE word=$1",
        [word]);
      return row && {...row, evidence_status:"source_observation_only",admitted_new_words:0};
    },
    async compareWords({left,right,max_hops=12}) {
      if (!dictionaryEnabled) throw new Error("dictionary unavailable");
      const records=rowsOf(await query(
        "SELECT word,synset,chain FROM echo_dictionary.wordnet_context WHERE word=$1 OR word=$2",
        [left,right]));
      if (records.length !== 2 || left === right) return {decision:"abstain",reason:"missing or repeated source word"};
      const d=Object.fromEntries(records.map(r=>[r.word,r]));
      if (!d[left] || !d[right]) return {decision:"abstain",reason:"missing lexical sense"};
      const cards=rowsOf(await query(
        "SELECT card_id,revision FROM card_protocol.card_revisions WHERE (card_id=$1 OR card_id=$2) AND revision=1 AND card_kind='lexical_context'",
        ["lex:"+left,"lex:"+right]));
      if (cards.length !== 2) return {decision:"abstain",reason:"missing pinned evidence cards"};
      const counts=rowsOf(await query(
        "SELECT source_ref, count(*)::integer AS edge_count FROM evidence_net.edges WHERE source_ref=$1 OR source_ref=$2 GROUP BY source_ref",
        ["genesis.wordnet_chain:"+left,"genesis.wordnet_chain:"+right]));
      const bySource=Object.fromEntries(counts.map(r=>[r.source_ref,Number(r.edge_count)]));
      if ([left,right].some(w=>!Array.isArray(d[w].chain) ||
           d[w].chain.length>max_hops ||
           bySource["genesis.wordnet_chain:"+w] < d[w].chain.length)) {
        return {decision:"abstain",reason:"incomplete or overlong evidence path"};
      }
      const common=[...new Set(d[left].chain)].filter(x=>d[right].chain.includes(x));
      const all=rowsOf(await query("SELECT word,chain FROM echo_dictionary.wordnet_context",[]));
      const frequency=x=>all.filter(r=>Array.isArray(r.chain)&&r.chain.includes(x)).length;
      const candidates=common.filter(x=>x!=="entity"&&frequency(x)<=Math.max(2,Math.floor(all.length*0.25))
         && !(x===left||x===right) || false);
      // Exact matching synset is distinct from common generic lexical ancestors.
      const winner=d[left].synset===d[right].synset?d[left].chain.at(-1):
           candidates.sort((a,b)=>frequency(a)-frequency(b)||a.localeCompare(b))[0];
      if (!winner) return {decision:"abstain",reason:"generic-only or no specific common ancestor"};
      return {decision:"supported_provisional",relation:"lexical_shared_ancestor",
        ancestor:winner,scope:"dictionary_only",
        sources:["genesis.wordnet_chain:"+left,"genesis.wordnet_chain:"+right],
        pinned_cards:cards, independent_verification:false,admitted_new_words:0};
    }
  };
}
