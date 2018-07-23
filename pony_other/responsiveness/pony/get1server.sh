#/bin/bash

# Run benchmark with a smaller workload and record results of 
# what's happening in the actor attached to core 32. 

~/thesis-evaluation/ponies/my-pony/build/release/ponyc --pic
output="linear.log"
rm $output

numactl -C "0-63" ./pony 64 250 14 14 --ponythreads=64 --ponynoblock | grep "(32" >> $output

