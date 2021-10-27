from .control_task_base import ControlTaskBase
import time

class MissionManager(ControlTaskBase):
  def __init__(self):
      self.sfr = None
      
  def initialize(self, config):
      self.var1 = config["var1"]
      self.var2 = config["var2"]
      self.var3 = config["var3"]

  def default(self):
      pass

  def execute(self):
      print(self.var1)
      print(self.var2)
      print(self.var3)
      time.sleep(0.001)
