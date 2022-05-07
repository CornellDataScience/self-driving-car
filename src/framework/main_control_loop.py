from typing import List
from ..ControlTasks import (
    ControlTaskBase,
    ClockManager,
    MissionManager,
    Webcam,
    PointTracker,
    ProcessFrame,
    DisplayFrame,
    DepthCamera,
    StaticFrame,
    MotorController,
    LaneDetection,
)
from ..sfr import StateFieldRegistry
import time
import serial


class MainControlLoop(ControlTaskBase):
    def setup(self):
        self.sfr = StateFieldRegistry()
        """All the setup required for the MainControlLoop."""
        self.clock_manager = ClockManager("clock_manager", self.config, self.sfr)

        # set how to read images depending on run mode
        if self.config["run_mode"] == "HOOTL":
            self.read_camera = StaticFrame("static_frame_camera", self.config, self.sfr)
        elif self.config["run_mode"] == "HITL":
            if self.config["camera"] == "webcam":
                self.read_camera = Webcam("webcam_camera", self.config, self.sfr)
            elif self.config["camera"] == "depthcam":
                self.read_camera = DepthCamera("depth_camera", self.config, self.sfr)
            else:
                raise ValueError(
                    "invalid camera type. Please choose either webcam or depthcam"
                )
        else:
            raise ValueError("invalid run mode. Please choose either HOOTL or HITL")

        self.point_tracker = PointTracker("point_tracker", self.config, self.sfr)
        self.mission_manager = MissionManager("mission_manager", self.config, self.sfr)
        self.process_frame = ProcessFrame("process_frame", self.config, self.sfr)
        self.display_frame = DisplayFrame("display_frame", self.config, self.sfr)
        self.lane_detection = LaneDetection("lane_detection", self.config, self.sfr)
        self.motor_controller = MotorController(
            "motor_controller", self.config, self.sfr
        )

        # All ControlTasks must be added here to be setup and run.
        self.ct_list: List[ControlTaskBase] = [
            self.clock_manager,
            self.read_camera,
            self.point_tracker,
            self.mission_manager,
            self.process_frame,
            self.display_frame,
            self.motor_controller,
            self.lane_detection,
        ]

        # Lists ready to re-order if required
        self.default_ct_list = self.ct_list
        self.setup_ct_list = self.ct_list
        self.execute_ct_list = self.ct_list

        self.default()
        self.setup_control_tasks()

    def default(self) -> None:
        """Call the default functions of all the ControlTasks."""
        for ct in self.default_ct_list:
            ct.full_default()

    def setup_control_tasks(self):
        """Call the setup functions of all the ControlTasks."""
        for ct in self.setup_ct_list:
            ct.full_setup()

    def execute(self):
        """Call the execute functions of all the ControlTasks."""
        for ct in self.execute_ct_list:
            ct.full_execute()

        time.sleep(0.1)  # TODO #3, remove this
