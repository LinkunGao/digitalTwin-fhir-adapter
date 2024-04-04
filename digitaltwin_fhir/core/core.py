from fhirpy import AsyncFHIRClient
from .loader import Loader

class Adpter:
    def __init__(self, fhir_server_url, authorization='Bearer TOKEN'):
        self.client = AsyncFHIRClient(url=fhir_server_url, authorization=authorization)
        self.loader = Loader(self.client)
