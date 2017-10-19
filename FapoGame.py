import procgame.game
import pinproc
from modes import BasicMode
from modes import IdleMode
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
    self.midi_in = rtmidi.MidiIn()
    self.midi_in.open_port(self.gameConfig.inputMidiChSolendoids)
    self.midi_out = rtmidi.MidiOut()
    self.midi_out.open_port(self.gameConfig.outputChSwitches)
    self.addSwitchHandlers()


  def addSwitchHandlers(self):
    for sw in self.switches: 
      eventType = 'active'
      if sw.name == "shooterR":
        eventType = 'deactive'
      self.basic_mode.add_switch_handler(name=sw.name, event_type=eventType, delay=0, handler=self.fireMidi)

  def fireMidi (self, sw):
    midiNum = int(filter(str.isdigit, sw.yaml_number))
    print sw.name, midiNum
    self.midi_out.send_message([0x90, midiNum, 100]) # Note on
    # midi_out.send_message([0x80, midiNum, 100]) # Note off

  def reset(self):
    super(FapoGame, self).reset()

    self.modes.add(self.idle_mode)
    # self.modes.add(self.basic_mode)
    self.resetSolenoids()

  def resetSolenoids(self):
    self.rudyMouthClose()
    self.trapDoorClose()
    self.coils.outhole.pulse()

  def handleInputMidi(self,midi):
    if midi in self.midiMap:
      yaml_num = self.midiMap[midi]
      for coil in self.coils:
        if coil.yaml_number == yaml_num:
          coil.pulse()

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

