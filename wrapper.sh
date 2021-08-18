#!/bin/bash

source setup_env.sh
export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS} "
python3 "$@"