#!/bin/sh

make -f border-router/webserver/Makefile TARGET=cooja connect-router-cooja &

mosquitto -v &

python3 python-server/python.py


