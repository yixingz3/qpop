# Releasing `forward-qpop` to PyPI

This repo publishes with **trusted publishing (OIDC)** — no API tokens are stored. The workflow is
[`publish.yml`](publish.yml): publishing a GitHub **Release** uploads to PyPI; a manual run uploads to
**TestPyPI** (a dry run).

## One-time setup

### 1. Configure the trusted publisher on PyPI
On <https://pypi.org> → account menu → **Publishing** → **Add a pending publisher** (the project does
not exist yet, so it's "pending" until the first upload creates it):

| Field | Value |
|-------|-------|
| PyPI Project Name | `forward-qpop` |
| Owner | `yixingz3` |
| Repository name | `chokepoint-research-engine` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

### 2. (Optional) Same on TestPyPI
Repeat on <https://test.pypi.org> with **Environment name `testpypi`** to enable the dry-run path.

### 3. Create the GitHub environments
Repo → **Settings → Environments** → create `pypi` (and `testpypi`). Optional but recommended: add
yourself as a **required reviewer** on `pypi` so each real publish needs a one-click approval.

> The repo can be private during setup, but make it **public before the first release** so the PyPI
> page's repository links resolve.

## Cut a release

1. Bump the version in **`pyproject.toml`** *and* **`src/forward_qpop/__init__.py`** (keep them equal),
   commit, and push.
2. (Optional dry run) Actions → **Publish to PyPI** → **Run workflow** → uploads to TestPyPI;
   verify with `pip install -i https://test.pypi.org/simple/ forward-qpop`.
3. Create a **GitHub Release** with tag `v<version>` (e.g. `v0.1.0`). The workflow builds, runs
   `twine check`, and publishes to PyPI.

## Notes
- A published version is **immutable** — you cannot overwrite it; bump the version for any fix.
- `python -m build` + `twine check` already pass locally, so the build step is verified.
