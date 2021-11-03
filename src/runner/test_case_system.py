import sys
import yaml
from src.framework.main_control_loop import MainControlLoop
from src.runner.no_sim_test import NoSIM

from src.sfr.state_field_registry import StateFieldRegistry

class TestCaseSystem:
    def run(self):
        # creates necessary objects
        if len(sys.argv) > 2:
            # Read YAML file
            file_path = sys.argv[1]
        else:
            file_path = 'src/config.yaml'

        with open(file_path, 'r') as stream:
            self.config = yaml.safe_load(stream)
    
        self.sfr = StateFieldRegistry()
        self.mcl = MainControlLoop(self.config, self.sfr)
        self.mcl.initialize()
        self.mcl.default()
        test = NoSIM(self.config, self.sfr, self.mcl)
        test.run()

