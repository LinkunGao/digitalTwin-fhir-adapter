from fhirpy import AsyncFHIRClient

class Adpter:
    def __init__(self, fhir_server_url, authorization='Bearer TOKEN'):
        self.client = AsyncFHIRClient(url=fhir_server_url, authorization=authorization)

