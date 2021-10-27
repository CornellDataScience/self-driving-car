from .framework import MainControlLoop
import sys

def run():
    mcl = MainControlLoop()
    mcl.initialize(sys.argv[1])
    mcl.execute()

if __name__ == '__main__':
    run()