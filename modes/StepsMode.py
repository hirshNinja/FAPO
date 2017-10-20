import procgame.game
from BasicMode import BasicMode

class StepsMode(procgame.game.Mode):
  def __init__(self, game):
    super(StepsMode, self).__init__(game=game, priority=6)

  def mode_started(self):
    self.game.flippersOff()
    self.game.coils.stepsGate.schedule(schedule=0xffffffff,
        cycle_seconds=0, now=True)
    self.game.coils.redFlashers.schedule(schedule=0xa10340,
    cycle_seconds=0, now=False)

  def sw_stepsLightFrenzy_active(self, sw):
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def sw_stepsLightExtraBall_active(self, sw):
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def sw_steps500000_active(self, sw):
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def sw_stepsSuperdog_active(self, sw):
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def sw_shooterL_active(self, sw):
    for mode in self.game.modes:
      print mode
    return procgame.game.SwitchStop

  def mode_stopped(self):
    self.game.coils.stepsGate.pulse()
    self.game.coils.redFlashers.pulse()
    self.game.flippersOn()
