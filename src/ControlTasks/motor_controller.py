from .control_task_base import ControlTaskBase
from control import spin
import serial

class MotorController(ControlTaskBase):
    def setup(self):
      self.comm = serial.Serial(port='/dev/tty.usbmodem142101',
                     baudrate=115200, timeout=10)
    
    def default(self):
      spin(0, self.comm)

    def execute(self):
      spin(self.sfr.get('steering_angle'), self.comm)