import sys
import yaml
from src.framework.main_control_loop import MainControlLoop
from src.sfr.state_field_registry import StateFieldRegistry
from src.runner import * # must import all test instance classes, eg clock_test, no_sim_test

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
        self.mcl.setup()

        # load test case
        test = self.load_test_case("ClockTest")
        test.run()

    def load_test_case(self, test_case_name):
        print(globals())
        test = globals()[test_case_name]
        return test(self.config, self.sfr, self.mcl)
