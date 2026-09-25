# PWA Hosting Environment

This directory is a standalone application project inside the `Echo_Green_Future` repository.

It is intentionally isolated from the rest of the repository.

## Initial state

The application opens to a blank white screen.

The only infrastructure included at this stage is:

- a minimal HTML application shell
- a web app manifest
- a service worker for installability/offline shell behavior
- a Cloudflare Wrangler configuration for static asset hosting

No ECHO application logic, data model, interface components, or runtime behavior is imported into this project.

## Project branch

`pwa-hosting-environment`

Future application development should remain inside this project boundary unless explicitly decided otherwise.
