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
    # derb
    return


  def mode_tick(self):
    if time.time() >= self.delay and not self.modeEnded:
      self.modeEnded = True
      self.game.nextMode()
    return


  def mode_stopped(self):
    self.game.lampctrl.stop_show()
    return
    
  def sw_outhole_active(self, sw):
    self.game.coils.outhole.pulse()
    return procgame.game.SwitchContinue

  def sw_tunnelKickout_active(self, sw):
    self.game.coils.tunnelKickbig.pulse()
    return procgame.game.SwitchContinue