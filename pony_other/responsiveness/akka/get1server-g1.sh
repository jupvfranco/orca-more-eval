#/bin/bash

scalac *.scala
output="linear.log"
rm $output

numactl -C "0-63" env JAVA_OPTS="-XX:+UseG1GC" scala Main 64 250 14 14 | grep "(32" >> $output

