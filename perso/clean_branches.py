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
from docopt import docopt


currentDir = os.getcwd()
gitDir = os.path.join(currentDir, '.git')

gitOutput = re.compile('(?P<starred>\*)*([\s\t])*(?P<branchName>([\w._/]+-*)*)')


_branchKeep = [
    #'12.0$',
    #'13.0$',
    #'saas-13.5$',
    "14.0$",
    "15.0$",
    #"saas-15.3$",
    'master$',
    'master-wowl$',
]
branchKeep = re.compile('|'.join(_branchKeep))


def deleteBranch(branchName, dryRun=False):
    pprint('dry: %s // deleted %s' % (dryRun, branchName))
    if branchName:
        cmd = getGitCmd() + ['branch', '-D', branchName]
        if not dryRun:
            subprocess.call(cmd)


def getBranches():
    branches = getRawBranches()
    res = []
    for b in branches:
        match = gitOutput.match(b)
        if match and not match.group('starred'):
            res.append(match.group('branchName'))
    return res


def getGitCmd():
    return [
        'git',
        '--git-dir=%s' % gitDir,
    ]


def getRawBranches():
    gitCmd = getGitCmd() + ['branch']
    return subprocess.check_output(gitCmd).decode('utf-8').split('\n')


def execClean(opt):
    branches = getBranches()
    for b in branches:
        if not branchKeep.match(b):
            dry = not opt.get('--true-run', False)
            deleteBranch(b, dry)


if __name__ == '__main__':
    opt = docopt(__doc__)
    execClean(opt)
