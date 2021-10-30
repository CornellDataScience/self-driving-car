from .testing_system import TInstance

class NoSIM(TInstance):
    # def __init__(self):
    #     super().__init__()
        # self.SIM = ....

    # override
    def run_iteration(self):
        # MCL.read_sensors() # updates SFR with raw sensor vals/simulated sensor inputs
        # MCL.process() # process sensor values and add to SFR
        # MCL.decide() # decide what to do
        self.MCL.execute() # set hardware components to execute decision

    def test_time1(self):
        self.MCL.initialize({}) #config
        self.MCL.default()
        self.run_iteration()
        assert self.SFR['time'] == 1
    
    def test_time2(self):
        self.MCL.initialize({}) #config
        self.MCL.default()
        for i in range(5):
            self.run_iteration()
        assert self.SFR['time'] == 5
    
    
