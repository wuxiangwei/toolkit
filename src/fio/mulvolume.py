#!/usr/bin/env python
# coding:utf-8

import os
import time
import glob
import fio_parser
import subprocess

BS = 'BS'
TYPE = 'TYPE'
DEVICE = 'DEVICE'

DEVICE_NUM = 10  # 参与测试块的数量
CEPH_POOL = 'nbs'
RES_DIR = 'result/mv'


def LOG(msg):
    print '[Multivolume] %s' % msg


def init():
    if not os.path.exists(RES_DIR):
        subprocess.check_output(['mkdir', '-p', RES_DIR])


def get_devices():
    ret = []
    for i in xrange(1, DEVICE_NUM):
        ret.append('vm%d' % i)

    out = subprocess.check_output(['rbd', 'list', CEPH_POOL])
    devices = out.split('\n')[:-1]

    for device in ret:
        # create device if not exists
        if device not in devices:
            subprocess.check_output(['rbd', 'create', '%s/%s' % (CEPH_POOL, device), '--size', '10G'])

    return ret


def _run_task(task, device):
    fn = 'mv-' + '-'.join(task) + '-' +  device + '.rs'
    fpath = os.path.join(RES_DIR, fn)

    new_env = os.environ.copy()
    new_env[BS] = task[0]
    new_env[TYPE] = task[1]
    new_env[DEVICE] = device

    cmd = [
        'fio',
        'pervolume.job',
        '--output', fpath,
        '--output-format', 'json',
        '--section', task[2],
    ]

    LOG('Start to execute task (%s, %s, %s, %s)..' % (task[0], task[1], task[2], device))
    p = subprocess.Popen(cmd, env=new_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p


def run_task(task):
    devices = get_devices()
    wait_list = {}
    for device in devices:
        p = _run_task(task, device)
        wait_list[device] = p
    
    while len(wait_list):
        for k in wait_list.keys():
            p = wait_list[k]
            p.wait()
            LOG('The task (%s, %s, %s, %s) is completed' % (task[0], task[1], task[2], k))
            wait_list.pop(k)
        time.sleep(0.5)


def parse_task_result(task):
    res_fn = 'mv-' + '-'.join(task) + '-*.rs'
    res_path = os.path.join(RES_DIR, res_fn)

    # 解析每个fio的结果
    for res in glob.glob(res_path):
        fio_parser.parse(res)

    # 累加所有结果
    count = 0
    summary = {
        'write_bw': 0,
        'write_iops': 0,
        'write_lat': 0,
        'read_bw': 0,
        'read_iops': 0,
        'read_lat': 0,
    }

    csv_fn = 'mv-' + '-'.join(task) + '-*.csv'
    csv_path = os.path.join(RES_DIR, csv_fn)
    for csv in glob.glob(csv_path):
        with open(csv, 'r') as fd:
            lines = fd.readlines()
            # Skip header
            for line in lines[1:]:
                e = line.split(',')
                k = e[0]
                v = float(e[1])
                summary[k] += v
            count += 1

    # 平均延迟，IOPS和带宽为累加
    summary['write_lat'] /= count
    summary['read_lat'] /= count

    # 写到文件
    fn = 'mv-' + '-'.join(task) + '.csv'
    fpath = os.path.join(RES_DIR, fn)
    with open(fpath, 'w') as fd:
        write_bw_str = 'write_bw, ' + str(summary['write_bw']) + '\r\n'
        write_iops_str = 'write_iops, ' + str(summary['write_iops']) + '\r\n'
        write_lat_str = 'write_lat, ' + str(summary['write_lat']) + '\r\n'

        read_bw_str = 'read_bw, ' + str(summary['read_bw']) + '\r\n'
        read_iops_str = 'read_iops, ' + str(summary['read_iops']) + '\r\n'
        read_lat_str = 'read_lat, ' + str(summary['read_lat']) + '\r\n'

        fd.write(write_bw_str)
        fd.write(write_iops_str)
        fd.write(write_lat_str)
        fd.write(read_bw_str)
        fd.write(read_iops_str)
        fd.write(read_lat_str)


def main():
    
    tasks = [
        # BS, TYPE, SECTION
        ('4k', 'randread', 'iodepth_1'),
        ('4k', 'randread', 'iodepth_4'),
        ('4k', 'randread', 'iodepth_8'),
        ('4k', 'randread', 'iodepth_16'),
        ('4k', 'randread', 'iodepth_32'),
        ('4k', 'randread', 'iodepth_64'),
        ('4k', 'randwrite', 'iodepth_1'),
        ('4k', 'randwrite', 'iodepth_4'),
        ('4k', 'randwrite', 'iodepth_8'),
        ('4k', 'randwrite', 'iodepth_16'),
        ('4k', 'randwrite', 'iodepth_32'),
        ('4k', 'randwrite', 'iodepth_64'),
        ('4k', 'readwrite', 'iodepth_1'),
        ('4k', 'readwrite', 'iodepth_4'),
        ('4k', 'readwrite', 'iodepth_8'),
        ('4k', 'readwrite', 'iodepth_16'),
        ('4k', 'readwrite', 'iodepth_32'),
        ('4k', 'readwrite', 'iodepth_64'),
        ('512k', 'read', 'iodepth_1'),
        ('512k', 'read', 'iodepth_4'),
        ('512k', 'read', 'iodepth_8'),
        ('512k', 'read', 'iodepth_16'),
        ('512k', 'read', 'iodepth_32'),
        ('512k', 'read', 'iodepth_64'),
        ('512k', 'write', 'iodepth_1'),
        ('512k', 'write', 'iodepth_4'),
        ('512k', 'write', 'iodepth_8'),
        ('512k', 'write', 'iodepth_16'),
        ('512k', 'write', 'iodepth_32'),
        ('512k', 'write', 'iodepth_64'),
        ('512k', 'readwrite', 'iodepth_1'),
        ('512k', 'readwrite', 'iodepth_4'),
        ('512k', 'readwrite', 'iodepth_8'),
        ('512k', 'readwrite', 'iodepth_16'),
        ('512k', 'readwrite', 'iodepth_32'),
        ('512k', 'readwrite', 'iodepth_64'),
    ]

    init()

    for task in tasks:
        start = time.time()
        run_task(task)
        elapsed = time.time() - start
        LOG('Elapsed time: %d(s)\r\n' % elapsed)
        parse_task_result(task)


if __name__ == '__main__':
    main()
