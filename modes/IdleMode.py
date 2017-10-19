import procgame.game
from BasicMode import BasicMode

class IdleMode(procgame.game.Mode):
  def __init__(self, game):
    super(IdleMode, self).__init__(game=game, priority=5)

  def mode_started(self):
    # self.game.coils.blueFlashers.pulsed_patter(30,127,0)
    self.game.coils.blueFlashers.schedule(schedule=0xa10340,
    cycle_seconds=0, now=False)

  def sw_startButton_active(self, sw):
    # basic_mode = BasicMode(self)
    # self.game.modes.add(basic_mode)
    print 'IDLE START BTN'
    self.game.modes.add(self.game.basic_mode)
    self.game.coils.blueFlashers.pulse()
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def mode_tick(self):
    if self.game.switches.outhole.state:
      self.game.coils.outhole.pulse()