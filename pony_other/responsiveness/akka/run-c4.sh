#/bin/bash

scalac *.scala
echo "Akka with C4"
output="akka$1.c4.log"
rm $output

/usr/bin/time -o temp.txt \
  env JAVA_OPTS="-Xmx2g -Xloggc:gc.c4.$1.log -XX:+PrintGCDetails -Xms2G -Xmx2G" \
  scala Main 64 64000 $1 $1 | python massage.py  >> $output

