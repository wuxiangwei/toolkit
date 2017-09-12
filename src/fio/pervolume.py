#!/usr/bin/env python
# coding:utf-8

import os
import glob
import time
import subprocess
import fio_parser

# 环境变量
BS = 'BS'
TYPE = 'TYPE'
DEVICE = 'DEVICE'

RES_DIR = 'result/pv'  # 存放结果的路径


def init():
    if not os.path.exists(RES_DIR):
        subprocess.check_output(['mkdir', '-p', RES_DIR])


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

    print '[Pervolume] Start to run task (%s, %s)..' % task
    subprocess.check_output(cmd, env=new_env)
    print '[Pervolume] The task (%s, %s) is completed' % task


def main():
    
    device = 'vm01'
    tasks = [
        # (BS, TYPE)
        ('4k', 'randwrite'),
        ('4k', 'randread'),
        ('4k', 'readwrite'),
        ('512k', 'write'),
        ('512k', 'read'),
        ('512k', 'readwrite'),
    ]

    init()
    # TODO: 铺底数据

    for task in tasks:
        start = time.time()
        run_task(task, device)
        elapsed = time.time() - start
        print '[Pervolume] Elapsed time: %d (s)\r\n' % elapsed
        # TODO: 存储端drop_cache清缓存

    print '[Pervolume] Start to parse result..'
    for res in glob.glob(RES_DIR+'/*.rs'):
        fio_parser.parse(res)

    print '[Pervolume] Finished!'


if __name__ == '__main__':
    main()

