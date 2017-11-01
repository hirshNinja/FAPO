import MidiHandler
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
from modes import AttractMode



class FapoGame(procgame.game.GameController):
  def __init__(self, machine_type):
    super(FapoGame, self).__init__(machine_type)
    self.ball_start_time = 0
    self.modeIndex = 0
    self.load_config('config/funhouse.yaml')

    ### ALPHANUMERIC DISPLAY ###
    self.aux_port = auxport2.AuxPort(self)
    self.alpha_display = alphanumeric2.AlphanumericDisplay(self.aux_port)
    # self.scoredisplay = scoredisplay.AlphaScoreDisplay(self,4) # blink text

    ### MODES ###
    self.modeSequence = []
    self.attract_mode = AttractMode.AttractMode(game=self)
    self.modeSequence.append(self.attract_mode)
    self.idle_mode = IdleMode.IdleMode(game=self)
    self.modeSequence.append(self.idle_mode)
    self.basic_mode = BasicMode.BasicMode(game=self)
    self.modeSequence.append(self.basic_mode)
    self.steps_mode = StepsMode.StepsMode(game=self)
    self.alpha_mode = scoredisplay.AlphaScoreDisplay(game=self,priority=5)
    self.trough_mode = procgame.modes.trough.Trough(self,
      ["trough1", "trough2", "trough3"], "trough1", "trough",
       [], "shooterR", self.ballDrained)

    ### MIDI HANDLING ###
    self.midiHandler = MidiHandler.MidiHandler(self)
    self.addSwitchHandlers()

    ### LAMP SHOWS ###
    self.lampctrl = procgame.lamps.LampController(self)
    self.lampctrl.register_show('attract', 'lamps/attract.lampshow')
    self.lampctrl.register_show('start', 'lamps/start.lampshow')
    self.lampctrl.register_show('trapdoorOpen', 'lamps/trapdoorOpen.lampshow')

    print self.lamps
    
  def addSwitchHandlers(self):
    for sw in self.switches: 
      self.basic_mode.add_switch_handler(name=sw.name, event_type='active', delay=0, handler=self.midiHandler.fireMidiActive)
      self.basic_mode.add_switch_handler(name=sw.name, event_type='inactive', delay=0, handler=self.midiHandler.fireMidiInactive)
  
  def tick(self):
    self.midiHandler.handleMidiInput()

  def nextMode(self):
    print self.modeSequence
    print 'NEXT MODE: ' + str(self.modeIndex)
    if self.modeIndex > 0:
      self.modes.remove(self.modeSequence[self.modeIndex-1])
    self.modes.add(self.modeSequence[self.modeIndex])
    self.modeIndex = self.modeIndex + 1

  def reset(self):
    super(FapoGame, self).reset()
    self.modes.add(self.alpha_mode)
    self.modes.add(self.trough_mode)
    self.modeIndex = 0
    self.nextMode()
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
    self.midiHandler.fireMidiStartGame()

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
    self.midiHandler.fireMidiBallStarting()

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

  

def run():
  game = FapoGame(pinproc.MachineTypeWPCAlphanumeric)
  game.reset()
  game.run_loop()
  

if __name__ == '__main__':
  run()

