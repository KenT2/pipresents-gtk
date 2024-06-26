# PI PRESENTS  - Version 1.6.1 (GTK)

## WARNING: pipresesents-gtk currently has a bug which causes the mpv based videoplayer to crash after a number of tracks are played. See Issue #3. I am working to fix it but it might take a while, sorry.

pipresents-gtk is a major rewrite of the internals of Pi Presents to make it compatible with Raspberry Pi Model 5 and with the Wayland Desktop environment introduced in RPI OS Bookworm.

Other changes have been made to remove unsupported software and I have also tidied up some of the profile fields that have grown like topsy over the 10 years of Pi Presents development.

* X11 replaced by Wayland 
* Tkinter and PIL replaced by GTK4
 
* RPI.GPIO replaced by GPIOZero
 
* Chrome web browser replaced by Webkit browser engine
 
* mplayer based audio player removed. MPV video player now plays audio

GTK runs on a RPi5 or RPi4 under Bookworm using the Wayland Desktop Environment.

To use GPIO on a RPi model 5 the GPIOZero I/O plugin must be used. This plugin will work with any model of RPi.


# TO INSTALL PIPRESENTS-GTK

Read the 'Installing Pi Presents GTK' section below.


# TO UPGRADE FROM EARLIER VERSIONS OF PIPRESENTS KMS, BEEP, OR GAPLESS

Read the 'Updating Pi Presents from Pi Presents KMS, Beep or Gapless' section below.


# WHAT IS PI PRESENTS

Pi Presents is a toolkit for producing interactive multimedia applications for museums, visitor centres, and more.

There are a number of Digital Signage solutions for the Raspberry Pi which are often browser based, limited to slideshows, non-interactive, and driven from a central server enabling the content to be modified frequently.

Pi Presents is different, it is stand alone, multi-media, highly interactive, diverse in its set of control paradigms – slideshow, cursor controlled menu, radio button, and hyperlinked shows, and able to interface with users or machines over several types of interface. It is aimed primarly at curated applications in museums, science centres, and visitor centres.

Being so flexible Pi Presents needs to be configured for your application. This is achieved using a simple to use graphical editor and needs no Python programming. There are numerous tutorial examples and a comprehensive manual.

For a detailed list of applications and features see here:

    https://pipresents.wordpress.com/features

## Licence

See the licence.md file. Pi Presents is Careware to help support a small museum charity http://www.museumoftechnology.org.uk  Particularly if you are using Pi Presents in a profit making situation a donation would be appreciated.


# INSTALLING PI PRESENTS GTK

The instructions here assume the user is pi

The full manual in English is here https://github.com/KenT2/pipresents-gtk/blob/master/manual.pdf. It will be downloaded with Pi Presents.


## Requirements

* must use the latest version of 32 bit RPi OS Bookworm with Desktop, (not the Lite version)
* must be run from the PIXEL desktop.
* can be installed and run from any user that is created with RPi OS utilities
* should use a clean install of RPi OS, particularly if you intend to use GPIO

## Install RPi OS Bookworm

Image a SD Card with RPi OS Bookworm with desktop (32 Bit).

Ensure the OS is up to date:

         sudo apt update
         sudo apt full-upgrade


## Install required packages 

         sudo apt install libgtk-4-dev
         sudo apt install libwebkitgtk-6.0-dev
         sudo apt install python3-mpv
         sudo apt install python3-pymediainfo
         sudo apt install mpg123         

## Download Pi Presents GTK

**THE GUI WAY**

* Using a browser go to https://github.com/KenT2/pipresents-gtk
* Click the green CODE button and Download ZIP
* There should now be a file 'pipresents-gtk-master.zip' in your /downloads directory. Unzip the file and copy the directory to /home. Rename it to pipresents

**THE COMMAND LINE WAY**

From a terminal window open in your home directory type:

    wget https://github.com/KenT2/pipresents-gtk/tarball/master -O - | tar xz     # -O is a capital Ohhh...

There should now be a directory 'KenT2-pipresents-gtk-master' in your /home/pi directory. Copy or rename the directory to pipresents

## Running Pi Presents GTK

Run Pi Presents to check the installation is successful. From a terminal window opened in the pipresents directory type:

    python pipresents.py

You will see a window with an error message which is because you have no profiles. Click OK to exit Pi Presents.


