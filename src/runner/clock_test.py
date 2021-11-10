from src.runner.testing_instance import TInstance

class ClockTest(TInstance):
    def cycle(self):
        self.mcl.execute() # set hardware components to execute decision

    def run(self):
        self.test_time1()
        self.test_time2()

    def test_time1(self):
        self.mcl.initialize() #config
        self.mcl.default()
        self.cycle()
        assert self.sfr.get('time')== 1
    
    def test_time2(self):
        self.mcl.initialize() #config
        self.mcl.default()
        for i in range(5):
            self.cycle()
        assert self.sfr.get('time') == 5