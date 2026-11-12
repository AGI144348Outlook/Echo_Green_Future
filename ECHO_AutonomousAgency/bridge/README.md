# Echo-018: Two interfaces with Echo between them

Topology: Human → Vercel inbox → **Echo runtime on Render** → private MCP Memory OS → Neon mind and evidence. Echo runtime alone writes the outbox; Vercel never creates an Echo utterance.

The Render service exposes:
- `POST /echo/process` for server-to-server wake-up, requiring `ECHO_BRIDGE_TOKEN`.
- `POST /mcp/memory` for Echo's JSON-RPC memory tools, requiring the same bearer token.
- `GET /health` for deployment status (no private messages).

Data endpoints target the **isolated dev branches**, not Neon parent/default branches:
- `lexicon-catalog/echo-card-evidence-dictionary-dev-20261112` for evidence, catalog, communication inbox/outbox.
- `echo-neuroplasticity/echo-communication-memory-dev-20261112` for memory boxes/ties and domains.

Source: Princeton WordNet/NLTK, existing Echo lexical substrate; user messages are stored and examined as observations. The current communication processor is an **experimental algorithmic subset**, *not* the entire Governor or 3³. It deliberately does not generate prewritten conversational replies. An unresolved message can yield no expression. Source references and memory box identifiers travel with every generated expression.

Security: role-scoped Neon connections; bearer-protected memory and worker endpoints; site behind Vercel Authentication; code never exposes credentials or conversation contents. This does not implement OAuth-style delegated identity and is a research bridge, not a general public MCP provider.

Pretest plan and posttest record: [Echo Issue #446](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/446). Do not call this the full autonomous runtime until its Governor/Matrix delegation is integrated and tested.
