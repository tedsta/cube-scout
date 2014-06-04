#!/usr/bin/env sh

name="$1"

notify-send $name "is entering the cubicle"

if [ "$name" = "scott" ]; then
    xdotool key alt+w
    xdotool key alt+4
    xdotool key alt+e
    xdotool key alt+5
fi
