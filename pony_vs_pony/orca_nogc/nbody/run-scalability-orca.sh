rm trees
../../../ponies/my-pony/build/release/ponyc --pic  

logfile="orca.scalability.log"
rm $logfile

repetition=10
corecount=4
while [ $corecount -le 64 ]
do 
  i=1
  while [ $i -le $repetition ]
  do
    /usr/bin/time -f "%e" -o "tmp" ./nbody 0 50 500 --ponythreads=$corecount --ponynoblock > /dev/null 
    t=$(cat tmp) >> $logfile
    echo $corecount" cores :: iteration "$i" :: "$t >> $logfile
    i=$[$i+1]
  done
  corecount=$[$corecount + $corecount]
done

rm tmp
