__author__ = 'Dawson'
import wpilib

class PIDTest(wpilib.IterativeRobot):

    def robotInit(self, talonPort, ticksPerRotation=4000, maxVelocity=10):
        print("PID Adjustor")
        print("Move the joystick up and down to spin the motor")
        print("Press 4 to toggle the selected value (P, I, D, F)")
        print("Use 2 and 3 to increase/decrease the selected value")
        print("Hold trigger to print the speed of the motor continuously")
        print()
        print("Using CANTalon:", talonPort)
        
        self.Talon = wpilib.CANTalon(talonPort)
        self.Talon.setPID(1,0,1,0)
        self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        #self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)

        self.goalPosition = self.Talon.getEncPosition()
        self.maxVelocity = maxVelocity
        self.ticksPerRotation = ticksPerRotation

        self.Joystick= wpilib.Joystick(0)
        self.JoystickValues = [0,0,0,0]

        self.PIDNumber = 0
        self.loopCalls = 0
        self.buttonAllowedTime = 0

    def teleopInit(self):
        self.goalPosition = self.Talon.getEncPosition()
    
    # DO NOT CHANGE TELEOPPERIODIC, CHANGE DOALLELSE
    def teleopPeriodic(self):
        if (self.buttonAllowedTime <= self.loopCalls):
            if self.Joystick.getRawButton(4):
                self.PIDNumber += 1
                if self.PIDNumber > 3:
                    self.PIDNumber = 0
                print("Currently adjusting: ")
                if self.PIDNumber == 0:
                    print("P")
                elif self.PIDNumber == 1:
                    print("I")
                elif self.PIDNumber == 2:
                    print("D")
                elif self.PIDNumber == 3:
                    print("F")
                self.buttonAllowedTime = self.loopCalls + 5
            
            elif self.Joystick.getRawButton(3):
                self.changePID(1.1)
                self.printValues()
                self.buttonAllowedTime = self.loopCalls + 5
                
            elif self.Joystick.getRawButton(2):
                self.changePID(1/1.1)
                self.printValues()
                self.buttonAllowedTime = self.loopCalls + 5
                
            elif self.Joystick.getRawButton(1):
                print("Speed: " + str(self.Talon.getEncVelocity()))
                self.buttonAllowedTime = self.loopCalls + 5

        if not (abs(self.goalPosition - self.Talon.getEncPosition()) \
                > self.ticksPerRotation):
            self.goalPosition += self.Joystick.getY() * -1 * self.maxVelocity
        self.Talon.set(self.goalPosition)

        #AT END
        self.loopCalls += 1
        self.loopCalls %= 1000000
        
    def printValues(self):
        print()
        print()
        print("P: " + str(self.Talon.getP()) \
           + " I: " + str(self.Talon.getI()) \
           + " D: " + str(self.Talon.getD()) \
           + " F: " + str(self.Talon.getF()))
        
    def changePID(self, number):
        if self.PIDNumber == 0:
            self.Talon.setP(self.Talon.getP() * number)
        elif self.PIDNumber == 1:
            self.Talon.setI(self.Talon.getI() * number)
        elif self.PIDNumber == 2:
            self.Talon.setD(self.Talon.getD() * number)
        elif self.PIDNumber == 3:
            self.Talon.setF(self.Talon.getF() * number)