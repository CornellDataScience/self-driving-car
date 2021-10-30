from src.ControlTasks.mission_manager import MissionManager
from ..ControlTasks import ControlTaskBase, ClockManager, MissionManager
from ..sfr import StateFieldRegistry
from configparser import ConfigParser

class MainControlLoop(ControlTaskBase):
    def __init__(self):
        super().__init__()
        self.clock_manager = ClockManager(self.SFR)
        self.mission_manager = MissionManager(self.SFR)

    def configure(self, config):
        # Tobi's configuration code

        # self.clock_manager = ClockManager()
        
        
        #### call initialize of all 
        # self.clock_manager.initialize_sfr(self.sfr)
        # self.clock_manager.initialize_sfr(self.sfr)
        pass

    # clockManagerConfig = config_object["CLOCKMANAGER"]
    # MissionManagerConfig = config_object["MISSIONMANAGER"]

    #Not sure how the config file will look so divided it by managers for now
    #Do we put variables from config into SFR from here?
    # def config(data):
    #     config_object = ConfigParser()
    #     config_object.read(data)
    def default(self) -> None:
        pass

    def execute(self):
        self.clock_manager.execute()
        # MissionManager.execute()
        print("execute")