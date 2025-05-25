#!/bin/bash

wifi=$(nmcli -t -f TYPE,STATE device | grep '^wifi:connected')
eth=$(nmcli -t -f TYPE,STATE device | grep '^ethernet:connected')

if [ -n "$wifi" ]; then
    echo ""

elif [ -n "$eth" ]; then
    echo "󰌗"

else
    echo ""
fi