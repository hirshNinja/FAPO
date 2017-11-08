import procgame.game
import time
class AttractMode(procgame.game.Mode):
  def __init__(self, game):
    super(AttractMode, self).__init__(game=game, priority=4)
    self.delay = 10
    self.modeEnded = False

  def mode_started(self):
    self.game.lampctrl.play_show('attract', repeat=True)
    self.delay = self.delay + time.time()
    self.game.coils.outhole.pulse()
    self.game.coils.tunnelKickbig.pulse()

    self.game.midiHandler.midi_out.send_message([0x92, 1, 127])
    self.game.alpha_display.display(["     PRESS      ", "     START      "])

    # derb
    return


  # def mode_tick(self):
  #   if time.time() >= self.delay and not self.modeEnded:
  #     self.modeEnded = True
  #     self.game.nextMode()
  #   return

  def sw_startButton_active(self, sw):
    self.game.nextMode()
    return procgame.game.SwitchContinue

  def mode_stopped(self):
    self.game.lampctrl.stop_show()
    return
    
  def sw_outhole_active(self, sw):
    self.game.coils.outhole.pulse()
    return procgame.game.SwitchContinue

  def sw_tunnelKickout_active(self, sw):
    self.game.coils.tunnelKickbig.pulse()
    return procgame.game.SwitchContinue