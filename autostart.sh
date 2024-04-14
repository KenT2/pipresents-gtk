# include reference to this script file in /home/pi/.config/wayfire.ini. See manual.
# make this file (autostart.sh) executable

# set the current working directory ($PWD)
cd /home/pi/pipresents

# to run a pipresents profile
python $PWD/pipresents.py -p pp_mediashow_1p6

# to debug autostart use this instead 
#python $PWD/pipresents.py -p pp_DRV2605_1p6 -d >> $PWD/pp_logs/pp_autostart.txt 2>&1

# to inhibit all error messages and warnings
#GTK_A11Y=none python $PWD/pipresents.py -p pp_mediashow_1p6 2>/dev/null

#to run Pi Presents from a virtual environment called venv
#$PWD/venv/bin/python3 $PWD/pipresents.py -p pp_DRV2605_1p6
