import procgame.game
import pinproc
from modes import BasicMode
from modes import IdleMode
from modes import StepsMode
import rtmidi_python as rtmidi
from config import GameConfig

  

class FapoGame(procgame.game.GameController):
  def __init__(self, machine_type):
    super(FapoGame, self).__init__(machine_type)
    self.gameConfig = GameConfig.GameConfig()
    self.midiMap = None
    if self.gameConfig.inputKeyboardTest:
      self.midiMap = self.gameConfig.midiKeyboardMap
    else:
      print 'ERROR DEFINE MAX MAP'
    self.load_config('config/funhouse.yaml')
    self.basic_mode = BasicMode.BasicMode(game=self)
    self.idle_mode = IdleMode.IdleMode(game=self)
    self.steps_mode = StepsMode.StepsMode(game=self)
    self.midi_in = rtmidi.MidiIn()
    self.midi_in.open_port(self.gameConfig.inputMidiChSolendoids)
    self.midi_out = rtmidi.MidiOut()
    self.midi_out.open_port(self.gameConfig.outputChSwitches)
    self.addSwitchHandlers()


  def addSwitchHandlers(self):
    for sw in self.switches: 
      self.basic_mode.add_switch_handler(name=sw.name, event_type='active', delay=0, handler=self.fireMidiActive)
      self.basic_mode.add_switch_handler(name=sw.name, event_type='inactive', delay=0, handler=self.fireMidiInactive)


  def fireMidiActive (self, sw):
    midiNum = int(filter(str.isdigit, sw.yaml_number))
    print sw.name, midiNum
    self.midi_out.send_message([0x90, midiNum, 100]) # Note on
    # midi_out.send_message([0x80, midiNum, 0]) # Note off

  def fireMidiInactive (self, sw):
    midiNum = int(filter(str.isdigit, sw.yaml_number))
    self.midi_out.send_message([0x91, midiNum, 100]) # Note on
    # midi_out.send_message([0x80, midiNum, 0]) # Note off

  def reset(self):
    super(FapoGame, self).reset()

    self.modes.add(self.idle_mode)
    # self.modes.add(self.basic_mode)
    self.resetSolenoids()

  def resetSolenoids(self):
    self.flippersOff()
    self.coils.rampDiverter.pulse()
    self.rudyMouthClose()
    self.trapDoorClose()
    self.crazyStepsClose()
    self.coils.outhole.pulse()

  def handleInputMidi(self,midi):
    if midi in self.midiMap:
      yaml_num = self.midiMap[midi]
      for coil in self.coils:
        if coil.yaml_number == yaml_num:
          coil.pulse()

  def flippersOn(self):
    self.enable_flippers(enable=True)

  def flippersOff(self):
    self.enable_flippers(enable=False)

  def crazyStepsOpen(self):
    self.coils.rampDiverter.schedule(schedule=0xffffffff,
    cycle_seconds=1, now=True)
    self.coils.stepsGate.schedule(schedule=0xffffffff,
    cycle_seconds=4, now=True)

  def crazyStepsClose(self):
    self.coils.rampDiverter.pulse(1)
    self.coils.stepsGate.pulse(1)

  def rudyMouthOpen(self):
    self.coils.upDownDriver.enable()
    self.coils.mouthMotor.pulse()

  def rudyMouthClose(self):
    self.coils.upDownDriver.disable()
    self.coils.mouthMotor.pulse()

  def trapDoorOpen(self):
    if self.switches.trapDoorClosed.state:
      self.coils.trapDoorOpen.pulse()

  def trapDoorClose(self):
    if not self.switches.trapDoorClosed.state:
      self.coils.trapDoorClose.pulse()

  def tick(self):
    message, delta_time = self.midi_in.get_message()
    if message and message[0] == 144:
      print message, delta_time
      self.handleInputMidi(message[1])
       

def startGame():
  game = FapoGame(pinproc.MachineTypeWPCAlphanumeric)
  game.reset()
  game.run_loop()
  

if __name__ == '__main__':
  startGame()