## Download the Example Profiles

Examples are in the github repository pipresents-gtk-examples.

**THE GUI WAY**

* Using a browser go to https://github.com/KenT2/pipresents-gtk-examples
* Click the green CODE button and Download ZIP
* There should now be a file pipresents-gtk-examples-master.zip' in your /downloads directory. Unzip the file and copy the directory /pp_home to /home/pi.

**THE COMMAND LINE WAY**

Open a terminal window in your home directory and type:

     wget https://github.com/KenT2/pipresents-gtk-examples/tarball/master -O - | tar xz

There should now be a directory 'KenT2-pipresents-gtk-examples-master' in the /home/pi directory. Open the directory and copy the 'pp_home' directory and its contents to the home directory /home/pi.

## Running an Example Profile

From a terminal window opened in the pipresents directory type:

    python pipresents.py -p pp_mediashow_1p6
 
to see a repeating multimedia show

Exit this with CTRL-BREAK or closing the window, then:

    python pipresents.py -p pp_mediashow_1p6 -f
 
to display it full screen

Now read the manual to try other examples.


# UPDATING PI PRESENTS FROM PI PRESENTS KMS, BEEP OR GAPLESS

Backup the directories /home/pi/pipresents and /home/pi/pp_home. You will need to copy some of the files to the new SD card.

Pi Presents GTK requires Raspberry Pi OS Bookworm so first install the operating system on a new SD card and then follow the instructions above for a new install of Pi Presents GTK.

Now modify the following:

## .cfg files in pipresents/pp_config

Do not copy across pp_audio.cfg, pp_display.cfg, or pp_editor.cfg

If you have modified it, make the edits to pp_web.cfg. If you are using a username other than pi then edit the appropriate fields.

Copy any other files you have changed in pp_config, - pp_email.cfg, pp_oscmonitor.cfg, pp_oscremote.cfg


## .cfg files that are in /pipresents/pp_io_config or in a profile 

If using a Pi5 you must replace gpio.cfg with a .cfg file based on /pipresents/pp_resources/pp_templates/gpiozero.cfg. The fields differ considerably from earlier versions and you will need edit the file. It is recommended you do this for earlier models of RPi as gpio.cfg is end of life.

Minor changes have been made to keys.cfg and keys_plus.cfg but these are backwards compatible, if you have changed them copy them across and maybe edit them. Instructions in manual and /pp_templates.

Copy any other files you have made or changed from the old to new /pipresents/pp_io_config directory.

## I/O plugins in /pipresents/pp_io_plugins

Copy any files you have made or changed from the old to new /pipresents/pp_io_plugins directory. If you have timers in you plugin you will need to edit the code to move from Tkinter to GTK4

## track_plugins in /pipresents/pp_track_plugins or in a profile 

Copy any files you have made or changed from the old to new /pipresents/pp_track_plugins directory. You will need to edit the code to move from Tkinter to GTK4



# Updating Profiles for use in Pi Presents GTK

Copy the /pp_home directory from your backup to the /home/pi directory of your SD card.

When you open a profile using the editor it will be updated from KMS, Beep or Gapless versions. You can use the update>update_all menu option of the editor to update all the profiles in a single directory at once.

You will now need to make the following manual modifications:

* Video tracks using omxplayer are now removed and will be deleted from the profile by the update. Any reference to them will be retained.  You will need to create new equivalent tracks using the MPV Video track.

* VLC Video tracks using VLC Player are now removed and will be deleted from the profile by the update. Any reference to them will be retained.  You will need to create new equivalent tracks using the MPV Video/Audio track. 

* Audio tracks using mplayer are now removed and will be deleted from the profile by the update. Any reference to them will be retained.  You will need to create new equivalent tracks using the MPV Video/Audio track. 

* Web tracks that used the UZBL browser are now removed and will be deleted from the profile by the update. Any reference to them will be retained. You will need to create new equivalent tracks using the Chrome Web track.
 
* Chrome Web tracks that used the chromium browser are now removed and will be deleted from the profile by the update. Any reference to them will be retained. You will need to create new equivalent tracks using the Chrome Web track.

* For MPV video/audio tracks the Audio Volume range is now 0>100 instead of -60>0
      
* Videoplayout has changed yet again, back to its original method. See manual and pp_videoplayout_1p6 example

      
To help with replacing the removed tracks there are two features:

