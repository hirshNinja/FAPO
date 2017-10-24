import procgame.game
from BasicMode import BasicMode

class IdleMode(procgame.game.Mode):
  def __init__(self, game):
    super(IdleMode, self).__init__(game=game, priority=4)

  def mode_started(self):
    # blink stuff
    # self.game.scoredisplay.set_text("Press",0) 
    # self.game.scoredisplay.set_text("Press Start",0,blink_rate=0.5, seconds=0.5)
    # self.game.scoredisplay.set_text("Start",1,blink_rate=0.1, seconds=0.1)

    self.game.alpha_display.display(["     PRESS      ", "     START      "])
    self.game.lampctrl.play_show('attract', repeat=True)

    # self.game.coils.blueFlashers.schedule(schedule=0xa10340, cycle_seconds=0, now=False)

  def sw_startButton_active(self, sw):
    self.game.modes.remove(self)
    return procgame.game.SwitchStop

  def mode_tick(self):
    if self.game.switches.outhole.state:
      self.game.coils.outhole.pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)
    if self.game.switches.tunnelKickout.state:
      self.game.coils.tunnelKickbig.pulse().pulsed_patter(on_time=30, off_time=50, run_time=1, now=True)

  def startBasicMode(self):
    self.game.modes.add(self.game.basic_mode)
    self.game.coils.blueFlashers.pulse()


  def mode_stopped(self):
    # self.game.scoredisplay.cancel_script() # blink stuff
    self.game.lampctrl.stop_show()
    self.startBasicMode()
    
