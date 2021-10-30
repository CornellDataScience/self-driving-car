from runner.testing_system import TestInstance

class NoSIM(TestInstance):
    def __init__(self):
        super().__init__()
        # self.SIM = ....

    # override
    def run_iteration(self):
        # MCL.read_sensors() # updates SFR with raw sensor vals/simulated sensor inputs
        # MCL.process() # process sensor values and add to SFR
        # MCL.decide() # decide what to do
        self.MCL.execute() # set hardware components to execute decision

    def test_cycle(self):
        self.MCL.configure() #config

        self.run_iteration()
        assert self.SFR['cycle'] == 1
    
