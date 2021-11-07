from .control_task_base import ControlTaskBase
from ..sfr import StateFieldRegistry

import time
#control tasks init and sfr init 

class TimeManager(ControlTaskBase):
    def __init__(self):
        self.time = 0

    def default(self):
        self.sfr.set("target_control_cycle_duration",0.1)

    def execute(self):
        
        #add start time into sfr 
        #get start time after all control task calls 
        start_time = self.sfr.get("start_time")
        self.default()
        runtime = self.sfr.get("target_control_cycle_duration")
        
        if start_time < runtime:
            time.sleep(runtime-start_time)

        if start_time >= runtime:
            print("BAD! Ran for "+ runtime + " seconds")
            

