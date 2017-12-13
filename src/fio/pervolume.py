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
PV_RES_DIR = 'result/pv-result'


def log(msg):
    print '[Pervolume] %s' % msg

LOG = lambda msg: log(msg)


def init():
    if not os.path.exists(RES_DIR):
        subprocess.check_output(['mkdir', '-p', RES_DIR])

    if not os.path.exists(PV_RES_DIR):
        subprocess.check_output(['mkdir', '-p', PV_RES_DIR])


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

    LOG('Start to run task (%s, %s)..' % task)
    subprocess.check_output(cmd, env=new_env)
    LOG('The task (%s, %s) is completed' % task)


def main():
    
    device = 'vm1'
    tasks = [
        # (BS, TYPE)
        #  ('4k', 'randwrite'),
        ('4k', 'write'),
        # ('4k', 'randread'),
        # ('4k', 'readwrite'),
        # ('512k', 'write'),
        # ('512k', 'read'),
        # ('512k', 'readwrite'),
    ]

    init()
    # TODO: 铺底数据

    for task in tasks:
        start = time.time()
        run_task(task, device)
        elapsed = time.time() - start
        LOG('Elapsed time: %d (s)\r\n' % elapsed)
        # TODO: 存储端drop_cache清缓存

    LOG('Start to parse result..')
    for res in glob.glob(RES_DIR+'/*.rs'):
        fio_parser.parse(res)
        src_fn = res.split('/')[-1]
        src_fn = src_fn.split('.')[-2] + '.csv'
        src_fpath = os.path.join(RES_DIR, src_fn)
        dst_fpath = os.path.join(PV_RES_DIR, src_fn)
        os.rename(src_fpath, dst_fpath)

    LOG('Finished!')


if __name__ == '__main__':
    main()

