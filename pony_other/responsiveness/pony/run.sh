#/bin/bash

~/ponyc/build/release/ponyc
output="14orca.log"
rm $output

/usr/bin/time -o temp.txt \
  ./pony 64 64000 14 14 --ponythreads=64 | python massage.py >> $output

