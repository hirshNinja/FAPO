## Introduction

Code repository for the 'For Amusement Purposes Only' project.

## Hardware installation

Install the P-ROC board into the Williams Funhouse pinball machine. For now, unplug the speakers from the driver board. Connect USB cable to host computer (currently OSX)

## Prerequisite Software 

1. Make sure Python 2.7 in installed on the machine.

2. Also downloading and installing MIDI monitor is very helpful:
https://www.snoize.com/MIDIMonitor/

3. Install the libraries in this guide: 
 - up to step 13
 - make sure you git clone pyprocgame, not just download the zip!
 - something else to make it work (with one of the cmake's?)
 - http://skeletongame.com/step-1-alternate-manual-installation-for-osxlinux/
  

 4. If using OS X 10.11+, make sure you see the answer to this post about Apple Integrity Protection for errors relating to importing .dylib libraries:
 https://stackoverflow.com/questions/31343299/mysql-improperly-configured-reason-unsafe-use-of-relative-path


5. Make a config.yaml file in a '.pyprocgam' folder in your home directory 

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

## Configuring MIDI

1. Open `~/FAPO/MidiConfig.py` or `HOMEDIRECTORY/FAPO/MidiConfig.pg` in any text editor (Sublime preferred)


- changing values from `True` to `False` or vica versa, must have a captial first letter (e.g `True` not `true`, `False` not `false`)
- leave `self.inputKeyboardTest = True` for now
- to enable/disable the USB Novation Launchpad controlling the lights, change the `self.inputLaunchpadTest` value. If `self.inputLaunchpadTest = True`, the machine will not accept midi light signals from MAX so set to `False` if you aren't using the Launchpad.
- if you want the test to Toggle lights rather than turn them on while the corresponding button is pressed, change  `self.lampToggle` to equal `False`.

2. The next three values determine which MIDI Ports the software is using to talk with MAX. If you open MIDI Monitor and expand the 'MIDI Sources' option in the 'Sources' pane, you can view which MIDI ports are in the machine. The numbering counts from 0 (so the first port is 0, the second port is 1, etc.)

These numbers correspond to the input/output variables in the config file.

- `self.inputMidiSolenoids` is the port that waits for MIDI signals to control the solenoids/coils in the pinball table. If you look at the `self.midiKeyboardMap` variable, you can see the mapping between the MIDI note and which solenoid it triggers (e.g. MIDI Note 48 triggers Solenoid C01 Outhole). 

<b>WARNING: DO NOT CONTINUALLY LEAVE A SOLENOID ON BECAUSE IT WILL BURN OUT AND EXPLODE</b>

- `self.inputMidiLamps` is the port that waits for MIDI signals to control the lights. The notes are mapped to the lamp matrix in the pinball manual. So MIDI note 11 will light lamp L11 (Gangway 75,000 left) and MIDI note 37 will light lamp L37 (Clock 11 o'clock). Will the MIDI signal is on the lamp will stay lit until the signal sends the off trigger. 

- `self.outputMidiSwitches` is the port that sends MIDI whenever a switch is activated or deactivated on the pinball machine on channel 1 and channel 2, respectively.

3. Save and close the file. If the software is running, stop (CTRL + C) and restart it.

## Running the Software

Power on the computer and plug in the USB cable. Then turn on the pinball table (switch is underneath)

1. Open up the terminal 
 - cmd + space
 - type `Terminal`
 - hit enter
1
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

- If you've made any changes (like to the config file) it will ask you to commit or stash first. 
- If you want to see what those are type `git diff` and take a note of them (you'll have to put them back in after updating). 
- Then type `git stash` so you can try step 4 again.
- Put back in the changes seen when entering `git diff` previously.

5. Run the program:
```
python FapoGame.py
```

### Shutting down

1. Stop the software by clicking on the Terminal window and pressing CTRL + C

2. Turn off the machine

3. Unplug the USB cable

## Troubleshooting

- If the machine stops playing or responding (e.g. no flipper control during game play), check the Terminal window to see if a crash has occured. Note down the error log (usually the last 4 or 5 lines), sink any balls on the playfield or plungers, then you can rerun the program again by following step 5 or hitting the 'up' arrow then Enter.

- `IOError: Unable to open ftdi device: -3: device not found` means the computer is having trouble connecting to P-ROC. Usually this means that the pinball table isn't switched on or the USB dirvers haven't been configured as in step 2. If neither is the case, switch off the machine reconnect and turn it back on and it should work. Another possibility is the fourth line of the 'config.yaml' file (from installation step 5)  `#pinproc_class: procgame.fakepinproc.FakePinPROC` has the hash symbol missing from the front. 