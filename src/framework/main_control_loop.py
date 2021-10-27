from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager, ReadCamera, PointTracker
from ..sfr import StateFieldRegistry
import yaml
import time

class MainControlLoop(ControlTaskBase):
    def __init__(self):
        super().__init__()

    def initialize(self, config):
        # self.sfr = StateFieldRegistry()
        # Read YAML file
        with open(config, 'r') as stream:
            config_file = yaml.safe_load(stream)

        self.sfr = StateFieldRegistry()

        self.clock_manager = ClockManager(config, self.sfr)
        self.read_camera = ReadCamera(config, self.sfr)
        self.point_tracker = PointTracker(config, self.sfr)
        self.mission_manager = MissionManager(config, self.sfr)
        
        self.mission_manager.initialize(config_file)        
        
        #### call initialize of all 
        # self.clock_manager.initialize_sfr(self.sfr)
        # self.clock_manager.initialize_sfr(self.sfr)

    def default(self, sfr: StateFieldRegistry) -> None:
        pass

    def execute(self):
        while(True):
            self.clock_manager.execute()
            self.mission_manager.execute()
            time.sleep(0.1) #TODO #3, remove this