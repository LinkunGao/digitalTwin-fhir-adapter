from abc import ABC, abstractmethod
class AbstractResource(ABC):
    async_client = None
    sync_client = None
    def __init__(self, core):
        self.async_client = core.async_client
        self.sync_client = core.sync_client
        