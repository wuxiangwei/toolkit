#!/bin/bash

rm -rf t1.log t2.log t3.log t3.csv
# cat xw_iops.1.log | awk -F , '{print $2}' > t1.log
cat xw_clat.1.log | awk -F , '{print $2}' > t1.log
cat peering_count.log | awk -F , '{print $2","$3}' > t2.log

paste -d , t1.log t2.log > t3.csv
