#!/usr/bin/bash

K6_SCRIPT=$1;
TAG=$2;
k6 run $1 > k6out_$TAG.txt &
pid=$!
echo $pid

echo > logs/ens5.txt
echo > logs/nvme0n1.txt
echo > logs/pidstat.txt
elapsed=0

while kill -0 $pid 2> /dev/null; do
    echo "Elapsed $elapsed s."
    elapsed=$(($elapsed + 1))
    iostat  -p nvme0n1 | awk 'NR==7||NR==8||NR==9{print}'  >> logs/nvme0n1_$TAG.txt
    pidstat  -p $(pidof terrad) | tail -n 1  >>  logs/pidstat_$TAG.txt
    vmstat  -w -S M   >>  logs/vmstat_$TAG.txt
    sar -n DEV  1 1 | awk 'NR==5 {print}' >> logs/ens5_$TAG.txt
done

#-⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈[ Network ]┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯
sudo iftop -t  -s 1 | awk 'NR==10||NR==11||NR==12{print}'
# 