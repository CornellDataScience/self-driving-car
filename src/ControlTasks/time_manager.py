import time
from .control_task_base import ControlTaskBase
from ..sfr import StateFieldRegistry
 
class TimeManager(ControlTaskBase):
 
   def setup(self):
       pass
 
   def default(self):
       self.sfr.set("start_time", time.time())
       self.sfr.set("target_control_cycle_duration", .05)
 
   def execute(self):
 
       current_time = time.time()
       start_time = self.sfr.get("start_time")
       runtime = self.sfr.get("target_control_cycle_duration")
 
       if current_time - start_time < runtime:
          
           time.sleep(runtime - (current_time - start_time))
 
       #if current_time - start_time >= runtime:
       else:
           print("ERROR! Ran for more than " + str(runtime) + " seconds")
           print('Ran for ' + str(current_time - start_time))
 
       self.sfr.set("start_time", time.time())
