#!/usr/bin/env python
# coding:utf-8

import os
import subprocess

# 环境变量
BS = 'BS'
TYPE = 'TYPE'
DEVICE = 'DEVICE'

RES_DIR = 'result'  # 存放结果的路径


def init():
    if not os.path.exists(RES_DIR):
        os.mkdir(RES_DIR)


def run_task(task, device):
    fn = 'pv-' +  '-'.join(task) + '-' + device + '.rs'
    fpath = os.path.join(RES_DIR, fn)

    new_env = os.environ.copy()
    new_env[BS] = task[0]
    new_env[TYPE] = task[1]
    new_env[DEVICE] = device

    cmd = [
        "fio", 
        "pervolume.job", 
        "--output", fpath, 
        "--output-format", "json"
    ]

    print '[Pervolume] start to run task (%s, %s)..' % task
    subprocess.check_output(cmd, env=new_env)
    print '[Pervolume] the task (%s, %s) is completed' % task


def main():
    
    device = 'vm01'
    tasks = [
        # (BS, TYPE)
        ('4K', 'randwrite'),
        ('4K', 'randread'),
        ('4K', 'readwrite'),
        ('512K', 'write'),
        ('512K', 'read'),
        ('512K', 'readwrite'),
    ]

    init()
    # TODO: 铺底数据

    for task in tasks:
        run_task(task, device)
        # TODO: 清缓存


if __name__ == '__main__':
    main()
