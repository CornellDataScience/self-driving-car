from ControlTaskBase import ControlTaskBase
import sys
sys.path.append("..")
from StateFieldRegistry import StateFieldRegistry

""" This test control task demonstrates how to set and read info from the SFR"""
class TestControlTask(ControlTaskBase):
  def __init__(self):
    print("init")
  
  def default(self, sfr:StateFieldRegistry):
    sfr.set("test", True)

  def execute(self, sfr:StateFieldRegistry):
    res = sfr.get("test")
    print(res)

t = TestControlTask()