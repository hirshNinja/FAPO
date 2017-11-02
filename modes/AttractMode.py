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

  def mode_tick(self):
    if time.time() >= self.delay and not self.modeEnded:
      self.modeEnded = True
      self.game.nextMode()

    if self.game.switches.outhole.state:
      self.game.coils.outhole.pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)
    if self.game.switches.tunnelKickout.state:
      self.game.coils.tunnelKickbig.pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)


  def mode_stopped(self):
    self.game.lampctrl.stop_show()
    
