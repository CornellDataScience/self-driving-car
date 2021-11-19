import yaml
import argparse
from src.framework.main_control_loop import MainControlLoop
from src.sfr.state_field_registry import StateFieldRegistry
# from src.runner import * # must import all test instance classes, eg clock_test, no_sim_test
from .clock_test import ClockTest
from .no_sim_test import NoSIM
from .camera_test import CameraTest


CONFIGS_DIR = 'src/configs/'


class TestCaseSystem:
    def run(self):
        # creates necessary objects
        args = self.get_arg_parser()

        # Read YAML file
        if '/' in args.config_file_name:
            raise NameError("Please use the name of the config file in the config file directory. Ex: hootl.yaml")

        file_path = CONFIGS_DIR + args.config_file_name

        with open(file_path, 'r') as stream:
            self.config = yaml.safe_load(stream)
            print(self.config)

        self.sfr = StateFieldRegistry()
        self.mcl = MainControlLoop('main_control_loop', self.config, self.sfr)
        self.mcl.setup()

        # load test case
        test_case_name = args.t
        test = self.load_test_case(test_case_name)
        test.run()

    def load_test_case(self, test_case_name):
        test = globals()[test_case_name]
        return test(self.config, self.sfr, self.mcl)

    def get_arg_parser(self):
        parser = argparse.ArgumentParser("config file, run mode")
        parser.add_argument(
            "config_file_name",
            type=str,
            help=f"A required argument. The config file name. "
                 f"Configs must be in {CONFIGS_DIR}")
        parser.add_argument(
            "t",
            type=str,
            help="An required argument. Specifies which tests to run.")

        return parser.parse_args()
