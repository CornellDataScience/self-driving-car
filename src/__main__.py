from .framework import MainControlLoop
import sys
import yaml

def run():
    mcl = MainControlLoop()

    # TODO REFACTOR THIS OUT
    if len(sys.argv) > 2:
        # Read YAML file
        file_path = sys.argv[1]
    else:
        file_path = 'src/config.yaml'

    with open(file_path, 'r') as stream:
        config_dict = yaml.safe_load(stream)

    mcl.initialize(config_dict)
    # END REFACTOR TODO


    mcl.execute()

if __name__ == '__main__':
    run()