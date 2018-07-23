#/bin/bash

/home/albert/github/otp-default/bin/erlc +native response.erl
output="8beam.log"
rm $output

/usr/bin/time -o temp.txt \
  /home/albert/github/otp-default/bin/erl +sbt tnnps -noshell -run \
  response main 64 64000 8 8 -s init stop \
  | python massage.py >> $output

