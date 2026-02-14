
#PREPARING THE TRIXIE AUTOSTART FILE
#Autostart will function only if you have set 'boot to desktop' using raspi-config.

# The directory .config is already present in the image but you will need to select 'Show
# Hidden Files' in the File Manager to see it.

# For Trixie the autostart file:
#   /home/pi/.config/lxsession/rpd-x/autostart
#  does not exist so it, or its contents, needs to be copied from the file:
#   etc/xdg/lxsession/rpd-x/autostart

# then edit the file
#   /home/pi/.config/lxsession/rpd-x/autostart
# Add the following line below the last line to start Pi Presents with the required
# options:
#   /home/pi/pipresents/autostart.sh

# Note: the autostart file is not a standard .sh file. The leading @ is not required, it
# means restart the process should it fail.

# EDITING THIS FILE
# edit this file to the required profile and options
# Ensure this file, autostart.sh is executable

/usr/bin/python /home/pi/pipresents/pipresents.py -o /home/pi -p pp_mediashow_1p6

# to help the debug of PP when using autostart use this line instead.

#/usr/bin/python /home/pi/pipresents/pipresents.py -p pp_mediashow_1p5 -d -o /home/pi  >> /home/pi/pipresents/pp_logs/pp_autostart.txt 2>&1

