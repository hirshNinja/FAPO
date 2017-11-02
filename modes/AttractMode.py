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


  def mode_tick(self):
    if time.time() >= self.delay and not self.modeEnded:
      self.modeEnded = True
      self.game.nextMode()

    if self.game.switches.outhole.state:
    if self.game.switches.tunnelKickout.state:


  def mode_stopped(self):
    self.game.lampctrl.stop_show()
    
  def sw_outhole_active_for_100ms(self, sw):
    self.game.coils.outhole.pulse()
    return procgame.game.SwitchContinue

  def sw_tunnelKickout_active_for_200ms(self, sw):
    self.game.coils.tunnelKickbig.pulse()
    return procgame.game.SwitchContinue