## Introduction

Code repository for the **For Amusement Purposes Only** project.

## Hardware installation

Install the P-ROC board into the Williams Funhouse pinball machine. Connect USB cable to host computer (currently OSX)

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

```mkdir ~/.pyprocgame
cd ~/.pyprocgame```

config will look like this:

```font_path:
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
dmd_cache_path: ~/.pyprocgame/dmd_cache```



## Installation

- Clone this repository to a working directory (e.g ~/FAPO/)


## Running the Software

1. Open up the terminal 
... - cmd + space
... - type `Terminal`
... - hit enter

2.  


## Troubleshooting

xxx