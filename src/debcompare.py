#!/usr/bin/env python
# coding:utf-8

import re
import glob
import subprocess


def parse_name(text):
    """
    解析包名
    """
    name_re = re.compile("Package: (.*)")
    mt = name_re.search(text)
    return mt.group(1)


def parse_version(text):
    """
    解析版本号
    """
    version_re = re.compile('Version: (.*)')
    mt = version_re.search(text)
    return mt.group(1)


def parse_depends(text):
    """
    解析依赖
    """
    depend_re = re.compile('Depends: (.*,)(.*\n)')
    
    ret = []
    for mt in depend_re.finditer(text):
        index = 1
        for index in xrange(1, mt.lastindex+1):
            grp_str = mt.group(index)
            deps = grp_str.split(',')
            # 剔除首尾空格
            deps = [i.strip() for i in deps]
            # 剔除空匹配
            deps = [i for i in deps if i != '']
            ret.extend(deps)
    return sorted(ret)


def parse(text):
    """
    解析包名、版本号、依赖
    """
    name = parse_name(text)
    version = parse_version(text)
    depends = parse_depends(text)
    return name, version, depends


def scan_depends_for_unistalled(path):
    """
    扫描给定路径下所有deb包的依赖
    """
    ret = []
    for pkg_path in glob.glob(path):
        cmd = ['dpkg', '-I']
        cmd.append(pkg_path)
        out = subprocess.check_output(cmd)
        ret.append(parse(out))

    return ret


def scan_depends_for_installed(names):
    """
    扫描已安装的deb的依赖
    """
    ret = []
    for nm in names:
        cmd = ['dpkg', '-s']
        cmd.append(nm)
        try:
            out = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as error:
            print '%s is not installed' % nm
            continue
        ret.append(parse(out))

    return ret


def store_result(filepath, res):
    with open(filepath, 'w') as fd:
        for name, version, depends in res:
            head = "="*60 + "\r\n"
            head += "Package: %s\r\n" % name
            head += "Version: %s\r\n\r\n" % version
            fd.write(head)
            depends = [i+'\r\n' for i in depends]
            fd.writelines(depends)


def main():
    path = '/root/ceph-debs/*.deb'

    ures_filepath = "u.o"
    ures = scan_depends_for_unistalled(path)
    store_result(ures_filepath, ures)

    names = [i[0] for i in ures]

    ires_filepath = "i.o"
    ires = scan_depends_for_installed(names)
    store_result(ires_filepath, ires)


if __name__ == '__main__':
    main()
