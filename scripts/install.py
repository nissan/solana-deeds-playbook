#!/usr/bin/env python3
"""Put a pinned copy of the playbook into a deed repository, or check one.

    install.py apply TARGET   copy playbook/ to TARGET/docs/playbook/, write its import.json
                              and add the pointer section to TARGET/AGENTS.md
    install.py check TARGET   exit 1 if TARGET's copy differs from its own import.json

Run from a clean checkout of this repository. Nothing outside TARGET/docs/playbook/ and
TARGET/AGENTS.md is written. No network, no git commands in TARGET.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "playbook"
BEGIN = "<!-- deeds-playbook:begin (managed by nissan/solana-deeds-playbook scripts/install.py) -->"
END = "<!-- deeds-playbook:end -->"
SECTION = f"""{BEGIN}
## Deed playbook

When the owner says "begin", or on any resume, read [the deed playbook](docs/playbook/PLAYBOOK.md) after this contract. It covers kickoff, builder briefs, devnet work, review and merge, the build journal, the demo video, the article and social posts, public source and the retrospective. It is a pinned copy of `nissan/solana-deeds-playbook` and gives no authority: this contract and the owner's instruction win. Do not edit the copy; propose changes to the master.
{END}
"""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(base):
    return sorted(p for p in base.rglob("*") if p.is_file() and p.name != "import.json"
                  and "__pycache__" not in p.parts)


def apply(target):
    if subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "playbook"],
                      capture_output=True, text=True, check=True).stdout.strip():
        raise SystemExit("playbook/ has uncommitted changes; commit before installing")
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    agents = target / "AGENTS.md"
    if not agents.is_file():
        raise SystemExit(f"{agents} not found")
    dest = target / "docs" / "playbook"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SOURCE, dest, ignore=shutil.ignore_patterns("__pycache__"))
    manifest = {"schemaVersion": 1, "source": "nissan/solana-deeds-playbook", "commit": commit,
                "path": "playbook", "modified": False,
                "files": {str(p.relative_to(dest)): digest(p) for p in files(dest)}}
    (dest / "import.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8")
    text = agents.read_text(encoding="utf8")
    if BEGIN in text:
        if END not in text:
            raise SystemExit("AGENTS.md has a playbook section with no end marker")
        head, rest = text.split(BEGIN, 1)
        text = head + SECTION + rest.split(END, 1)[1].lstrip("\n")
    else:
        text = text.rstrip("\n") + "\n\n" + SECTION
    agents.write_text(text, encoding="utf8")
    print(f"installed {len(manifest['files'])} files from {commit[:7]} into {dest}")


def check(target):
    dest = target / "docs" / "playbook"
    manifest = json.loads((dest / "import.json").read_text(encoding="utf8"))
    actual = {str(p.relative_to(dest)): digest(p) for p in files(dest)}
    problems = [f"changed or missing: {n}" for n, h in manifest["files"].items() if actual.get(n) != h]
    problems += [f"not in import.json: {n}" for n in actual if n not in manifest["files"]]
    if BEGIN not in (target / "AGENTS.md").read_text(encoding="utf8"):
        problems.append("AGENTS.md has no playbook section")
    for line in problems:
        print("FAIL:", line)
    if problems:
        return 1
    print(f"PASS: {len(actual)} files match import.json (source commit {manifest['commit'][:7]})")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("apply", "check"):
        raise SystemExit(__doc__)
    where = Path(sys.argv[2]).resolve()
    sys.exit(apply(where) if sys.argv[1] == "apply" else check(where))
