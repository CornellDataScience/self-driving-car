from .control_task_base import ControlTaskBase
import sys
import time
import serial

sys.path.append('self-driving-car/embedded')

from comm.py import write, spin

class MotorController(ControlTaskBase):
    def setup(self):
        self.comm = serial.Serial(port='/dev/tty.usbmodem142101',
                     baudrate=115200, timeout=10)
    
    def default(self):
      spin(0)

    def execute(self):
      spin(self.sfr.get('steering_angle'))