from .control_task_base import ControlTaskBase
import serial
import time

class MotorController(ControlTaskBase):
    def setup(self):
      self.comm = serial.Serial(port="/dev/tty.usbmodem142101", baudrate=115200, timeout=10) 
      time.sleep(0.5)

    def spin(x, self):
      self.comm.write(str(-1 * x).encode('UTF-8'))
      time.sleep(0.0856)
      self.comm.write(str(-1 * x).encode('UTF-8'))
      time.sleep(0.0856)

    def default(self):
        pass

    def execute(self):
        self.spin(self.sfr.get("steering_angle"))
