from src.ControlTasks.static_frame import StaticFrame
from ..ControlTasks import (ControlTaskBase, ClockManager, MissionManager,
ReadCamera, PointTracker, ProcessFrame, DisplayFrame, ReadFullCamera)
from ..sfr import StateFieldRegistry
import time


class MainControlLoop(ControlTaskBase):
    def setup(self):
        self.sfr = StateFieldRegistry()

        """All the setup required for the MainControlLoop."""
        self.clock_manager = ClockManager(self.config, self.sfr)

        # set how to read images depending on run mode
        if self.config['run_mode'] == 'HOOTL':
            self.read_camera = StaticFrame(self.config, self.sfr)
        elif self.config['run_mode'] == 'HITL':
            if self.config['camera'] == 'webcam':
                self.read_camera = ReadCamera(self.config, self.sfr)
            elif self.config['camera'] == 'depthcam':
                self.read_camera = ReadFullCamera(self.config, self.sfr)

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
        start_time = time.time()

        self.clock_manager.execute()
        clock_time = time.time()
        self.read_camera.execute()
        read_time = time.time()
        self.mission_manager.execute()
        mission_time = time.time()
        self.process_frame.execute()
        process_time = time.time()
        self.display_frame.execute()

        end_time = time.time()

        print("Read Image time: ", read_time-clock_time)
        print("Process Image Time: ", process_time-mission_time)
        print("Display Image Time: ", end_time-process_time)
        print("Total Time: ", end_time-start_time)
        time.sleep(0.1)  # TODO #3, remove this
