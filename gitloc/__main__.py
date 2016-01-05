#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main entry point. Invoke as `gitloc' or `python -m gitloc'.
"""
import sys
import re
from argparse import ArgumentParser
from datetime import datetime

import pyprind
from pygit2 import init_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE


def short_hash(commit):
    return str(commit.tree_id)[:6]


def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    repo = init_repository('.')
    commits = list(repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE))
    bar = pyprind.ProgBar(len(commits))

    total_commits = 0
    total_insertions = 0
    total_deletions = 0

    for commit in commits:
        # Skip merge commits
        if len(commit.parents) > 1:
            bar.update()
            continue

        # Skip commits not in 2015
        year = datetime.fromtimestamp(commit.commit_time).year
        if year != 2015:
            bar.update()
            continue

        # Skip commits by other authors
        if commit.author.name not in [u'LIU Dongyuan / 柳东原', 'Xhacker Liu', 'Dongyuan Liu']:
            bar.update()
            continue

        total_commits += 1

        if len(commit.parents) == 1:
            diff = repo.diff(commit.parents[0], commit)
        else:
            diff = commit.tree.diff_to_tree(swap=True)

        for patch in diff:
            old_path = patch.delta.old_file.path
            new_path = patch.delta.new_file.path

            # Ignore files with certain pattern
            regexp = r'^Pods'
            if re.match(regexp, old_path) or re.match(regexp, new_path):
                continue

            insertions = patch.line_stats[1]
            deletions = patch.line_stats[2]
            total_insertions += insertions
            total_deletions += deletions

        if args.verbose:
            short_message = commit.message.split('\n')[0]
            print '[' + commit.author.name + ']', short_hash(commit), short_message
            print '+' + str(diff.stats.insertions), '-' + str(diff.stats.deletions)

        bar.update()

    print str(total_commits) + ' commit(s)'
    print '+++ ' + str(total_insertions)
    print '--- ' + str(total_deletions)


if __name__ == '__main__':
    sys.exit(main())
