# NVE-D-HOURLY-012 — Experimental summary
Date: 2026-10-09. Scope: finite digital fixture, not conceptual EVE/NVE validation.

Three opaque UTF-8 expressions × two independent seeds (19,73) × two synthetic transformations (additive, ordered-fold) × three depths (0,2,4) × three topologies (ring,star,mesh) × five budgets (250,1000,2500,5000,10000) = **540 completed configurations** and **2,025,000 baseline root generations**. All source expressions, including `(?):(?)::(?):(?)::|#|::(?):(?)::(?):(?)::#::(?)`, were preserved as opaque strings. No semantics assigned to symbols.

Executed **15,330,375 node transitions**: 6,075,000 baseline, 3,037,500 checkpoint prefixes, 3,037,500 durable replay suffixes, 3,037,500 receipt-loss replay suffixes, 142,875 fresh-interpreter suffixes. Baseline sent and applied 247,836 synthetic messages. Runtime 31.528 s. All 540 durable replays and all 15 fresh-interpreter resumes matched reference canonical states (`=`). All 540 deliberate lost-receipt negative controls changed final node states (`0` under equality criterion; `∆` recorded), and all failed the structural audit. Because a crash-boundary probe was injected in every configuration, these are engineered controls, not estimates of naturally occurring failure probability.

Independent structural auditor checked 540 checkpoints and arithmetic (`=`) but did not reimplement transitions. Arbitrary internal-state modification remains undetected by structural checks; external original digest comparison detects a mismatch (`0`), but locally stored digests are not independent authentication. No real process crash at the critical instant, fsync, external witness, or network was tested.

Historical IETF provenance: the independently authored Infinite Expanse Testing Framework source is present in AGI144348Outlook/Mashet-Echo-Drive main as `Infinitely Expandable Testing Framework Codex.txt`, blob `b8d28481be30b7619296e79ccf5cdc11b2f28c46`, identical to `experiments/nve-d/sources/ietf/01-framework.txt`. Mind Domain, Chronotool, and Master Codex source blobs were verified by Git tree. No affiliation with the Internet Engineering Task Force.

Code-library-registry assessments CLR-0036, CLR-0038, CLR-0040 were read and verified by blob identity; original executable sources and original RFC-0031/RFC-0033 specification files were not found in the two inspected branch trees. The CLR-0040 assessment references a user-uploaded `mashet_eve_v3.py` but is not that source. Search scope does not include every archive or branch.

DFE stages 5/7/8 are documented separately. EVE = Envelope Virtual Environment; NVE = Nested Virtual Environments. These results concern a DVE fixture, not CVE/DCVE/CDVE/CDCVE validity.

**Persistence caveat:** Full Python runner (SHA-256 `30de47f8dcf037d57541fc9f8e07c0b54479467a924c03afc979af8159b479c5`), 540 checkpoint files, row-level results and independent auditor are in the local downloadable Cycle 012 package, not in this GitHub summary. No protected registries modified, nothing merged or deployed.
