#!/usr/bin/env python
# coding:utf-8

import os
import sys


def list_comps(path):
    return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]


def get_dirs(path, comps):
    bin_dirs = []
    for comp in comps:
        comp_path = os.path.join(path, comp)
        for dirpath, dirnames, filenames in os.walk(comp_path):
            if 'bin' in dirnames:
                bin_path = os.path.join(dirpath, 'bin')
                bin_dirs.append(bin_path)
    return bin_dirs


def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    tools_dir = os.path.join(current_dir, 'tools')
    comps = list_comps(tools_dir)
    bin_dirs = get_dirs(tools_dir, comps)

    path_env = ':'.join(bin_dirs) + ':$PATH'
    print 'export PATH=' + path_env


if __name__ == '__main__':
    main()
