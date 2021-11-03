from abc import ABC, abstractmethod
from typing import Dict
from ..sfr import StateFieldRegistry

""" Subclasses MUST implement the functions contained here """
class ControlTaskBase(ABC):
    """ """
    def __init__(self, config: Dict, sfr: StateFieldRegistry):
        self.config = config
        self.sfr = sfr
    
    @abstractmethod
    def setup(self):
        """ Setup code that must be called for a given ControlTask """
        pass
    
    """ Maps keys to default values """
    @abstractmethod
    def default(self)->None:
        pass
    
    """ Code that executes every cycle """
    @abstractmethod
    def execute(self)->None:
        pass       
    
# c = ControlTaskBase()