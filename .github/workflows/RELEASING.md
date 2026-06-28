# Releasing

The primary distribution is the **Claude Code plugin** (`/plugin marketplace add yixingz3/qpop`), which
tracks `main` — no release step is needed for plugin users to get updates. The release workflow
([`publish.yml`](publish.yml)) is for **version tags + the Python package**.

## Cut a release (tag + build)

1. Bump the version in `.claude-plugin/plugin.json`, `pyproject.toml`, and
   `src/forward_qpop/__init__.py` (keep them equal); commit and push.
2. Create a **GitHub Release** with tag `v<version>` (e.g. `v0.1.0`).
3. The workflow builds the sdist + wheel, runs `twine check`, and **attaches them to the release**.
   PyPI is **not** touched by default (it's backlog — see below).

## Publishing to PyPI (opt-in, when you're ready)

PyPI uses **trusted publishing (OIDC)** — no API token. One-time setup:

1. **PyPI → Publishing → Add a pending publisher:** project `forward-qpop`, owner `yixingz3`,
   repo `qpop`, workflow `publish.yml`, environment `pypi`. (Optional: same on TestPyPI, env `testpypi`.)
2. **GitHub → Settings → Environments → create `pypi`** (optional: require yourself as a reviewer).

Then either:
- set repo variable **`PUBLISH_TO_PYPI = true`** (Settings → Secrets and variables → Actions → Variables)
  so every release also publishes to PyPI, **or**
- run the workflow manually (Actions → Release → Run workflow) with **target = `testpypi`** (dry run)
  or **`pypi`**.

## Notes
- A published PyPI version is immutable — bump the version for any fix.
- `python -m build` + `twine check` pass locally, so the build is verified.
