from abc import ABC, abstractmethod
import time
from typing import Dict
from ..sfr import StateFieldRegistry

""" Subclasses MUST implement the functions contained here """
class ControlTaskBase(ABC):
    """ """
    def __init__(self, name: str, config: Dict, sfr: StateFieldRegistry):
        self.name = name
        self.config = config
        self.sfr = sfr
    
    def full_setup(self) -> None:
        '''A common setup function that then calls the child's setup'''
        self.setup()

    @abstractmethod
    def setup(self):
        """ Setup code that must be called for a given ControlTask """
        pass
    
    def full_default(self) -> None:
        '''Common setup call that then calls the child's default.'''
        self.sfr.set(f'{self.name}.execution_time', 0)
        self.default()

    @abstractmethod
    def default(self)->None:
        """ Maps keys to default values """
        pass
    
    def pre_execute(self) -> None:
        '''A common pre-execution function'''
        self.sfr.set(f'{self.name}.execution_start', time.time())
        
    def post_execute(self) -> None:
        '''A common post-execution function'''
        start_time = self.sfr.get(f'{self.name}.execution_start')
        self.sfr.set(f'{self.name}.execution_time', time.time() - start_time)
    
    def full_execute(self) -> None:
        '''A parent execution function that also calls pre and post execute.'''
        self.pre_execute()
        self.execute()
        self.post_execute()

    """ Code that executes every cycle """
    @abstractmethod
    def execute(self)->None:
        '''Abstract execution function that children should override.'''
        pass