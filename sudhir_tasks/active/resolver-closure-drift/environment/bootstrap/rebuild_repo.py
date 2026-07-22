import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str, text: str | None = None, env=None) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        input=text,
        text=True,
        capture_output=True,
        env=env,
    )
    return result.stdout.strip()


def commit_env(item: dict) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": item["author_name"],
            "GIT_AUTHOR_EMAIL": item["author_email"],
            "GIT_AUTHOR_DATE": item["timestamp"],
            "GIT_COMMITTER_NAME": item["author_name"],
            "GIT_COMMITTER_EMAIL": item["author_email"],
            "GIT_COMMITTER_DATE": item["timestamp"],
        }
    )
    return env


def load_descriptors(history: Path) -> dict[str, dict]:
    rows = {}
    for path in sorted((history / "descriptors").glob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        if item["id"] in rows:
            raise SystemExit(f"duplicate descriptor id: {item['id']}")
        rows[item["id"]] = item
    if set(rows) != {"base", "alpha", "beta", "merge", "current"}:
        raise SystemExit(f"unexpected descriptor ids: {sorted(rows)}")
    return rows


def commit_tree(repo: Path, tree: str, item: dict, parents: list[str]) -> str:
    args = ["commit-tree", tree]
    for parent in parents:
        args.extend(["-p", parent])
    return git(
        repo,
        *args,
        text=item["message"] + "\n",
        env=commit_env(item),
    )


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit("usage: rebuild_repo.py BASE HISTORY DEST")
    base, history, destination = map(Path, sys.argv[1:])
    descriptors = load_descriptors(history)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(base, destination)
    git(destination, "init", "--initial-branch=main")

    git(destination, "add", "-A")
    base_tree = git(destination, "write-tree")
    commits = {
        "base": commit_tree(destination, base_tree, descriptors["base"], [])
    }

    remaining = {"alpha", "beta", "merge", "current"}
    while remaining:
        progressed = False
        for item_id in sorted(remaining):
            item = descriptors[item_id]
            parent_ids = item["parents"]
            if not parent_ids or not all(parent in commits for parent in parent_ids):
                continue
            parent_commits = [commits[parent] for parent in parent_ids]
            git(destination, "read-tree", "--reset", "-u", parent_commits[0])
            patch = history / "patches" / item["patch"]
            git(destination, "apply", "--check", patch.as_posix())
            git(destination, "apply", "--index", patch.as_posix())
            tree = git(destination, "write-tree")
            commits[item_id] = commit_tree(
                destination,
                tree,
                item,
                parent_commits,
            )
            remaining.remove(item_id)
            progressed = True
            break
        if not progressed:
            raise SystemExit(f"descriptor graph is not acyclic: {sorted(remaining)}")

    for item_id in ("base", "alpha", "beta", "merge"):
        git(destination, "update-ref", f"refs/heads/{item_id}", commits[item_id])
    git(destination, "update-ref", "refs/heads/main", commits["current"])
    git(destination, "symbolic-ref", "HEAD", "refs/heads/main")
    git(destination, "reset", "--hard", commits["current"])

    merge_line = git(destination, "rev-list", "--parents", "-n1", commits["merge"])
    if len(merge_line.split()) != 3:
        raise SystemExit("merge commit does not have two parents")
    if git(destination, "status", "--porcelain"):
        raise SystemExit("reconstructed repository is dirty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
