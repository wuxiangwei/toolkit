#!/usr/bin/env python
#coding:utf-8

import sys
import json


def parse(filename):
    # TODO: 检查filename文件是否存在
    csv_filename = filename + '.csv'

    # 读取原始文件
    result_json = None
    with open(filename, 'r') as fd:
        result_text = fd.read()
        result_json = json.loads(result_text)

    jobs = result_json['jobs']
    iops_summary = {'write': [], 'read': []}
    latency_summary = {'write': [], 'read': []}
    jobnames = []
    for job in jobs:
        jobname = job['jobname']
        jobnames.append(jobname)
        iops_summary['write'].append((jobname, job['write']['iops']))
        iops_summary['read'].append((jobname, job['read']['iops']))

        latency_summary['write'].append((jobname, job['write']['lat_ns']['mean']))
        latency_summary['read'].append((jobname, job['read']['lat_ns']['mean']))

    print jobnames
    with open(csv_filename, 'w') as fd:
        print 'write IOPS'
        write_iops = [str(iops) for (jobname, iops) in iops_summary['write']]
        write_iops_str = ','.join(write_iops)
        write_iops_str += '\r\n'
        fd.write(write_iops_str)

        print 'write Latency'
        write_latency = [str(latency/1000000.0) for (jobname, latency) in latency_summary['write']]
        write_latency_str = ','.join(write_latency)
        write_latency_str += '\r\n'
        fd.writelines(write_latency_str)

        print 'read IOPS'
        read_iops = [str(iops) for (jobname, iops) in iops_summary['read']]
        read_iops_str = ','.join(read_iops)
        read_iops_str += '\r\n'
        fd.write(read_iops_str)

        print 'read Latency'
        read_latency = [str(latency/1000000.0) for (jobname, latency) in latency_summary['read']]
        read_latency_str = ','.join(read_latency)
        read_latency_str += '\r\n'
        fd.writelines(read_latency_str)
        

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
