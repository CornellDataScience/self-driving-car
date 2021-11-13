import yaml
import argparse
from src.framework.main_control_loop import MainControlLoop
from src.sfr.state_field_registry import StateFieldRegistry
# from src.runner import * # must import all test instance classes, eg clock_test, no_sim_test
from .clock_test import ClockTest
from .no_sim_test import NoSIM
from .camera_test import CameraTest


class TestCaseSystem:
    def run(self):
        # creates necessary objects
        args = self.get_arg_parser()

        # Read YAML file
        file_path = args.config_file_path
        with open(file_path, 'r') as stream:
            self.config = yaml.safe_load(stream)
            print(self.config)

        self.sfr = StateFieldRegistry()
        self.mcl = MainControlLoop(self.config, self.sfr)
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
            "config_file_path",
            type=str,
            help="A required argument. The path to YAML configuration file.")
        parser.add_argument(
            "t",
            type=str,
            help="An required argument. Specifies which tests to run.")

        return parser.parse_args()
