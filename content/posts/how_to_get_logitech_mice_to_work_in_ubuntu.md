---
title: "How to get Logitech mice to work in Ubuntu"
date: 2006-04-02T10:25:24-04:00
slug: "how_to_get_logitech_mice_to_work_in_ubuntu"
url: /2006/04/02/how_to_get_logitech_mice_to_work_in_ubuntu/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-04"]
categories:
  - "linux"
tags: []
aliases:
  - "/2006/04/02/how_to_get_logitech_mice_to_work_in_ubuntu/feed/"
---

Most Logitech mice are connected via USB, and I have not tested this with PS/2 mice.

Open xorg.conf

`sudo gedit /etc/X11/xorg.conf`

Now find the section that says something like:

`Section "InputDevice"  
Identifier "Mouse"  
Driver "mouse"  
Option "CorePointer"  
Option "Device" "/dev/input/mice"  
Option "Protocol" "ImPS/2"  
Option "Emulate3Buttons" "true"  
Option "ZAxisMapping" "4 5"  
Option "Buttons" "7"  
EndSection`

and comment it out by putting a # symbol in front of each line. It should look like this:

`#Section "InputDevice"  
# Identifier "Mouse"  
# Driver "mouse"  
# Option "CorePointer"  
# Option "Device" "/dev/input/mice"  
# Option "Protocol" "ImPS/2"  
# Option "Emulate3Buttons" "true"  
# Option "ZAxisMapping" "4 5"  
# Option "Buttons" "7"  
#EndSection`

Now make some space under or above that section and paste in the following:

`Section "InputDevice"  
Identifier "Mouse"  
Driver "mouse"  
Option "Protocol" "evdev"  
Option "Dev Name" "Logitech USB-PS/2 Optical Mouse"  
Option "Dev Phys" "usb-*/input0"  
Option "Device" "/dev/input/event2"  
Option "Buttons" "10"  
Option "ZAxisMapping" "4 5"  
EndSection`

Save the file and restart the X server by pressing Ctrl+Alt+Backspace.

Note: If the X server fails to start, use the command “sudo cp /etc/X11/xorg.conf.backup /etc/X11/xorg.conf” to restore your original settings.

After the X server is restarted and your mouse is still working, you have to edit the .Xmodmap file.

`sudo gedit ~/.Xmodmap`

Paste the line “pointer = 1 2 3 6 7 8 9 10 4 5” without quotes in this file. If there’s already a “pointer” section, overwrite it.

Now run xmodmap to apply the settings:

`xmodmap ~/.Xmodmap`

Now to get the side buttons working in Nautilus and Firefox. Install xvkbd and xbindkeys with:

`sudo apt-get install xvkbd xbindkeys`

Create a configuration file for these new program by:

`gedit ~/.xbindkeysrc`

Paste the following into that file, then save and exit:

`"/usr/X11R6/bin/xvkbd -xsendevent -text "[Alt_L][Left]""  
m:0x0 + b:6  
"/usr/X11R6/bin/xvkbd -xsendevent -text "[Alt_L][Right]""  
m:0x0 + b:7`

Now add this program to you session by adding it to “System > Preferences > Sessions”. Click on the “Startup Programs” tab and click “Add” and enter “xbindkeys”. This makes sure that everytime you log in, your setting are loaded.

Install the logitech applet (not really an applet by the way) by:

`sudo apt-get install checkinstall build-essential libusb-dev  
wget http://freshmeat.net/redir/logitech_applet/53319/url_tgz/logitech_applet-0.4test1.tar.gz  
tar xvfz logitech_applet-0.4test1.tar.gz  
mv ./logitech_applet-0.4test1 ./logitech-applet-0.4test1  
cd ./logitech-applet-0.4test1  
./configure --prefix=/usr  
make  
sudo checkinstall`

Just hit enter when checkinstall prompts you. Everything should now be installed.

Use the command:

`sudo logitech_applet -s 800 -e`

This sets you mouse at optimum resolution. You might have to adjust the mouse setting in Gnome as the mouse will be much more accurate now. Go to “System > Preferences > Mouse” and adjust the settings to your liking.

Now to make all this load at boot time. Make a file in /etc/init.d/local to keep local settings.

`sudo gedit /etc/init.d/local`

Paste this into the file, save, and exit:

`echo "Setting up Logitech mouse..."  
logitech_applet -s 800 -e`

Make that file executable by:

`sudo chmod 755 /etc/init.d/local`

Now run the following command to make the “local” script run when the system boots:

`sudo update-rc.d local defaults`

Now you should have a fully working Logitech USB mouse in Ubuntu.
