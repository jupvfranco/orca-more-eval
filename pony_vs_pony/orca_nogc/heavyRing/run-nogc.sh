#!/bin/bash

rm heavyRing
../../../ponies/my-pony/build/release-nogc/ponyc --pic

logfile="nogc.log"
rm $logfile

repetition=10
size=4
while [ $size -le 16 ]
do 
  i=1
  while [ $i -le $repetition ]
  do
    numactl -C "0,8,16,24" \
      /usr/bin/time -f "%e %M" -o "tmp" \
      ./heavyRing 64 $size 10  \
      --ponynoblock --ponythreads=1  
    t=$(cat tmp) >> $logfile
    echo "size "$size" :: iteration "$i" :: "$t >> $logfile
    i=$[$i+1]
  done
  size=$[$size + 4]
done

rm tmp
