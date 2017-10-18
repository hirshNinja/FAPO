import procgame.game

class BasicMode(procgame.game.Mode):
  def __init__(self, game):
    super(BasicMode, self).__init__(game=game, priority=5)
    self.ballInMouth = False

  def mode_started(self):
    print 'BASIC START'
    self.game.coils.trough.pulse()
    self.game.enable_flippers(enable=True)
    return

  def sw_startButton_active(self, sw):
    self.game.coils.trough.pulse()
    self.game.coils.eyesRight.pulse()

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

  def sw_outhole_active_for_100ms(self, sw):
    self.game.resetSolenoids()
    return procgame.game.SwitchContinue

  def sw_outhole_active_for_100ms(self, sw):
    self.game.resetSolenoids()
    return procgame.game.SwitchContinue

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

  def sw_upperRightLoop_active(self, sw):
    # print sw.number, sw.name, sw.yaml_number
    self.game.trapDoorOpen()
    return procgame.game.SwitchStop
  
  def sw_rampExitTrack_active(self, sw):
    # print sw.number, sw.name, sw.yaml_number
    self.game.coils.rampDiverter.schedule(schedule=0xffffffff,
    cycle_seconds=10, now=True)
    return procgame.game.SwitchStop

  def sw_stepsTrackUpper_active(self, sw):
    self.game.coils.rampDiverter.pulse()
    return procgame.game.SwitchStop

  # def sw_rampEntrance_active(self, sw):
  #   print sw.number, sw.name, sw.yaml_number
  #   return procgame.game.SwitchStop

  def sw_trapDoor_active(self, sw):
    self.game.trapDoorClose()
    return procgame.game.SwitchContinue
