#!/usr/bin/env python
# coding:utf-8

import os
import subprocess

def log(msg):
    print '[Prepare] %s' % msg

LOG = lambda msg: log(msg)


def run_task(task):
    pool, device, sz = task[0], task[1], task[2]
    new_env = os.environ.copy()
    new_env['SIZE'] = sz
    new_env['CEPH_POOL'] = pool
    new_env['CEPH_DEVICE'] = device

    cmd = ['fio', 'prepare.job']

    p = subprocess.Popen(cmd, env=new_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p


def main():
    ceph_pool = 'nbs'
    ceph_devices = ['vm1', 'vm2', 'vm3']

    count = 0
    task_num = len(ceph_devices)
    max_concurrent_task_num = 2
    task_handles = []
    for device in ceph_devices:
        task = (ceph_pool, device, '10G')
        handle = run_task(task)
        
        task_handles.append(handle)
        count += 1
        if not (count % max_concurrent_task_num) or \
            count == task_num:
            # wait 
            LOG('waiting (%d tasks)..' % count)
            for handle in task_handles:
                handle.wait()
            count = 0
            task_handles = []


if __name__ == '__main__':
    main()
