from fhirpy import AsyncFHIRClient, SyncFHIRClient
from .operator import Operator
from .search import Search
from .nzbase.Patient import NzPatient
from abc import ABC, abstractmethod


class AbstractAdapter(ABC):
    async_client = None
    sync_client = None

    def __init__(self, url, authorization):
        self.async_client = AsyncFHIRClient(url=url, authorization=authorization)
        self.sync_client = SyncFHIRClient(
            url,
            requests_config={
                "verify": False,
                "allow_redirects": True,
                "timeout": 60,
            },
            authorization=authorization
        )

    @property  # pragma no cover
    @abstractmethod
    def operator_class(self):
        pass

    @property  # pragma no cover
    @abstractmethod
    def search_class(self):
        pass


class Adapter(AbstractAdapter, ABC):
    operator_class = Operator
    search_class = Search

    def __init__(self, url, authorization='Bearer TOKEN'):
        super().__init__(url, authorization)

    def loader(self):
        return self.operator_class(self).load()

    def search(self):
        return self.search_class(self)

    def create(self):
        return self.operator_class(self).create()

