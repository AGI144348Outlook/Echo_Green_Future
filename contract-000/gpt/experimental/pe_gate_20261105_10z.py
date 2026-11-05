"""GPT-only synthetic Pe-gated grammar slots; NOT canonical Echo. Seed 20261105."""
import json, random
SEED=20261105
GLYPHS=list("אבגדהוזחטיכלמנסעפצקרשת")+list("ךםןףץ")
SLOTS=["noun","adjective","anchor","verb","adverb","fused","prep_forward","prep_backward","interrogative","join","split","relation","absence","turned","nested","catch","sense"]
assert len(GLYPHS)==27 and len(SLOTS)==17
HOSTS=[g for g in GLYPHS if g!="פ"][:17]
ASSIGN=dict(zip(HOSTS,SLOTS))
BASE={g:"ordinary:"+g for g in GLYPHS}
def access(host,pe_active):
    return ASSIGN.get(host) if pe_active else None
def compose(n,seed):
    rng=random.Random(seed)
    return tuple(rng.sample(GLYPHS,n))
def influence(edge=True,source=0.25):
    return source*0.4 if edge else 0.0
checks={
"T1_unique_glyphs":len(set(GLYPHS))==27,
"T2_cube_bijection":len({(i//9,(i//3)%3,i%3) for i in range(27)})==27,
"T3_injective_17":len(ASSIGN)==17 and len(set(ASSIGN.values()))==17,
"T4_inactive_blocks":all(access(g,False) is None for g in GLYPHS),
"T5_active_permits":all(access(g,True)==s for g,s in ASSIGN.items()),
"T6_baseline_unchanged":all(BASE[g]=="ordinary:"+g for g in GLYPHS),
"T7_unassigned_blocks":all(access(g,True) is None for g in GLYPHS if g not in ASSIGN),
"T8_ring_arity":all(len(compose(n,SEED))==n for n in (2,3,4)),
"T9_seed_replay":compose(4,SEED)==compose(4,SEED),
"T10_edge_ablation":influence(True)!=0 and influence(False)==0,
}
print(json.dumps({"seed":SEED,"checks":checks,"passed":sum(checks.values()),"total":len(checks),"assigned":ASSIGN,"examples":{str(n):compose(n,SEED) for n in (2,3,4)},"directed":influence(True),"ablated":influence(False)},ensure_ascii=False,sort_keys=True))
