from abc import ABC, abstractmethod
# import sys
# sys.path.append("..")

from ..sfr import StateFieldRegistry
# Not really sure how to deal with imports, but ideally want it to be on
# ControlTaskBase, then TestControlTask inherits from it

""" Subclasses MUST implement the functions contained here """
class ControlTaskBase(ABC):
    """ """
    @abstractmethod
    def __init__(self, SFR: StateFieldRegistry):
        self.SFR = SFR
    
    """ Maps keys to default values """
    @abstractmethod
    def default(self)->None:
        pass
    
    """ Code that executes every cycle """
    @abstractmethod
    def execute(self)->None:
        pass       
    
# c = ControlTaskBase()