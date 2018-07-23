#!/bin/bash

rm heavyRing
../../../ponies/my-pony/build/release-telemetry/ponyc --pic

logfile="orca.log"
rm $logfile

repetition=10
size=10
while [ $size -le 60 ]
do 
  i=1
  while [ $i -le $repetition ]
  do
    /usr/bin/time -f "%e %M" -o "tmp" \
      ./nbody 0 $size 100  \
      --ponynoblock --ponythreads=1 \
      | grep "time_in" >> $logfile  
    t=$(cat tmp) >> $logfile
    echo "size "$size" :: iteration "$i" :: "$t >> $logfile
    i=$[$i+1]
  done
  size=$[$size + 10]
done

rm tmp
