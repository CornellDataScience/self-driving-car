sfrom src.runner.testing_instance import TInstance

class CameraTest(TInstance):
    def cycle(self):
        self.mcl.execute() # set hardware components to execute decision

    # for now, the same as no_sim test, will diverge later
    def run(self):
        while True:
            self.cycle()
