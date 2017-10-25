## Introduction

Code repository for the 'For Amusement Purposes Only' project.

## Hardware installation

Install the P-ROC board into the Williams Funhouse pinball machine. For now, unplug the speakers from the driver board. Connect USB cable to host computer (currently OSX)

## Prerequisite Software 

Make sure Python 2.7 in installed on the machine.

Install the libraries in this guide: 
 - up to step 13
 - make sure you git clone pyprocgame, not just download the zip!
 - something else to make it work (with one of the cmake's?)
 - http://skeletongame.com/step-1-alternate-manual-installation-for-osxlinux/
  

 If using OS X 10.11+, make sure you see the answer to this post about Apple Integrity Protection for errors relating to importing .dylib libraries:
 https://stackoverflow.com/questions/31343299/mysql-improperly-configured-reason-unsafe-use-of-relative-path


Make a config.yaml file in a '.pyprocgam' folder in your home directory 

``` 
mkdir ~/.pyprocgame
cd ~/.pyprocgame
```

config will look like this:

``` 
font_path:
    - .
    - ~/FAPO/dmd
#pinproc_class: procgame.fakepinproc.FakePinPROC
config_path:
    - ~/PROC/config
keyboard_switch_map:
    # Enter, Up, Down, Exit
    7: SD8
    8: SD7
    9: SD6
    0: SD5
    # Start:
    s: S13
    z: SF4
    /: SF2
desktop_dmd_scale: 2
dmd_cache_path: ~/.pyprocgame/dmd_cache
```



## Installation

- Clone this repository to a working directory (e.g ~/FAPO/)



## Running the Software

Power on the computer and plug in the USB cable. Then turn on the pinball table (switch is underneath)

1. Open up the terminal 
 - cmd + space
 - type `Terminal`
 - hit enter

2. If using OS X, configure the USB drivers in terminal (needs to be done after every reboot):
``` 
sudo kextunload -bundle-id com.apple.driver.AppleUSBFTDI 
```

- to undo this: 
```
sudo kextload -bundle-id com.apple.driver.AppleUSBFTDI
```

3. Navigate to working directory:
```
cd ~/FAPO
```

4. Pull any new updates:
```
git pull
```

5. Run the program:
```
python FapoGame.py
```

## Troubleshooting

xxx