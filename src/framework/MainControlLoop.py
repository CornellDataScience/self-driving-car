from ..ControlTasks import ClockManager, MissionManager

from configparser import ConfigParser


    # clockManagerConfig = config_object["CLOCKMANAGER"]
    # MissionManagerConfig = config_object["MISSIONMANAGER"]

    #Not sure how the config file will look so divided it by managers for now
    #Do we put variables from config into SFR from here?
def config(data):
    config_object = ConfigParser()
    config_object.read(data)


def execute():
    while(True):
        ClockManager.execute()
        MissionManager.execute()
        print("execute")