from .control_task_base import ControlTaskBase
from ..sfr import StateFieldRegistry

import time
# control tasks init and sfr init


class TimeManager(ControlTaskBase):

    def setup(self):
        pass

    def default(self):
        self.sfr.set("start_time", time.time())
        self.sfr.set("target_control_cycle_duration", 1)

    def execute(self):

        # add start time into sfr
        # get start time after all control task calls
        current_time = time.time()
        start_time = self.sfr.get("start_time")
        runtime = self.sfr.get("target_control_cycle_duration")

        if current_time - start_time < runtime:
            print(current_time)
            print(start_time)
            print('elapsed time: ' + str(current_time - start_time))
            print('runtime: ' + str(runtime))
            print('time to sleep: ' + str(runtime - (current_time - start_time)))
            time.sleep(runtime - (current_time - start_time))
            # while current_time - start_time < runtime:
            #     time.sleep(0.0000001)
            #     current_time = time.time()

        if current_time - start_time >= runtime:
            print("BAD! Ran for more than " + str(runtime) + " seconds")
            print('Ran for ' + str(current_time - start_time))

        self.sfr.set("start_time", time.time())
