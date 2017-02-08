Title: `xrandr` Script to Setup External Monitor
Author: Tim Henderson
Date: 2017-02-08
Category: Blog

I have a quirky adapter for my external monitor. The adapter doesn't correctly
report the display's size or refresh rate to the laptop. To solve this problem,
I wrote the following script to automatically setup the external monitor:

```bash
#!/usr/bin/env bash

## size and refresh rate of the screen
X=1920
Y=1200
R=60

## mode string
MODE="$X"x"$Y"_"$R".00

## turn the output off in case it is on
xrandr --output DP1 --off

## delete the mode from the output in case it exists
xrandr --delmode DP1 "$MODE"

## delete the mode
xrandr --rmmode "$MODE"

## create the mode, you need to compute the actual mode line using the `gtf`
## program which computes VESA GTF mode lines from size and refresh rates
gtf $X $Y $R | grep Modeline | sed 's/ *Modeline *//' | xargs xrandr --newmode

## add your newly created mode to the output
xrandr --addmode DP1 "$MODE"

## turn on the output with the new mode. Place it to the right of the laptop
## display but displaced -600 pixels above the laptop display
xrandr --output DP1 --mode $MODE --pos 1920x-600
```

This script also has the advantage that I never have to run the GUI tool to
change the position of the monitor in relationship to my laptop's monitor.

