#/bin/bash

scalac *.scala
echo "Akka with Parallel"
output="akka14.parallel.log"
rm $output

/usr/bin/time -o temp.txt \
  env JAVA_OPTS="-XX:+UseParallelGC -Xloggc:parallelgc.log -XX:+PrintGCDetails -Xms2G -Xmx2G" \
  scala Main 64 64000 14 14 | python massage.py >> $output

