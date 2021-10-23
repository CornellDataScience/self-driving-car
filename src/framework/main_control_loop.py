<<<<<<< HEAD
from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager
from ..sfr import StateFieldRegistry
import yaml
=======
from src.ControlTasks.mission_manager import MissionManager
from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager
from ..sfr import StateFieldRegistry
from configparser import ConfigParser
>>>>>>> cd7438bd6b78a304d8b5ea0a849f4c90c91be241

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


    # clockManagerConfig = config_object["CLOCKMANAGER"]
    # MissionManagerConfig = config_object["MISSIONMANAGER"]

    #Not sure how the config file will look so divided it by managers for now
    #Do we put variables from config into SFR from here?
    # def config(data):
    #     config_object = ConfigParser()
    #     config_object.read(data)
    def default(self, sfr: StateFieldRegistry) -> None:
        pass

    def execute(self):
        while(True):
            #self.clock_manager.execute()
            self.mission_manager.execute()
            print("execute")