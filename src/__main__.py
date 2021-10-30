from src.sfr.state_field_registry import StateFieldRegistry
from .framework import MainControlLoop
import sys
import yaml

def run():

    # TODO REFACTOR THIS OUT
    if len(sys.argv) > 2:
        # Read YAML file
        file_path = sys.argv[1]
    else:
        file_path = 'src/config.yaml'

    with open(file_path, 'r') as stream:
        config_dict = yaml.safe_load(stream)

    sfr = StateFieldRegistry()
    mcl = MainControlLoop(config_dict, sfr)

    # END REFACTOR TODO

    mcl.initialize()
    mcl.default()
    mcl.execute()

if __name__ == '__main__':
    run()