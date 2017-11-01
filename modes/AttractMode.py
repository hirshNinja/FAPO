import procgame.game

class AttractMode(procgame.game.Mode):
  def __init__(self, game):
    super(AttractMode, self).__init__(game=game, priority=4)

  def mode_started(self):
    self.game.lampctrl.play_show('attract', repeat=True)

  def mode_tick(self):
    if self.game.switches.outhole.state:
      self.game.coils.outhole.pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)
    if self.game.switches.tunnelKickout.state:
      self.game.coils.tunnelKickbig.pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)

  def next_mode(self):
    self.game.modes.add(self.game.idle_mode)

  def mode_stopped(self):
    self.game.lampctrl.stop_show()
    self.next_mode()
    
