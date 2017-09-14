#!/usr/bin/env python
# coding:utf-8

import os
import time
import glob
import fio_parser
import subprocess

# 环境变量
BS = 'BS'
TYPE = 'TYPE'
DEVICE = 'DEVICE'

# 测试参数
DEVICE_NUM = 50  # 参与测试块的数量
BIG_BS_DEVICE_NUM = 4
SMALL_BS_DEVICE_NUM = 25
CEPH_POOL = 'nbs'  # 测试块所在的存储池
FIO_RES_DIR = 'result/mv'  # 存放fio结果的路径
MANUAL_TASK = False # 手动任务，在多台主机运行时，手动来同步任务
CLIENT_NUM = 2  # 测试客户端的数量
CLIENT_ID = 0  # 当前客户端的编号


def log(msg):
    print '[Multivolume] %s' % msg

LOG = lambda msg: log(msg)


def init():
    if not os.path.exists(FIO_RES_DIR):
        subprocess.check_output(['mkdir', '-p', FIO_RES_DIR])


def get_devices():
    ret = []
    for i in xrange(1, 1+DEVICE_NUM):
        ret.append('vm%d' % i)

    out = subprocess.check_output(['rbd', 'list', CEPH_POOL])
    devices = out.split('\n')[:-1]

    for device in ret:
        # create device if not exists
        if device not in devices:
            subprocess.check_output(['rbd', 'create', '%s/%s' % (CEPH_POOL, device), '--size', '10240'])

    return ret


def get_test_devices(task):
    bs = task[0]
    all_devices = get_devices()
    client_device_num = DEVICE_NUM / CLIENT_NUM
    start_index = client_device_num * CLIENT_ID
    client_devices = all_devices[start_index: start_index+client_device_num]
    LOG("%d, %d, %d, %d" % (start_index, client_device_num, len(client_devices), len(all_devices)))
    # note: 越界检查
    ret = client_devices[0:SMALL_BS_DEVICE_NUM] if bs == '4k' else client_devices[0:BIG_BS_DEVICE_NUM]
    return ret


def _run_task(task, device):
    fn = 'mv-' + '-'.join(task) + '-' +  device + '.rs'
    fpath = os.path.join(FIO_RES_DIR, fn)

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
    devices = get_test_devices(task)
    LOG(str(devices))
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
    res_path = os.path.join(FIO_RES_DIR, res_fn)

    # 解析每个fio的结果
    for res in glob.glob(res_path):
        LOG('Parse %s ..'%res)
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
    csv_path = os.path.join(FIO_RES_DIR, csv_fn)
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
    fpath = os.path.join(FIO_RES_DIR, fn)
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
        while MANUAL_TASK:
            nt = raw_input('\r\n[Multivolume] Please input <Enter> to run task.. ')
            if nt == '':
                break

        start = time.time()
        run_task(task)
        elapsed = time.time() - start
        parse_task_result(task)
        LOG('Elapsed time: %d(s)' % elapsed)
    
    import mvparser
    mvparser.main()
    LOG('Finished!!')


if __name__ == '__main__':
    main()
