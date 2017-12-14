#!/usr/bin/env python
# coding=utf-8

import os
import time
import json
import subprocess


def sample():
    cmd = ['ceph', '-s', '-f', 'json']
    output = subprocess.check_output(cmd, True)
    output_js = json.loads(output)
    summaries = output_js.get('health', {}).get('summary', [])

    defer_peering_num, peering_num = 0, 0
    for summary in summaries:
        sum_string = summary['summary']
        if 'pgs defer_peering' in sum_string:
            defer_peering_num = int(sum_string.split()[0])
        elif 'pgs peering' in sum_string:
            peering_num = int(sum_string.split()[0])
    return defer_peering_num,  peering_num


def main():

    fpath = 'peering_count.log'
    if os.path.exists(fpath):
        os.remove(fpath)

    result = []
    count = 0
    while True:
        #  计算比较慢，所以降低睡眠时间
        time.sleep(.8)
        result.append(sample())
        count += 1
        if count % 500 == 0:
            lines = []
            for rs in result:
                line = '%d, %d, %d\r\n' % (count, rs[0], rs[1])
                lines.append(line)

            result = []
            with open(fpath, 'aw') as fd:
                fd.writelines(lines)

        if count > 2000:
            #  记录多余部分
            lines = []
            for rs in result:
                line = '%d, %d, %d\r\n' % (count, rs[0], rs[1])
                lines.append(line)

            with open(fpath, 'aw') as fd:
                fd.writelines(lines)
            break


if __name__ == '__main__':
    main()
