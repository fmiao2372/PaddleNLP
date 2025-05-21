#!/bin/bash
ps aux | egrep -i "paddle|spawn_main|triton" | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
