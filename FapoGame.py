import procgame.game
import scoredisplay # blink idea
from procgame import alphanumeric
import procgame.lamps
import alphanumeric2
import auxport2
from procgame.modes import trough
import time

import pinproc
from pinproc import PinPROC
from modes import BasicMode
from modes import IdleMode
from modes import StepsMode
import rtmidi_python as rtmidi
from config import GameConfig


class FapoGame(procgame.game.GameController):
  def __init__(self, machine_type):
    super(FapoGame, self).__init__(machine_type)
    self.gameConfig = GameConfig.GameConfig()
    self.ball_start_time = 0
    self.midiMap = None
    self.midiLampMap = None
    if self.gameConfig.inputKeyboardTest:
      self.midiMap = self.gameConfig.midiKeyboardMap
    self.midiLampMap = None
    if self.gameConfig.inputLaunchpadTest:
      self.midiLampMap = self.gameConfig.midiLaunchpadMap

    self.load_config('config/funhouse.yaml')


    ### ALPHANUMERIC DISPLAY ###
    self.aux_port = auxport2.AuxPort(self)
    self.alpha_display = alphanumeric2.AlphanumericDisplay(self.aux_port)
    # self.scoredisplay = scoredisplay.AlphaScoreDisplay(self,4) # blink text

    ### MODES ###
    self.basic_mode = BasicMode.BasicMode(game=self)
    self.idle_mode = IdleMode.IdleMode(game=self)
    self.steps_mode = StepsMode.StepsMode(game=self)
    self.alpha_mode = scoredisplay.AlphaScoreDisplay(game=self,priority=5)
    self.trough_mode = procgame.modes.trough.Trough(self,
      ["trough1", "trough2", "trough3"], "trough1", "trough",
       [], "shooterR", self.ballDrained)

    ### MIDI HANDLING ###
    self.midi_in_sol = rtmidi.MidiIn()
    self.midi_in_sol.open_port(self.gameConfig.inputMidiSolenoids)
    self.midi_in_lamp = rtmidi.MidiIn()
    self.midi_in_lamp.open_port(self.gameConfig.inputMidiLamps)
    self.midi_out = rtmidi.MidiOut()
    self.midi_out.open_port(self.gameConfig.outputMidiSwitches)
    self.addSwitchHandlers()

    ### LAMP SHOWS ###
    self.lampctrl = procgame.lamps.LampController(self)
    self.lampctrl.register_show('attract', 'lamps/attract.lampshow')
    self.lampctrl.register_show('start', 'lamps/start.lampshow')
    self.lampctrl.register_show('trapdoorOpen', 'lamps/trapdoorOpen.lampshow')

    print self.lamps
    
  def addSwitchHandlers(self):
    
    def fireMidiActive (sw):
      midiNum = int(filter(str.isdigit, sw.yaml_number))
      print sw.name, midiNum 
      self.midi_out.send_message([0x90, midiNum, 100]) # Note on channel 1
      # midi_out.send_message([0x80, midiNum, 0]) # Note off

    def fireMidiInactive (sw):
      midiNum = int(filter(str.isdigit, sw.yaml_number))
      self.midi_out.send_message([0x91, midiNum, 100]) # Note off channel 2
      # midi_out.send_message([0x80, midiNum, 0]) # Note off

    for sw in self.switches: 
      self.basic_mode.add_switch_handler(name=sw.name, event_type='active', delay=0, handler=fireMidiActive)
      self.basic_mode.add_switch_handler(name=sw.name, event_type='inactive', delay=0, handler=fireMidiInactive)
  

  def tick(self):
    self.handleMidiInput()

  def reset(self):
    super(FapoGame, self).reset()
    self.modes.add(self.alpha_mode)
    self.modes.add(self.trough_mode)
    self.modes.add(self.idle_mode)
    self.resetSolenoids()

  def resetSolenoids(self):
    self.flippersOff()
    self.coils.rampDiverter.pulse()
    self.rudyMouthClose()
    self.trapDoorClose()
    self.crazyStepsClose()
    self.coils.outhole.pulse()
    self.coils.tunnelKickbig.pulse()
    self.coils.rudyKickbig.pulse()

  def updateBallDisplay(self):
    self.alpha_display.display(["      PLAY      ", "   Ball " + str(self.ball) + " of " + str(self.balls_per_game) + "  "])

  # TEST IF THIS OVERRIDE IS OKAY
  def start_game(self):
    self.game_started()
    if self.gameConfig.disableMaxCtrl:
      self.midi_start_game()
    else:
      # Fire start_game midi at Max
      self.midi_out.send_message([0x92, self.gameConfig.midiStartGame, 100]) # Command on channel 3

  def midi_start_game(self):
    self.start_ball()
    self.ball_start_time = time.time()
    self.add_player()
    self.updateBallDisplay()
    self.flippersOn()

  def ballDrained(self):
    # Check to see if ball is in play to determine false positive
    if not self.trough_mode.num_balls_in_play:
      self.end_ball()
      print "BALL DRAINED"
      if self.ball > 0:
        self.updateBallDisplay()
      

  def game_ended(self):
    print "GAME OVER!"
    self.alpha_display.display(["      GAME      ", "      OVER      "])
    self.basic_mode.delay(name=None, event_type=None, delay=5, handler=self.reset, param=None)

  def ball_starting(self):
    if self.gameConfig.disableMaxCtrl:
      self.midi_ball_starting()
    else:
      self.midi_out.send_message([0x92, self.gameConfig.midiBallStarting, 100]) # Command on channel 3 

  def midi_ball_starting(self):
    self.lampctrl.play_show('start', repeat=True)
    self.trough_mode.launch_balls(1)

  def flippersOn(self):
    # General Illumination on?
    self.enable_flippers(enable=True)

  def flippersOff(self):
    # General Illumination off?
    self.enable_flippers(enable=False)

  def crazyStepsOpen(self):
    self.coils.rampDiverter.schedule(schedule=0xffffffff,
    cycle_seconds=1, now=True)
    self.coils.stepsGate.schedule(schedule=0xffffffff,
    cycle_seconds=4, now=True)
    self.lamps.stepsOpen.schedule(schedule=0xffffffff,
    cycle_seconds=4, now=True)
    self.lamps.rampStepsLamp.schedule(schedule=0xffffffff,
    cycle_seconds=4, now=True)

  def crazyStepsClose(self):
    self.coils.rampDiverter.pulse(1)
    self.coils.stepsGate.pulse(1)
    self.lamps.stepsOpen.pulse()
    self.lamps.rampStepsLamp.pulse()

  def rudyMouthOpen(self):
    self.coils.upDownDriver.enable()
    self.coils.mouthMotor.pulse()

  def rudyMouthClose(self):
    self.coils.upDownDriver.disable()
    self.coils.mouthMotor.pulse()

  def trapDoorOpen(self):
    if self.switches.trapDoorClosed.state:
      self.lamps.trapDoorBonus.schedule(schedule=0xffffffff,
    cycle_seconds=0, now=True)
      self.coils.trapDoorOpen.pulse()
      self.lampctrl.play_show('trapdoorOpen', repeat=True)


  def trapDoorClose(self):
    if not self.switches.trapDoorClosed.state:
      self.lamps.trapDoorBonus.pulse()
      self.coils.trapDoorClose.pulse()
      self.lampctrl.stop_show()

  def handleMidiInput(self):

    def handleSolenoidInputMidi(midi):
      if midi in self.midiMap:
        yaml_num = self.midiMap[midi]
        for coil in self.coils:
          if coil.yaml_number == yaml_num:
            coil.pulse()
      else:
        if midi == self.gameConfig.midiStartGame:
          self.midi_start_game()
        elif midi == self.gameConfig.midiBallStarting:
          self.midi_ball_starting()


    def handleLampInputMidi(midi):
      if self.gameConfig.inputLaunchpadTest:
        handleLaunchpadTest(midi)   
      else: 
        # IF STATEMENTS FOR GENERAL ILLUMINATION
        for lamp in self.lamps:
          if lamp.yaml_number == ('L' + str(midi[1])):
            if midi[0] == 144:
              lamp.pulse(0)
            else:
              lamp.pulse()
            break

    def handleLaunchpadTest(midi):
      if not (midi[1] in self.midiLampMap):
        for lamp in self.lamps:
          lamp.disable()
        return 

      yaml_num = self.midiLampMap[midi[1]]
      if yaml_num[0] == 'L':
        for lamp in self.lamps:
          if lamp.yaml_number == yaml_num:
            if self.gameConfig.lampToggle:
              if midi[2] == 0:
                if lamp.state()['state'] == 1 and lamp.state()['outputDriveTime'] != 1:
                  print 'true'
                  lamp.disable()
                else:
                  print 'false'
                  lamp.enable()
            else:
              if midi[2] == 127:
                lamp.pulse(0)
              else:
                lamp.pulse()
            break
      else:
        for coil in self.coils:
          if coil.yaml_number == yaml_num:
            if midi[2] == 127:
              if yaml_num[0] == 'C':
                coil.schedule(schedule=0xffffff, cycle_seconds=10, now=True) # limit coils to 4 seconds
              else:
                if coil.state()['state'] == 1 and coil.state()['outputDriveTime'] != 1:
                  coil.disable()
                else:
                  coil.enable()
            else:
              if yaml_num[0] == 'C':
                coil.pulse()

    solenoidMsg, delta_time = self.midi_in_sol.get_message()
    if solenoidMsg and solenoidMsg[0] == 144 and solenoidMsg[2] == 127:
      print solenoidMsg, delta_time
      handleSolenoidInputMidi(solenoidMsg[1])

    lampMsg, delta_time2 = self.midi_in_lamp.get_message()
    if lampMsg:
      print "LAMP"
      print lampMsg, delta_time2
      handleLampInputMidi(lampMsg)
       

def run():
  game = FapoGame(pinproc.MachineTypeWPCAlphanumeric)
  game.reset()
  game.run_loop()
  

if __name__ == '__main__':
  run()

