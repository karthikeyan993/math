# Workflow files to install by hand

The session that wrote these couldn't push to `.github/workflows/` (its GitHub
token lacks the `workflow` scope). Copy them in yourself, e.g. in GitHub's web
editor:

- `check.yml` → `.github/workflows/check.yml` (new). Runs `tools/check_content.py`,
  `tools/test_check_content.py`, the build and `tools/smoke_test.cjs` on every
  push and pull request.
- `main.yml` → `.github/workflows/main.yml` (replaces it). Same deploy as before,
  plus a `tools/check_content.py` step that blocks a deploy with bad content.

Then delete this folder.
