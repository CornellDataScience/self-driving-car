from .control_task_base import ControlTaskBase
import time
#control tasks init and sfr init 

class TimeManager(ControlTaskBase):
    def __init__(self, config, sfr):
        self.time = 0
        self.sfr = sfr

    def default(self):
        self.sfr.set("target_control_cycle_duration",0.1)

    def execute(self):
        
        #add start time into sfr 
        #get start time after all control task calls 
        start_time = self.sfr.get("now")
        runtime = self.sfr.get("target_control_cycle_duration")
        
        if start_time < runtime:
            time.sleep(runtime-start_time)

        if start_time >= runtime:
            print("BAD! Ran for "+ runtime + " seconds")
            

