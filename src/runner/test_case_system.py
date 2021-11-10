import sys
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
        parser = argparse.ArgumentParser("config file, run mode")
        parser.add_argument("--c", type=str,
        help="An optional argument. The configuration file")
        parser.add_argument("--m", type=str,
        help="An optional argument. Specifies which mode to run in. By default, runs NoSIM")

        args = parser.parse_args()

        # Read YAML file
        file_path = "src/config.yaml"
        if args.c != None:
            file_path = args.c

        with open(file_path, 'r') as stream:
            self.config = yaml.safe_load(stream)

        self.sfr = StateFieldRegistry()
        self.mcl = MainControlLoop(self.config, self.sfr)
        self.mcl.setup()

        # load test case
        test_case_name = "NoSIM"
        if args.m != None:
            test_case_name = args.m
        test = self.load_test_case(test_case_name)
        test.run()

    def load_test_case(self, test_case_name):
        test = globals()[test_case_name]
        return test(self.config, self.sfr, self.mcl)
