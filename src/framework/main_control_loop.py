from src.ControlTasks.time_manager import TimeManager
from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager, ReadCamera, PointTracker
from ..ControlTasks import (ControlTaskBase, ClockManager, MissionManager,
                            Webcam, PointTracker, ProcessFrame, DisplayFrame,
                            DepthCamera, StaticFrame)
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
        self.time_manager = TimeManager(self.config, self.sfr)

        self.clock_manager = ClockManager(
            'clock_manager', self.config, self.sfr)

        # set how to read images depending on run mode
        if self.config['run_mode'] == 'HOOTL':
            self.read_camera = StaticFrame(
                'static_frame_camera', self.config, self.sfr)
        elif self.config['run_mode'] == 'HITL':
            if self.config['camera'] == 'webcam':
                self.read_camera = Webcam(
                    'webcam_camera', self.config, self.sfr)
            elif self.config['camera'] == 'depthcam':
                self.read_camera = DepthCamera(
                    'depth_camera', self.config, self.sfr)
            else:
                raise ValueError(
                    'invalid camera type. Please choose either webcam or depthcam'
                )
        else:
            raise ValueError(
                'invalid run mode. Please choose either HOOTL or HITL')

        self.point_tracker = PointTracker(
            'point_tracker', self.config, self.sfr)
        self.mission_manager = MissionManager(
            'mission_manager', self.config, self.sfr)
        self.process_frame = ProcessFrame(
            'process_frame', self.config, self.sfr)
        self.display_frame = DisplayFrame(
            'display_frame', self.config, self.sfr)

        self.default()
        self.setup_control_tasks()

    def default(self) -> None:
        """Call the default functions of all the ControlTasks."""
        self.clock_manager.default()
        self.read_camera.default()
        self.point_tracker.default()
        self.mission_manager.default()
        self.time_manager.default()

    def setup_control_tasks(self):
        """Call the setup functions of all the ControlTasks."""
        self.clock_manager.setup()
        self.read_camera.setup()
        self.point_tracker.setup()
        self.mission_manager.setup()
        self.time_manager.setup()

    def execute(self):
        """Call execute on all control tasks in order."""
        #start_time = time.time()
        # can we instead use an "end of last control cycle time
        # that is set at the end of execute in clock_manager?
        # self.sfr.set("start_time",start_time)
        self.clock_manager.execute()
        self.read_camera.execute()
        self.mission_manager.execute()
        self.time_manager.execute()
        # time.sleep(0.1) #TODO #3, remove this
        self.clock_manager.full_default()
        self.read_camera.full_default()
        self.point_tracker.full_default()
        self.mission_manager.full_default()
        self.process_frame.full_default()
        self.display_frame.full_default()

    def setup_control_tasks(self):
        """Call the setup functions of all the ControlTasks."""
        self.clock_manager.full_setup()
        self.read_camera.full_setup()
        self.point_tracker.full_setup()
        self.mission_manager.full_setup()
        self.process_frame.full_setup()
        self.display_frame.full_setup()

    def execute(self):
        """Call execute on all control tasks in order."""

        self.clock_manager.full_execute()
        self.read_camera.full_execute()
        self.mission_manager.full_execute()
        self.process_frame.full_execute()
        self.display_frame.full_execute()

        time.sleep(0.1)  # TODO #3, remove this
