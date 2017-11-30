#!/usr/bin/env sh

: "${TIMEOUT:=5}"

while true
do
	python remove_terminated_instances.py
	echo "Run once in $TIMEOUT seconds"
	sleep "$TIMEOUT"
done
