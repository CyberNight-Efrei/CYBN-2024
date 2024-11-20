#!/bin/bash

while :
do
  # run python app.py
  socat TCP-LISTEN:1001,reuseaddr,fork EXEC:'/app/app.py,stderr'
done