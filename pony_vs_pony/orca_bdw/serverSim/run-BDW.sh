#/bin/bash

../../../ponies/pony-bdw/build/release/ponyc --pic
export GC_INITIAL_HEAP_SIZE=4000000000

echo "("$GC_MAXIMUM_HEAP_SIZE","$GC_INITIAL_HEAP_SIZE$")"
export GC_NPROCS=64
export GC_MARKERS=64

output="responsiveness_bdw.log"
rm $output

/usr/bin/time -o temp.txt \
  ./serverSim 64 64000 8 8 --ponythreads=64 --ponynoblock | python massage.py >> $output

