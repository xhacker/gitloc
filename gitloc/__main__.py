#!/usr/bin/env python
"""The main entry point. Invoke as `gitloc' or `python -m gitloc'.
"""
import sys

import pyprind
from pygit2 import init_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE


def short_hash(commit):
    return str(commit.tree_id)[:6]


def main():
    repo = init_repository('.')
    commits = list(repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE))
    bar = pyprind.ProgBar(len(commits))

    for commit in commits:
        # Skip merge commits
        if len(commit.parents) > 1:
            bar.update()
            continue

        short_message = commit.message.split('\n')[0]
        print '[' + commit.author.name + ']', short_hash(commit), short_message
        diff = repo.diff(commit)
        print '+' + str(diff.stats.insertions), '-' + str(diff.stats.deletions)

        bar.update()


if __name__ == '__main__':
    sys.exit(main())
