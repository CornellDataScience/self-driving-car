from src.framework.main_control_loop import MainControlLoop
import sys


# Run the inilization on the config file (path from command line)

MainControlLoop = MainControlLoop()
MainControlLoop.initialize(sys.argv[1])
MainControlLoop.execute()  # Execute the main control loop
