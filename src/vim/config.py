#!/usr/bin/env python
#coding:utf-8

import os
import subprocess


def log(msg):
    print '[Config] %s' % msg

LOG = lambda msg: log(msg)


def main():
    cmds = [
        'mkdir -p ~/.vim',
        'cp .vimrc ~/',
        'sudo apt-get install ctags',
    ]

    for cmd in cmds:
        LOG('Start to run command %s' % cmd)
        subprocess.check_output(cmd, shell=True)

    LOG('Finished!!')


if __name__ == '__main__':
    main()

