## Introduction

Code repository for the 'For Amusement Purposes Only' project.

## Hardware installation

Install the P-ROC board into the Williams Funhouse pinball machine. For now, unplug the speakers from the driver board. Connect USB cable to host computer (currently OSX)

## Prerequisite Software 

Make sure Python 2.7 in installed on the machine.

Also downloading and installing MIDI monitor is very helpful:
https://www.snoize.com/MIDIMonitor/

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

## Configuring Midi

1. Open `~/FAPO/GameConfig.py` in any text editor (Sublime preferred)


- changing values from `True` to `False` or vica versa, must have a captial first letter (e.g `True` not `true`, `False` not `false`)
- leave `self.inputKeyboardTest = True` for now
- to enable/disable the USB Novation Launchpad controlling the lights, change the `self.inputLaunchpadTest` value. If `self.inputLaunchpadTest = True`, the machine will not accept midi light signals from MAX so set to False if you aren't using the Launchpad.
- if you want the test to Toggle lights rather than turn them on while the corresponding button is pressed, change  self.lampToggle to equal False.

2. The next three values determine which MIDI Ports the software is using to talk with MAX. If you open MIDI Monitor and expand the 'MIDI Sources' option in the 'Sources' pane, you can view which MIDI ports are in the machine. The numbering counts from 0 (so the first port is 0, the second port is 1, etc.)

These numbers correspond to the input/output variables in the config file.

- `self.inputMidiSolenoids` is the port that waits for MIDI signals to control the solenoids/coils in the pinball table. If you look at the `self.midiKeyboardMap` variable, you can see the mapping between the MIDI note and which solenoid it triggers (e.g. MIDI Note 48 triggers Solenoid C01 Outhole). WARNING: DO NOT CONTINUALLY LEAVE A SOLENOID ON BECAUSE IT WILL BURN OUT AND EXPLODE

- `self.inputMidiLamps` is the port that waits for MIDI signals to control the lights. The notes are mapped to the lamp matrix in the pinball manual. So MIDI note 11 will light lamp L11 (Gangway 75,000 left) and MIDI note 37 will light lamp L37 (Clock 11 o'clock). Will the MIDI signal is on the lamp will stay lit until the signal sends the off trigger. 

- `self.outputMidiSwitches` is the port that sends MIDI whenever a switch is activated or deactivated on the pinball machine on channel 1 and channel 2, respectively.

3. Save and close the file. If the software is running, stop (CTRL + C) and restart it.

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

### Shutting down

1. Stop the software by clicking on the Terminal window and pressing CTRL + C

2. Turn off the machine

3. Unplug the USB cable

## Troubleshooting

xxx