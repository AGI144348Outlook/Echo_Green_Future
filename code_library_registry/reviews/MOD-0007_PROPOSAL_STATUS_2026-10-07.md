# MOD-0007 proposal status — 2026-10-07

Selection: 1 repository.

| Ordinal | Repository issue | Disposition | Reason |
|---:|---|---|---|
| 31 | [excalidraw/excalidraw#12216](https://github.com/excalidraw/excalidraw/issues/12216) | Select | Current source still permits a hardware eraser path to bypass view-only mode; nearby tests provide a focused native adaptation seam; no matching PR was found; root license is MIT. |
| 32 | [OpenHands/OpenHands#17055](https://github.com/OpenHands/OpenHands/issues/17055) | Defer/watch | Strong conceptual fit, but it is explicitly a cross-repository RFC awaiting agreement and follow-up implementation issues. MOD-0007 is only a UI/resource admission primitive, not backend RBAC. |
| 33 | [open-webui/open-webui#31880](https://github.com/open-webui/open-webui/issues/31880) | Reject duplicate | PR [#31882](https://github.com/open-webui/open-webui/pull/31882) already implements the disabled-server enforcement path. The target license also includes branding restrictions and a CLA. |
| 34 | [jupyterlab/jupyterlab#19633](https://github.com/jupyterlab/jupyterlab/issues/19633) | Reject duplicate/scope | Draft PR [#19789](https://github.com/jupyterlab/jupyterlab/pull/19789) already adds the requested lock indicator; the issue is UI signaling rather than admission enforcement. |
| 35 | [tldraw/tldraw#10942](https://github.com/tldraw/tldraw/issues/10942) | Reject policy/license | The interaction distinction is relevant, but tldraw's standing policy says unsolicited external PRs are automatically closed, and its root license restricts production use. |

The Excalidraw proposal is prepared but not submitted. No upstream contact or outreach occurred.
