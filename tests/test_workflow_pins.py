"""Every non-local `uses:` step (third-party and first-party actions) in .github/workflows must be pinned to a full commit SHA.

A tag or branch ref (for example `release/v1` or `v4`) can move without any change in this
repository, so the code that runs in a job (including the OIDC publish jobs) could change between
two runs. The pin is a 40-hex commit SHA followed by a `# v...` comment naming the release tag it
was taken from. Bump the SHA and the comment together.
"""
import re
from pathlib import Path

import pytest

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
USES = re.compile(r"^\s*-?\s*uses:\s*(?P<ref>\S+)(?P<rest>.*)$")
PINNED = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")
VERSION_COMMENT = re.compile(r"^\s+#\s*v\d+(\.\d+)*\S*\s*$")


def _uses_lines():
    found = []
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = USES.match(line)
            if match and not match.group("ref").startswith("./"):
                found.append((path.name, number, match.group("ref"), match.group("rest")))
    return found


def test_workflows_have_uses_lines():
    assert _uses_lines(), "no `uses:` lines found; the glob or the regex is wrong"


@pytest.mark.parametrize(
    "name,number,ref,rest", _uses_lines(), ids=lambda v: str(v)
)
def test_uses_pinned_to_sha_with_version_comment(name, number, ref, rest):
    where = f"{name}:{number}"
    assert PINNED.match(ref), f"{where}: {ref} is not pinned to a 40-hex commit SHA"
    assert VERSION_COMMENT.match(rest), f"{where}: missing a '# vX.Y.Z' comment after {ref}"
