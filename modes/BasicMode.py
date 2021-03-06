import procgame.game
import time

class BasicMode(procgame.game.Mode):
  def __init__(self, game):
    super(BasicMode, self).__init__(game=game, priority=5)


  def mode_started(self):

    self.ballInMouth = False
    self.openCrazySteps = False
    self.game.start_game()

    # self.game.start_ball()
    # self.game.ball_start_time = time.time()
    # self.game.add_player()
    # self.game.updateBallDisplay()
    # self.game.flippersOn()
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
    self.game.coils.rudyKickbig.pulse()
    return procgame.game.SwitchContinue

  def sw_tunnelKickout_active_for_200ms(self, sw):
    self.game.coils.tunnelKickbig.pulse()
    return procgame.game.SwitchContinue

  def sw_outhole_active_for_100ms(self, sw):
    self.game.coils.outhole.pulse()
    return procgame.game.SwitchContinue

  def sw_dummyJaw_active(self, sw):
    self.game.coils.dummyFlasher.schedule(schedule=0xaaaaaa, cycle_seconds=2, now=True)
    self.game.rudyMouthOpen()
    return procgame.game.SwitchContinue

  def sw_dummyJaw_inactive(self, sw):
    if self.ballInMouth:
      self.game.rudyMouthClose()
      self.ballInMouth = False

  def sw_dummyEjectHole_active(self, sw):
    self.game.lampctrl.play_show('attract', repeat=False)
    return True

  def sw_dummyEjectHole_active_for_600ms(self, sw):
    self.ballInMouth = True
    self.game.coils.dummyEjectHole.pulse()
    return True

  def sw_trapDoor_active(self, sw):
    self.game.lampctrl.play_show('attract', repeat=False)
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

  def sw_shooterR_inactive(self, sw):
    self.game.lampctrl.stop_show()
    return True

  def sw_shooterL_active(self, sw):
    for mode in self.game.modes:
      print mode
    self.game.modes.add(self.game.steps_mode)
    return procgame.game.SwitchContinue

  def sw_upperLeftJetBumper_active(self, sw):
    self.game.lamps.upperLeftJetBumper.pulsed_patter(on_time=50, off_time=50, run_time=255, now=True)
    return True

  def sw_upperRightJetBumper_active(self, sw):
    self.game.lamps.upperRightJetBumper.pulsed_patter(on_time=50, off_time=50, run_time=255, now=True)
    return True

  def sw_lowerJetBumper_active(self, sw):
    self.game.lamps.lowerJetBumper.pulsed_patter(on_time=50, off_time=50, run_time=255, now=True)
    return True

  def sw_stepS_active(self, sw):
    self.game.lamps.stepS.schedule(schedule=0x123456, cycle_seconds=1, now=True)
    return True
    
  def sw_stepT_active(self, sw):
    self.game.lamps.stepT.schedule(schedule=0x123456, cycle_seconds=1, now=True)
    return True
    
  def sw_stepE_active(self, sw):
    self.game.lamps.stepE.schedule(schedule=0x123456, cycle_seconds=1, now=True)
    return True
        
  def sw_stepP_active(self, sw):
    self.game.lamps.stepP.schedule(schedule=0x123456, cycle_seconds=1, now=True)
    return True
    


