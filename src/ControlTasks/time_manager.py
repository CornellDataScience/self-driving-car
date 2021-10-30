from .control_task_base import ControlTaskBase
import time
#control tasks init and sfr init 

class TimeManager(ControlTaskBase):
    def __init__(self, config, sfr):
        self.time = 0
        self.sfr = sfr

    def default(self):
        pass

    def execute(self, start_time):
        
        runtime = 10
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time < runtime:
            time.sleep(runtime-elapsed_time)

        if elapsed_time >= runtime:
            print("BAD! Ran for "+ runtime + " seconds")
            

