
import rtmidi_python as rtmidi
from config import MidiConfig

class MidiHandler():
	def __init__(self, game):

		self.game = game
		self.midiConfig = MidiConfig.MidiConfig()
		self.midiLampMap = None
		if self.midiConfig.inputLaunchpadTest:
		  self.midiLampMap = self.midiConfig.midiLaunchpadMap
		self.midi_in = rtmidi.MidiIn()
		self.midi_in.open_port(self.midiConfig.inputMidi)
		self.midi_out = rtmidi.MidiOut()
		self.midi_out.open_port(self.midiConfig.outputMidi)

	def fireMidiActive(self, sw):
	  midiNum = int(filter(str.isdigit, sw.yaml_number))
	  print sw.name, midiNum 
	  self.midi_out.send_message([0x90, midiNum, 127]) # Note on channel 1
	  # midi_out.send_message([0x80, midiNum, 0]) # Note off
	  
	def fireMidiInactive(self, sw):
	  midiNum = int(filter(str.isdigit, sw.yaml_number))
	  self.midi_out.send_message([0x91, midiNum, 127]) # Note off channel 2
	  # midi_out.send_message([0x80, midiNum, 0]) # Note off

	def fireMidiStartGame(self):
		self.game.game_started()
		if self.midiConfig.disableMaxCtrl:
			self.game.midi_start_game()
		else:
			# Fire start_game midi at Max
			self.midi_out.send_message([0x92, self.midiConfig.midiStartGame, 100]) # Command on channel 3

	def fireMidiBallStarting(self):
		if self.midiConfig.disableMaxCtrl:
		  self.game.midi_ball_starting()
		else:
		  self.midi_out.send_message([0x92, self.midiConfig.midiBallStarting, 100]) # Command on channel 3 


	def handleMidiInput(self):

	  def solenoidInput(midi):
			note = midi[1]
			if note > 9:
      	yaml_num = "C" + note
      else:
      	yaml_num = "C0" + note
      for coil in self.game.coils:
        if coil.yaml_number == yaml_num:
          coil.pulse()
	    
	      # if midi == self.midiConfig.nextMode:
	      #   self.game.midi_start_game()
	      # elif midi == self.midiConfig.midiBallStarting:
	      #   self.game.midi_ball_starting()

	  def lampInput(midi):
	    if self.midiConfig.inputLaunchpadTest:
	      handleLaunchpadTest(midi)   
	    else: 
	      # IF STATEMENTS FOR GENERAL ILLUMINATION
	      for lamp in self.game.lamps:
	        if lamp.yaml_number == ('L' + str(midi[1])):
	          if midi[2] == 127:
	            lamp.pulse(0)
	          else:
	            lamp.pulse()
	          break

    def commandInput(midi):
  	  if midi[1] == self.midiConfig.midiNextMode:
  	    self.game.nextMode()

	  def handleLaunchpadTest(midi):
	    if not (midi[1] in self.midiLampMap):
	      for lamp in self.game.lamps:
	        lamp.disable()
	      return 

	    yaml_num = self.midiLampMap[midi[1]]
	    if yaml_num[0] == 'L':
	      for lamp in self.game.lamps:
	        if lamp.yaml_number == yaml_num:
	          if self.midiConfig.lampToggle:
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
	      for coil in self.game.coils:
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

    inputMessage, delta_time = self.midi_in.get_message()
  	if inputMessage:
  		if inputMessage[0] == 144:
  			# channel 1
  			lampInput(inputMessage)
  		elif inputMessage[0] == 145 and inputMessage[2] == 127:
  			# channel 2
  			solenoidInput(inputMessage)
  		elif inputMessage[0] == 146 and inputMessage[2] == 127:
  			# channel 3
  			commandInput(inputMessage)


	    
	     