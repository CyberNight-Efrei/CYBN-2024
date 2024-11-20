#!/bin/bash

while :
do
  # run python app.py
  su -c "exec socat TCP-LISTEN:1001,reuseaddr,fork EXEC:'/challenge/challenge.py,stderr'" - challenge;
done