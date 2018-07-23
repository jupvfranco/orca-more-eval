#/bin/bash

scalac *.scala
echo "Akka with CMS"
output="akka14.cms.log"
rm $output

/usr/bin/time -o temp.txt \
  env JAVA_OPTS="-XX:+UseConcMarkSweepGC -Xloggc:cmsgc.log -XX:+PrintGCDetails -Xms2G -Xmx2G" \
  scala Main 64 64000 14 14 | python massage.py >> $output

