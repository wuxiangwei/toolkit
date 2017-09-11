#!/usr/bin/env python
#coding:utf-8

import sys
import json


def parse(filename):
    # TODO: 检查filename文件是否存在
    csv_filename = filename.split('.')[0] + '.csv'

    # 读取原始文件
    result_json = None
    with open(filename, 'r') as fd:
        result_text = fd.read()
        result_json = json.loads(result_text)

    jobs = result_json['jobs']
    bw_summary = {'write': [], 'read': []}
    iops_summary = {'write': [], 'read': []}
    latency_summary = {'write': [], 'read': []}
    jobnames = []
    for job in jobs:
        jobname = job['jobname']
        jobnames.append(jobname)
        # 统计带宽
        bw_summary['read'].append((jobname, job['read']['bw']))
        bw_summary['write'].append((jobname, job['write']['bw']))

        # 统计IOPS
        iops_summary['read'].append((jobname, job['read']['iops']))
        iops_summary['write'].append((jobname, job['write']['iops']))

        # 统计延迟
        latency_summary['read'].append((jobname, job['read']['lat_ns']['mean']))
        latency_summary['write'].append((jobname, job['write']['lat_ns']['mean']))

    with open(csv_filename, 'w') as fd:
        header = ',' + ','.join(jobnames) + '\r\n'
        fd.write(header)

        write_bw = [str(bw) for (jobname, bw) in bw_summary['write']]
        write_bw_str = 'write_bw,' + ','.join(write_bw) + '\r\n'
        fd.write(write_bw_str)

        write_iops = [str(iops) for (jobname, iops) in iops_summary['write']]
        write_iops_str = 'write_iops,' + ','.join(write_iops) + '\r\n'
        fd.write(write_iops_str)

        write_latency = [str(latency/1000000.0) for (jobname, latency) in latency_summary['write']]
        write_latency_str = 'write_lat,' + ','.join(write_latency) + '\r\n'
        fd.write(write_latency_str)

        read_bw = [str(bw) for (jobname, bw) in bw_summary['read']]
        read_bw_str = 'read_bw,' + ','.join(read_bw) + '\r\n'
        fd.write(read_bw_str)

        read_iops = [str(iops) for (jobname, iops) in iops_summary['read']]
        read_iops_str = 'read_iops,' + ','.join(read_iops) + '\r\n'
        fd.write(read_iops_str)

        read_latency = [str(latency/1000000.0) for (jobname, latency) in latency_summary['read']]
        read_latency_str = 'read_lat,' + ','.join(read_latency) + '\r\n'
        fd.write(read_latency_str)
        

def main():
    argv = sys.argv[1:]
    print argv
    if len(argv) < 1:
        print '%s filename' % sys.argv[0]
        exit(-1)
    filename = argv[0]
    parse(filename)

    
if __name__ == "__main__":
    main()
