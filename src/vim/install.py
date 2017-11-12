#!/usr/bin/env python
# coding=utf-8

import os


def install_vundle():
    home_dir = os.path.expanduser('~')
    dst_path = os.path.join(home_dir, '.vim/bundle/Vundle.vim')
    if not os.path.exists(dst_path):
        src_path = 'https://github.com/VundleVim/Vundle.vim.git'
        cmd = 'git clone %s %s' % (src_path, dst_path)
        os.system(cmd)


def replace_vimrc():
    cmd = 'cp .vimrc ~/'
    os.system(cmd)
    # subprocess.check_output(cmd, True)


def main():
    install_vundle()
    replace_vimrc()


if __name__ == '__main__':
    main()
