from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager, ReadCamera, PointTracker
from ..sfr import StateFieldRegistry
import yaml
import time

class MainControlLoop(ControlTaskBase):
    def setup(self):
        # self.sfr = StateFieldRegistry()

        self.sfr = StateFieldRegistry()

        self.clock_manager = ClockManager(self.config, self.sfr)
        self.read_camera = ReadCamera(self.config, self.sfr)
        self.point_tracker = PointTracker(self.config, self.sfr)
        self.mission_manager = MissionManager(self.config, self.sfr)
        
        self.default()
        self.setup_control_tasks()

    def default(self) -> None:
        self.clock_manager.default()
        self.read_camera.default()
        self.point_tracker.default()
        self.mission_manager.default()

    def setup_control_tasks(self):
        self.clock_manager.setup()
        self.read_camera.setup()
        self.point_tracker.setup()
        self.mission_manager.setup()

    def execute(self):
        self.clock_manager.execute()
        self.mission_manager.execute()
        time.sleep(0.1) #TODO #3, remove this
