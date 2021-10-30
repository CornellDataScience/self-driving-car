from sfr.state_field_registry import *
from framework.main_control_loop import *

class TestInstance():
    """"
    An abstract class for test instances.
    TestInstances must implement a run function

    - SFR
    - MCL
    - SIM
    """

    def __init__(self):
        # creates necessary objects
        self.SFR = StateFieldRegistry()
        self.MCL = MainControlLoop(self.SFR)
        
    # Override - in later cases, will want different things
    # like running the SIM or something
    def run_iteration(self):
        pass