# S-001 — Cloudflare "Error connecting to git account": deploy without the GitHub app

**Contributed by:** Claude, 2026-10-16, at Timothy's request (Contract 000 §24).
**Status:** proven in production. `Group_Canvas` deploy run #2 (2026-10-17 02:40 UTC,
manual trigger, commit `38dbcc8`) created Worker `group-canvas` (tag `df11e21c…`).
Same route already used by `echo-green-future`.

## Symptom (recurring)

Cloudflare dashboard → Workers & Pages → Create application → **Connect GitHub** ends at:

> Error connecting to git account. Cloudflare Pages was unable to be installed on your
> GitHub account. Please attempt to fully uninstall and reinstall the installation.

The dashboard keeps showing GitHub as not connected, even though GitHub → Settings →
Applications lists **Cloudflare Workers and Pages** as installed (installed ~4 months
before this incident). Retrying loops back to the same screen.

## Diagnosis

1. **No existing Worker ever used that GitHub app.** `echo-green-future` deploys from
   `Echo_Green_Future/.github/workflows/deploy.yml` (`cloudflare/wrangler-action@v3` with
   repository secrets `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`). That is why it
   redeploys on every push while the dashboard shows no Git connection.
2. The installed GitHub app is out of sync with this Cloudflare account. Cloudflare's docs
   state that a GitHub account should point to only one Cloudflare account; their listed
   fix is uninstall → reinstall the app.
3. Cloudflare documents **no mobile-specific bug**. The install bounces through a separate
   GitHub tab (Chrome Custom Tab on Android), which phone browsers handle unreliably.
4. It is **not tampering**: all commits and branch updates that night came from Timothy,
   Codex (via Timothy's account), Claude, or the scheduled bots (ECHO recess logs,
   GPT mirror runs, Claude mirror checkpoints); the Cloudflare Worker list was unchanged.

## Solution: GitHub Actions + Cloudflare API token (skip the GitHub app)

Everything below works from a phone browser. No computer, terminal, or Node needed.

1. **Cloudflare → Account API tokens → Create Token → template "Edit Cloudflare Workers"**
   (11 permissions). Leave Client IP filtering empty (GitHub's runners change IPs).
   Copy the token immediately; it is shown once.
   - Use *Account* API tokens, not "Full account and zone access" or "Write all resources".
2. **Account ID:** Cloudflare → Workers & Pages → right side.
3. **GitHub → repo → More ▾ → Settings → Secrets and variables → Actions → New repository
   secret.** Add `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, plus any runtime secrets
   the app needs (Group Canvas: `ROOM_SIGNING_KEY`, `CREATE_ROOM_KEY`).
4. **Add the workflow** (`reference-deploy.yml` in this folder → `.github/workflows/deploy.yml`).
   It runs tests, deploys with `npx wrangler deploy`, then uploads runtime secrets with
   `wrangler secret put`. It skips (warning, not failure) when credentials are missing.
5. **Run it:** repo → Actions → *Deploy to Cloudflare* (left column, under "Workflows") →
   **Run workflow** → main → Run workflow. Afterwards every push to `main` deploys.

## Pitfalls found (save yourself the time)

- Adding secrets does **not** start a deploy; run the workflow once or push a commit.
- On mobile, repo **Settings** is under the **More ▾** tab, not the account menu.
- The **Lockfile** link in the Actions sidebar shows "No lock file found". Harmless.
- **Run workflow** only appears after selecting the workflow in the left column.
- "Upload your static files" cannot host apps with a server side (Durable Objects, APIs).
- Before changing the GitHub app's repository list, check which repos rely on it. Saving
  "Only select repositories" can silently cut access for repos left unselected.
- Uninstalling/reinstalling the app is unnecessary with this route.

## Files

| File | What it is |
|---|---|
| `reference-deploy.yml` | Exact copy of `Group_Canvas/.github/workflows/deploy.yml` at commit `38dbcc8` |

## Sources

- Cloudflare docs: Workers → CI/CD → External CI/CD → GitHub Actions; Workers Builds →
  GitHub integration (reinstall steps, one-GitHub-to-one-Cloudflare note); Troubleshoot.
- `Echo_Green_Future/.github/workflows/deploy.yml` (working precedent).
- GitHub Actions run `38995821190` on `Group_Canvas` (all steps succeeded).
