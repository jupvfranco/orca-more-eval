#/bin/bash

scalac *.scala
echo "Akka with g1gc"
output="akka8.g1gc.log"
rm $output

/usr/bin/time -o temp.txt \
  env JAVA_OPTS="-XX:+UseG1GC -Xloggc:g1gc.log -XX:+PrintGCDetails -Xms2G -Xmx2G" \
  scala Main 64 64000 8 8 | python massage.py >> $output

