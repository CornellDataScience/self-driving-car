from abc import ABC, abstractmethod



class TInstance(ABC):
    """ "
    An abstract class for test instances.
    TestInstances must implement a run function

    - SFR
    - MCL
    - SIM
    """

    def __init__(self, config, sfr, mcl):
        self.config = config
        self.sfr = sfr
        self.mcl = mcl

    # Override - in later cases, will want different things
    # like running the SIM or something
    @abstractmethod
    def cycle(self):
        pass
