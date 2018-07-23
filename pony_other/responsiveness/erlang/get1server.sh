#/bin/bash

#~/otp-OTP-18.3/bin/erlc response.erl
erlc +native response.erl
output="linear.log"
rm $output

numactl -C "0-63" \
erl  +sbt tnnps -noshell -run \
  response main 64 250 14 14 -s init stop | grep "(32" >> $output

