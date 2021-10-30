from .runner.test_case_system import TestCaseSystem
from src.sfr.state_field_registry import StateFieldRegistry
from .framework import MainControlLoop
from .runner.no_sim_test import NoSIM
import sys
import yaml

def run():
    tcs = TestCaseSystem()
    tcs.run()

if __name__ == '__main__':
    run()