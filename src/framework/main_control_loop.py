from src.ControlTasks.time_manager import TimeManager
from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager, ReadCamera, PointTracker
from ..sfr import StateFieldRegistry
import yaml
import time

class MainControlLoop(ControlTaskBase):
    def initialize(self):
        # self.sfr = StateFieldRegistry()

        self.sfr = StateFieldRegistry()

        self.clock_manager = ClockManager(self.config, self.sfr)
        self.read_camera = ReadCamera(self.config, self.sfr)
        self.point_tracker = PointTracker(self.config, self.sfr)
        self.mission_manager = MissionManager(self.config, self.sfr)
        self.time_manager = TimeManager(self.config, self.sfr)
        
        #### call initialize of all 
        # self.clock_manager.initialize_sfr(self.sfr)
        # self.clock_manager.initialize_sfr(self.sfr)

    def default(self) -> None:
        self.clock_manager.default()
        self.read_camera.default()
        self.point_tracker.default()
        self.mission_manager.default()

    def execute(self):
        while(True):
            start_time = time.time()
            self.clock_manager.execute()
            self.mission_manager.execute()
            self.time_manager.execute(start_time)
            time.sleep(0.1) #TODO #3, remove this