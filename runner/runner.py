import sys

import MainControlLoop 

MainControlLoop.__init__(sys.argv[1]) #Run the inilization on the config file (path from command line)
MainControlLoop.execute() #Execute the main control loop