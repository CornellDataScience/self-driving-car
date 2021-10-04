from abc import ABC, abstractmethod
# import sys
# sys.path.append("..")

from ..StateFieldRegister import StateFieldRegistry
# Not really sure how to deal with imports, but ideally want it to be on
# ControlTaskBase, then TestControlTask inherits from it

""" Subclasses MUST implement the functions contained here """
class ControlTaskBase(ABC):
    """ """
    @abstractmethod
    def __init__(self):
        pass
    
    """ Maps keys to default values """
    @abstractmethod
    def default(self, sfr:StateFieldRegistry)->None:
        pass
    
    """ Code that executes every cycle """
    @abstractmethod
    def execute(self, sfr:StateFieldRegistry)->None:
        pass       
    
# c = ControlTaskBase()