from .control_task_base import ControlTaskBase
import serial
import time

comm = serial.Serial(port="/dev/tty.usbmodem144101", baudrate=115200, timeout=10)


def write(x):
    comm.write(x.encode("UTF-8"))


def spin(x):
    write(str(x))
    time.sleep(0.0856)
    write(str(x))
    time.sleep(0.0856)


class MotorController(ControlTaskBase):
    def setup(self):
        pass

    def default(self):
        spin(0)

    def execute(self):
        spin(self.sfr.get("steering_angle"))
