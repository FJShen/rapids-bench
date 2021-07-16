#!/bin/bash

source setup_env.sh
export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS} -Xcomp"
python3 "$@" > out.txt 2>&1