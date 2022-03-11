import yaml
import argparse
from src.framework.main_control_loop import MainControlLoop
from src.sfr.state_field_registry import StateFieldRegistry

# from src.runner import * # must import all test instance classes, eg clock_test, no_sim_test


CONFIGS_DIR = "src/configs/"


class TestCaseSystem:
    """A class for setting up the MCL and SFR and running it within a test case."""

    @staticmethod
    def load_yaml(config_file_name: str) -> dict:
        """Reads in the yaml config dict given the config_file_name.

        Raises: NameError if the name of the config_file contains /'s indicating a full path.
        Returns: a dictionary of the configuration
        """
        if "/" in config_file_name:
            raise NameError(
                "Please use the name of the config file in the config file directory. Ex: hootl.yaml"
            )

        file_path = CONFIGS_DIR + config_file_name
        config = None
        with open(file_path, "r") as stream:
            config = yaml.safe_load(stream)

        return config

    def run(self):
        # creates necessary objects
        args = self.get_arg_parser()

        self.config = TestCaseSystem.load_yaml(args.config_file_name)

        self.sfr = StateFieldRegistry()
        self.mcl = MainControlLoop("main_control_loop", self.config, self.sfr)
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
            f"Configs must be in {CONFIGS_DIR}",
        )
        parser.add_argument(
            "t", type=str, help="An required argument. Specifies which tests to run."
        )

        return parser.parse_args()
