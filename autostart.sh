# include this script file in $HOME/.config/wayfire.ini. See manual.
# make autostart.sh executable first
python /home/pp/pipresents-gtk-dev/pipresents.py -p 1p6/pp_mediashow_1p6

# to debug autostart use this instead 
#python $HOME/pipresents-gtk/pipresents.py -p pp_mediashow_1p6 -d >> $HOME/pipresents-gtk/pp_logs/pp_autostart.txt 2>&1

# to inhibit all error messages and warnings
#GTK_A11Y=none python $HOME/pipresents-gtk/pipresents.py -p pp_mediashow_1p6 2>/dev/null
