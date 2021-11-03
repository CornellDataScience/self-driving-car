from src.runner.testing_instance import TInstance

class CameraTest(TInstance):
    def run_iteration(self):
        self.mcl.execute() # set hardware components to execute decision

    def run(self):
        pass