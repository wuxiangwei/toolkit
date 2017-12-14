#!/bin/bash

MAX_COUNT=1

for i in `seq 1 $MAX_COUNT`; do
    echo $i
    echo "begin to stop osds"
    ceph -s
    sleep 900
    sudo /etc/init.d/ceph stop osd
    sleep 1800
    sudo /etc/init.d/ceph start osd
    sleep 600
    echo $i >> test.log
    date >> test.log
    echo "Finished to start all osds" >> test.log
    ceph -s >> test.log
    ceph osd tree >> test.log
    echo "===================================================\r\n" >> test.log
done
