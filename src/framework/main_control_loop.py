from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager
from ..sfr import StateFieldRegistry
import yaml

class MainControlLoop(ControlTaskBase):
    def __init__(self):
        super().__init__()
    def initialize(self, config):
        # self.sfr = StateFieldRegistry()
        # Read YAML file
        with open(config, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        print(data_loaded)
        self.clock_manager = ClockManager()
        self.mission_manager = MissionManager()
        self.mission_manager.initialize(data_loaded)        
        
        #### call initialize of all 
        # self.clock_manager.initialize_sfr(self.sfr)
        # self.clock_manager.initialize_sfr(self.sfr)

    def default(self, sfr: StateFieldRegistry) -> None:
        pass

    def execute(self):
        while(True):
            self.clock_manager.execute()
            self.mission_manager.execute()
            print("execute")