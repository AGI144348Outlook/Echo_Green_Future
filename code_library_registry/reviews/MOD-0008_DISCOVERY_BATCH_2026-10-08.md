# MOD-0008 discovery batch — repositories 36–40

Search began only after the generalized abstraction was committed at `bf1964722b609a1e7a50f22b1dcfbb23df18a781`.

| Ordinal | Repository / issue-first evidence | License and maintenance evidence | Decision |
|---:|---|---|---|
| 36 | `agronholm/apscheduler` — open issue [#1144](https://github.com/agronholm/apscheduler/issues/1144) reports wall-clock interval arithmetic failures across DST. Current `interval.py` blob `f06a2cc...` adds `timedelta` directly to zoned datetimes; current test blob `607f3f8...` lacks fold/gap cases. | MIT license (`LICENSE.txt` blob `238c0d3...`); active, non-archived; `docs/contributing.rst` blob `2d618a2...` requires local tests and quality checks. | **Selected, proposal prepared.** Adapt the absolute-time invariant and DST tests natively; do not transplant Echo code. Recheck for linked/competing PR immediately before any implementation. |
| 37 | `celery/django-celery-beat` — open issue [#1044](https://github.com/celery/django-celery-beat/issues/1044) is a start-time wakeup regression; issues #918/#956 cover adjacent time behavior. | BSD-3-Clause text present (`LICENSE` blob `2983da2...`); active, non-archived. No root contribution file was found in this pass. | Not selected. The reported defect is crontab/model wakeup optimization, not the frozen pure interval/civil-slot gate; native project knowledge dominates. |
| 38 | `apache/airflow` — open issue [#69543](https://github.com/apache/airflow/issues/69543) concerns parse-time `now()` changing serialized DAG versions. | Apache-2.0 text present (`LICENSE` blob `cda7cff...`); active, non-archived; root `CONTRIBUTING.rst` blob `00fe429...` exists. | Not selected. The issue is object construction/serialization stability, outside MOD-0008's due-decision contract. |
| 39 | `PrefectHQ/prefect` — open issue [#23204](https://github.com/PrefectHQ/prefect/issues/23204) reports daily interval anchors drifting across DST; #23294 covers Windows IANA timezone preservation. | Apache-2.0 text present (`LICENSE` blob `8a8f20e...`); active, non-archived; contribution guide located under `docs/contribute/dev-contribute.mdx`. | Watch only. Functional fit is strong, but Prefect's async schedule schema and date-generation semantics require a native patch; APScheduler #1144 is the narrower first proposal. |
| 40 | `dbader/schedule` — issue-first search for open timezone/DST work returned no matching issue. | MIT license (`LICENSE.txt` blob `7c51781...`); active, non-archived; no root contribution file found. | Not selected: no current issue to solve, so opening speculative scope would violate issue-first filtering. |

Batch result: 5 distinct repositories actually reviewed; 1 selected; cumulative progress **40/1,000**. Echo licensing is unresolved, so target licenses are recorded but compatibility and submission clearance are not asserted.

Resume at repository ordinal **41**.
