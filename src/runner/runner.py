from src.MainControlLoop import MainControlLoop
import sys


# Run the inilization on the config file (path from command line)
MainControlLoop.__init__(sys.argv[1])
MainControlLoop.execute()  # Execute the main control loop
