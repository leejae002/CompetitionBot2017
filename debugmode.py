__author__ = "tadeuszpforte"

import wpilib
import seamonsters.fix2017
from seamonsters.wpilib_sim import simulate
from seamonsters.modularRobot import Module
from seamonsters.gamepad import Gamepad
from robot import DriveBot

class DebugMode(Module):

    def testInit(self):
        print("--- Debug Mode ---")
        print("Each joystick Y axis controls a motor")
        print("Each directional buttons axis controls a motor")
        print("X flips the motors joysticks and buttons control")

    def testPeriodic(self):
        # if true, joysticks control front motors
        # if false, joysticks control back motors
        testModeJoysticksFront = True

        # switches joysticks and dir buttons
        if DriveBot.gamepad.getRawButton(Gamepad.Y):
            if testModeJoysticksFront:
                print("Joysticks control rear motors")
                testModeJoysticksFront = False
            else:
                print("Joysticks control front motors")
                testModeJoysticksFront = True

        # get values -1 to 1
        joystickLeft = DriveBot.gamepad.getLY()
        joystickRight = DriveBot.gamepad.getRY()

        directionalVertical = 0
        if DriveBot.gamepad.getRawButton(Gamepad.UP):
            directionalVertical = 1
        elif DriveBot.gamepad.getRawButton(Gamepad.DOWN):
            directionalVertical = -1

        directionalHorizontal = 0
        if DriveBot.gamepad.getRawButton(Gamepad.RIGHT):
            directionalHorizontal = 1
        elif DriveBot.gamepad.getRawButton(Gamepad.LEFT):
            directionalHorizontal = -1

        # sets motors
        if testModeJoysticksFront:
            DriveBot.talons[0].set(joystickLeft)
            DriveBot.talons[1].set(joystickRight)
            DriveBot.talons[2].set(directionalVertical)
            DriveBot.talons[3].set(directionalHorizontal)
        else:
            DriveBot.talons[0].set(directionalVertical)
            DriveBot.talons[1].set(directionalHorizontal)
            DriveBot.talons[2].set(joystickLeft)
            DriveBot.talons[3].set(joystickRight)

if __name__ == "__main__":
    wpilib.run(DebugMode)
