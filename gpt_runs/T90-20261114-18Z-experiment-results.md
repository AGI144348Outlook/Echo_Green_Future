# GPT T90 independent synthetic replay — 2026-11-14 18Z

Prospective Issue #474 posted BEFORE execution: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/474 . Post-test observations in same issue comment 6881892454. Previous source: `gpt_experiments/T89_multiring_controls.py` Git blob `70cddd43dc08a8fbc3536f00dda072659528e904`, commit 4b033529cbfd256d01986808d1e9e083a2406365. Exact source transferred from GitHub connector result because raw HTTP DNS unavailable; independent Git blob SHA1 over 2434 bytes matched. Python 3.13.5, command `python T89_multiring_controls.py > results.json`. Output SHA256 `068b1594f28666a953b86281fe62c856f26caa2a68e25d0f2d25c574e47a0d01`. Fixed seeds 11,23,37,53. 10 test types × 4 seeds = 40/40 defined booleans true. All measurements are synthetic and from the committed source.

| Seed | Pair ablation | Triadic ablation | Shuffled affinity | Frequency-only | Radius min | Radius max |
|---|---:|---:|---:|---:|---:|---:|
| 11 | 1.3005563875628445 | 1.3951074095627034 | 0.26741108663323765 | 0.2400000000000001 | 0.9054895458160035 | 1.0969338426507664 |
| 23 | 1.4089430110066432 | 0.7433918448849945 | 0.0654987748730484 | 0.24000000000000027 | 0.9000268330347492 | 1.0895877057014016 |
| 37 | 1.8014789144651917 | 0.8109269853314532 | 0.16350863584449737 | 0.24000000000000016 | 0.9188187980879021 | 1.0999747810087894 |
| 53 | 1.3839122780080617 | 0.9100925004721832 | 0.0906640022404688 | 0.2400000000000001 | 0.9146594304634413 | 1.0998106210203888 |

Defined test types: unique IDs, 3³ bijection, ordered 2-ring, ordered 3/4-ring, no-op, uncoupled frequency, pairwise ablation, triadic ablation, shuffled affinity, bounded deformation. No failed booleans. Caveats: ring-order tests tautological, affinity uses ordinal index not authentic gematria, phase difference unwrapped, frequency shift algebraically fixed, and no semantic or physical validation. Next experimental plan requires a new prospective preregistration for circular-distance and real gematria controls. No CI or production changes.
