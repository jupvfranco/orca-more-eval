#/bin/bash

../../../ponies/my-pony/build/release/ponyc --pic

output="responsiveness_orca.log"
rm $output

/usr/bin/time -o temp.txt \
  ./serverSim 64 64000 8 8 --ponythreads=64 --ponynoblock | python massage.py >> $output

