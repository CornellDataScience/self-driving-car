from ..sfr.state_field_registry import *
from ..framework.main_control_loop import *
import sys

class TInstance():
    """"
    An abstract class for test instances.
    TestInstances must implement a run function

    - SFR
    - MCL
    - SIM
    """

    def __init__(self, config, sfr, mcl):
        self.config = config
        self.sfr = sfr
        self.mcl = mcl
        
    # Override - in later cases, will want different things
    # like running the SIM or something
    def run_iteration(self):
        pass