# not to use sys and use python packages

from .control_task_base import ControlTaskBase

from ..sfr import StateFieldRegistry

""" This test control task demonstrates how to set and read info from the SFR"""
class TestControlTask(ControlTaskBase):
  def __init__(self):
    pass
  
  def default(self, sfr:StateFieldRegistry):
    sfr.set("test", True)

  def execute(self, sfr:StateFieldRegistry):
    res = sfr.get("test")
    print(res)