* In the Editor, profile>validate will display errors for any track references that are to the removed tracks. 
      
* In the Editor, show>view backup will show the parameters for the show and of all tracks in the associated medialist. This allows identification of removed anonymous tracks. The backup was made when the profile issue was last updated.
      
* The format of the backup parameters display allows cut and paste of field content, particulary multi-line fields. The data is taken from /pp_home/pp_profiles.bak and uses the internal names for the fields, these are close to the names displayed by the editor except 'controls' which sometimes is displayed as 'links'


### CONFIGURATION /pp_config

pp_display.cfg, display position is not required and will be ignored.

pp_display.cfg, in develop window x,y is now not used but must be present.


### I/O PLUGINS

If using RPi5 the gpiozero.cfg file must be used instead of gpio.cfg. It is recommended that it also used for earlier models.The fields in gpiozero.cfg differ from gpio.cfg, see manual and /pi_resources/pp_templates/gpiozero.cfg for details.

The Keyboard I/O plugins have been rewritten for GTK4.In keys.cfg and keys_plus.cfg, <> is optional, CTRL-F4 is now F4

osmcremote.cfg I/O plugin not required for remote controls, use keys.cfg


### SHOWS

In all shows, in the track defaults tab, player windows and aspect mode are modified as in Tracks.

In mediashow, input-persist has been removed. Use freeze at start>after_first_frame as in pp_videoplayout_1p6


### ALL TRACKS

Removed the HDMI value in the Display field, use HDMI0 instead

html text fields - links to resources must be full paths not relative

The background image is fill'ed to fit the show canvas

Player windows, removed the x1 y1 x2 y2 format. Values are now fullscreen, x+y+w\*h, or w\*h. See manual.

Font format changed to bold italic 20pt helvetica from helvetica 20 bold italic

Colour fields cannot be blank

Colour field values can be a 6 figure hex number, an 8 figure providing opacity, or transparent


### AUDIO TRACKS

The Audio Tracks player implemented by mplayer has been removed. MPV video/audio tracks now play audio.

Audio tracks are removed when updating the profile


### MPV VIDEO/AUDIO TRACKS

Tracks now have MPV Speaker field and 5.1 value

Tracks now have a Alternate Video Display field for video playout on a different display

Changed hdmi0, hdmi1 to HDMI0, HDMI1 in the MPV Player Audio field

Aspect mode is now clip, fit, warp, or shrink. original value is deleted

Remove showcanvas/display from MPV window field. Window is now always referenced to show canvas


### IMAGE TRACKS

Aspect mode removed from image window field to a seperate aspect mode field

Aspect mode is now clip, fit, warp, or shrink. original value is deleted

Image window is referenced to show canvas not display

Removed rotation field


### WEB TRACKS

Web tracks are now implemented by the Webkit browser engine instead of Chrome

Chrome web track entries are removed when updating profiles

Removed window type from web window


### MENU TRACKS

menu window should be x+y+w\*h, the w\*h element is used only for the bounding box. See manual

menu window is referenced to show canvas it is not centred but is controlled by x,y.


### DUMMY TRACKS

Instead of the audio track, message tracks or image tracks can be a dummy track


### CLICK AREAS

In screen.cfg image width and height are not required. They will be ignored

In screen.cfg fill and outline colour fields must have a value. Colour field values can be transparent, a 6 figure hex number, or an 8 figure providing opacity.

In screen .cfg font font format changed to bold italic 20pt helvetica from helvetica 20 bold italic

### MISC

Installing unclutter is not required. The cursor is removed in fullscreen mode (-f) except if -c command line option is used.

The -b command line option to control blanking is removed. Raspberry Pi Configuration menu now controls blanking

Method to run Pi Presents with no monitor attached has changed. Use the NODISPLAY display instead of selecting A/V.

Autostart methid has changed to editing wayfire.ini. See manual


# Bug Reports and Feature Requests

I am keen to develop Pi Presents further and would welcome bug reports and ideas for additional features and uses.

Please use the Issues tab on Github https://github.com/KenT2/pipresents-gtk/issues or contact me on https://pipresents.wordpress.com/

For more information on how Pi Presents is being used, Hints and Tips on how to use it and all the latest news hop over to the Pi Presents website https://pipresents.wordpress.com/

