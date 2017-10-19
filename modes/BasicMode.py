import procgame.game

class BasicMode(procgame.game.Mode):
  def __init__(self, game):
    super(BasicMode, self).__init__(game=game, priority=5)
    self.ballInMouth = False
    self.openCrazySteps = False

  def mode_started(self):
    self.game.alpha_display.display(["     WELCOME    ", "      HOME      "])
    self.game.start_game()
    self.game.add_player()
    self.game.start_ball()
    self.game.flippersOn()
    return

### RESET GAME/MODE ###
  def sw_startButton_active(self, sw):
    # self.game.troughController.launch_balls(1)
    # self.game.flippersOn()
    return procgame.game.SwitchContinue

  def sw_lockMechLeft_active_for_1000ms(self, sw):
    self.game.coils.multiballRelease.pulse()
    return procgame.game.SwitchContinue

  def sw_rudysHideoutKickbig_active_for_100ms(self, sw):
    self.game.coils.kickbig.pulse()
    return procgame.game.SwitchContinue

  def sw_tunnelKickout_active_for_200ms(self, sw):
    self.game.coils.tunnelKickbig.pulse()
    return procgame.game.SwitchContinue

  # def sw_outhole_active_for_100ms(self, sw):
  #   self.game.resetSolenoids()
  #   return procgame.game.SwitchContinue

  def sw_dummyJaw_active(self, sw):
    self.game.rudyMouthOpen()
    return procgame.game.SwitchContinue

  def sw_dummyJaw_inactive(self, sw):
    if self.ballInMouth:
      self.game.rudyMouthClose()
      self.ballInMouth = False

  def sw_dummyEjectHole_active_for_300ms(self, sw):
    self.ballInMouth = True
    self.game.coils.dummyEjectHole.pulse()
    return True

  def sw_trapDoor_active(self, sw):
    self.game.trapDoorClose()
    return procgame.game.SwitchContinue

  def sw_upperRightLoop_active(self, sw):
    # print sw.number, sw.name, sw.yaml_number
    self.game.trapDoorOpen()
    self.delay(delay=5, handler=self.game.trapDoorClose)
    return procgame.game.SwitchStop
  
  def sw_rampExitTrack_active(self, sw):
    self.openCrazySteps = True
    return procgame.game.SwitchStop

  def sw_stepsTrackUpper_active(self, sw):
    self.openCrazySteps = False
    return procgame.game.SwitchStop

  def sw_upperRampSwitch_active(self, sw):
    if self.openCrazySteps:
      self.game.crazyStepsOpen()
    return procgame.game.SwitchStop

  def sw_shooterL_active(self, sw):
    self.game.modes.remove(self)
    self.game.modes.add(self.game.steps_mode)
    return procgame.game.SwitchContinue

