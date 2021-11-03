from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager, ReadCamera, PointTracker, ProcessFrame, DisplayFrame
from ..sfr import StateFieldRegistry
import time

class MainControlLoop(ControlTaskBase):
    def setup(self):
        self.sfr = StateFieldRegistry()

        """All the setup required for the MainControlLoop."""
        self.clock_manager = ClockManager(self.config, self.sfr)
        self.read_camera = ReadCamera(self.config, self.sfr)
        self.point_tracker = PointTracker(self.config, self.sfr)
        self.mission_manager = MissionManager(self.config, self.sfr)
        self.process_frame = ProcessFrame(self.config, self.sfr)
        self.display_frame = DisplayFrame(self.config, self.sfr)
        
        self.default()
        self.setup_control_tasks()

    def default(self) -> None:
        """Call the default functions of all the ControlTasks."""
        self.clock_manager.default()
        self.read_camera.default()
        self.point_tracker.default()
        self.mission_manager.default()
        self.process_frame.default()
        self.display_frame.default()

    def setup_control_tasks(self):
        """Call the setup functions of all the ControlTasks."""
        self.clock_manager.setup()
        self.read_camera.setup()
        self.point_tracker.setup()
        self.mission_manager.setup()
        self.process_frame.setup()
        self.display_frame.setup()

    def execute(self):
        """Call execute on all control tasks in order."""
        self.clock_manager.execute()
        self.mission_manager.execute()
        self.process_frame.execute()
        self.display_frame.execute()
        time.sleep(0.1) #TODO #3, remove this
