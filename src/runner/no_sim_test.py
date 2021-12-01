from .testing_instance import TInstance


class NoSIM(TInstance):

    # override
    def cycle(self):
        # mcl.read_sensors() # updates SFR with raw sensor vals/simulated sensor inputs
        # mcl.process() # process sensor values and add to SFR
        # mcl.decide() # decide what to do
        self.mcl.execute()  # set hardware components to execute decision

    def run(self):
        while True:
            self.cycle()
    
    
