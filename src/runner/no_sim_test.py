from .testing_instance import TInstance


class NoSIM(TInstance):

    # override
    def run_iteration(self):
        # mcl.read_sensors() # updates SFR with raw sensor vals/simulated sensor inputs
        # mcl.process() # process sensor values and add to SFR
        # mcl.decide() # decide what to do
        self.mcl.execute()  # set hardware components to execute decision

    def run(self):
        while True:
            self.run_iteration()

    def test_time1(self):
        self.mcl.initialize()  # config
        self.mcl.default()
        self.run_iteration()
        assert self.sfr.get("time") == 1

    def test_time2(self):
        self.mcl.initialize()  # config
        self.mcl.default()
        for i in range(5):
            self.run_iteration()
        assert self.sfr.get("time") == 5
