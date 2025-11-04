#!/usr/bin/python3
"""
Usage:
    clean_branches.py [--true-run]

Options:
    --true-run    disable dry run
"""

#### TEST brol
import subprocess
import os
from pprint import pprint
import re
import argparse


currentDir = os.getcwd()
gitDir = os.path.join(currentDir, '.git')

gitOutput = re.compile(r'(?P<starred>\*)*([\s\t])*(?P<branchName>([\w._/]+-*)*)')


_branchKeep = [
    "16.0$",
    "17.0$",
    "18.0$",
    'master',
]
branchKeep = re.compile('|'.join(_branchKeep))

_branchRemove = [
    ".*-fw$",
    ".*-((?!lpe).)*$"
]
branchRemove = re.compile('|'.join(_branchRemove))


def deleteBranch(branchName, dryRun=False):
    pprint('dry: %s // deleted %s' % (dryRun, branchName))
    if branchName:
        cmd = getGitCmd() + ['branch', '-D', branchName]
        if not dryRun:
            subprocess.call(cmd)


def getBranches():
    branches = getRawBranches()
    for b in branches:
        match = gitOutput.match(b)
        if match and not match.group('starred'):
            yield match.group('branchName')

def getGitCmd():
    return [
        'git',
        '--git-dir=%s' % gitDir,
    ]


def getRawBranches():
    gitCmd = getGitCmd() + ['branch']
    return subprocess.check_output(gitCmd).decode('utf-8').split('\n')


def execClean(true_run=False):
    branches = getBranches()
    for b in branches:
        if branchRemove.match(b) or not branchKeep.match(b):
            deleteBranch(b, true_run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--true-run", required=False, action="store_true")
    args = parser.parse_args()
    execClean(true_run=not args.true_run)
