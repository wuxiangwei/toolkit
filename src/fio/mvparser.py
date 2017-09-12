#!/usr/bin/env python
# coding:utf-8

import os
import glob
import subprocess

RESULT_DIR = 'result/mv'
MV_RESULT_DIR = 'result/mv-result'


def LOG(msg):
    print '[Mulparser] ' + msg


def init():
    # TODO: 检查RESULT_DIR
    if not os.path.exists(MV_RESULT_DIR):
        subprocess.check_output(['mkdir', '-p', MV_RESULT_DIR])


def run_task(task):
    fn = 'mv-' + '-'.join(task) + '-iodepth_*' + '.csv'
    fpath = os.path.join(RESULT_DIR, fn)

    res = [f for f in glob.glob(fpath) if 'iodepth_' in f.split('-')[-1]]
    summary = {}
    for f in res:
        iodepth = int(f.split('-')[-1].split('.')[0].split('_')[-1])
        f_sum = {}
        with open(f, 'r') as fd:
            lines = fd.readlines()
            for line in lines:
                k, v = line.split(',')
                f_sum[k] = float(v)
        summary[iodepth] = f_sum

    summary2 = {
        'write_bw': [],
        'write_iops': [],
        'write_lat': [],
        'read_bw': [],
        'read_iops': [],
        'read_lat': [],
    }
    iodepths = sorted(summary.keys())
    for iodepth in iodepths:
        item = summary[iodepth]
        for k in item.iterkeys():
            v = item[k]
            summary2[k].append(v)

    iodepths = [str(i) for i in iodepths]
    summary2['write_bw'] = [str(i) for i in summary2['write_bw']]
    summary2['write_iops'] = [str(i) for i in summary2['write_iops']]
    summary2['write_lat'] = [str(i) for i in summary2['write_lat']]
    summary2['read_bw'] = [str(i) for i in summary2['read_bw']]
    summary2['read_iops'] = [str(i) for i in summary2['read_iops']]
    summary2['read_lat'] = [str(i) for i in summary2['read_lat']]


    # 写入文件
    res_fn = 'mv-' + '-'.join(task) + '.csv'
    res_fpath = os.path.join(MV_RESULT_DIR, res_fn)
    with open(res_fpath, 'w') as fd:
        header = ',' + ','.join(iodepths) + '\r\n'
        write_bw_str = 'write_bw,' + ','.join(summary2['write_bw']) + '\r\n'
        write_iops_str = 'write_iops,' + ','.join(summary2['write_iops']) + '\r\n'
        write_lat_str = 'write_lat,' + ','.join(summary2['write_lat']) + '\r\n'
        read_bw_str = 'read_bw,' + ','.join(summary2['read_bw']) + '\r\n'
        read_iops_str = 'read_iops,' + ','.join(summary2['read_iops']) + '\r\n'
        read_lat_str = 'read_lat,' + ','.join(summary2['read_lat']) + '\r\n'
        fd.write(header)
        fd.write(write_bw_str)
        fd.write(write_iops_str)
        fd.write(write_lat_str)
        fd.write(read_bw_str)
        fd.write(read_iops_str)
        fd.write(read_lat_str)


def main():
    tasks = [
        # BS, TYPE
        ('4k', 'randwrite'),
        ('4k', 'randread'),
        ('4k', 'readwrite'),
        ('512k', 'write'),
        ('512k', 'read'),
        ('512k', 'readwrite'),
    ]

    init()

    for task in tasks:
        run_task(task)
    print '[Mvparser] Finished!!'


if __name__ == '__main__':
    main()
