from ControlTasks.ClockManager import ClockManager
from ControlTasks.MissionManager import MissionManager
from configparser import ConfigParser


def __init__(data):
    config_object = ConfigParser()
    config_object.read(data)
    global clockManagerConfig, MissionManagerConfig

    clockManagerConfig = config_object["CLOCKMANAGER"]
    MissionManagerConfig = config_object["MISSIONMANAGER"]

    #Not sure how the config file will look so divided it by managers for now

    #Do we put variables from config into SFR from here?

def execute():
    while(True):
        ClockManager.execute()
        MissionManager.execute()
        print("execute")