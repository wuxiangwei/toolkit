#!/usr/bin/env python
# coding=utf-8

import json
import subprocess


def get_osds():
    cmd = """
        ps -ef | grep "ceph-osd" | awk '{print $10}' | grep -P "\d+" | xargs
    """
    osds_string = subprocess.check_output(cmd, shell=True)
    osds = [int(osd) for osd in osds_string.split()]
    return sorted(osds)


def main():
    osds = get_osds()
    osdnames = [ 'osd.{}'.format(osd) for osd in osds ]
    opt_name = 'osd_defer_peering'
    opt_value = 'true'

    for osdname in osdnames:
        cmd = "sudo ceph daemon %s config set %s %s" % (osdname, opt_name, opt_value)
        res_string = subprocess.check_output(cmd, shell=True)
        res = json.loads(res_string)
        print '[ OK ] ' if 'success' in res else '[ FAILED] ', 'Update %s for %s' % (opt_name, osdname)


if __name__ == '__main__':
    main()
