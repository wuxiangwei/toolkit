#!/usr/bin/env python
# coding:utf-8

import os
import subprocess

def log(msg):
    print '[Prepare] %s' % msg

LOG = lambda msg: log(msg)
DEVICE_NUM = 200
CEPH_POOL = 'nbs'
CEPH_DEVICE_SIZE = 100 * 1024 # 100G
MAX_CONCURRENT_TASK_NUM = 20


def get_test_devices():
    # 如果测试块不存在，创建
    device_names = []
    for i in xrange(1, 1+DEVICE_NUM):
        device_names.append('vm%d' % i)

    out = subprocess.check_output(['rbd', 'list', CEPH_POOL])
    exist_devices  = out.split('\n')[:-1] 
    devices_to_create = [i for i in device_names if i not in exist_devices]
    for device in devices_to_create:
        subprocess.check_output(['rbd', 'create', '%s/%s' % (CEPH_POOL, device), '--size', str(CEPH_DEVICE_SIZE)])

    return device_names


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
    ceph_devices = get_test_devices()
    count = 0
    task_num = len(ceph_devices)
    task_handles = []
    for device in ceph_devices:
        task = (CEPH_POOL, device, str(CEPH_DEVICE_SIZE / 2)+'M')
        # task = (CEPH_POOL, device, '1024')
        handle = run_task(task)
        
        task_handles.append(handle)
        count += 1
        if not (count % MAX_CONCURRENT_TASK_NUM) or \
            count == task_num:
            # wait 
            LOG('waiting (%d tasks)..' % count)
            for handle in task_handles:
                handle.wait()
            count = 0
            task_handles = []


if __name__ == '__main__':
    main()
