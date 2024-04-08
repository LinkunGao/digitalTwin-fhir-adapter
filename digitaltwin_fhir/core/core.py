from fhirpy import AsyncFHIRClient
from .loader import Loader
from .nzbase.Patient import NzPatient

class Adpter:
    def __init__(self, fhir_server_url, authorization='Bearer TOKEN'):
        self.client = AsyncFHIRClient(url=fhir_server_url, authorization=authorization)
        self._loader = Loader(self.client)

    async def load_fhir_bundle_dataset(self, dataset_path):
        await self._loader.import_dataset(dataset_path)

    async def load_dicom_dataset(self, dataset_path):
        patient = NzPatient(self.client)
        await patient.create_nz_patient("yyds-2")
        await patient.update_name("John", "Thompson").update_gender("male").update_birth("1985-05-30").save()

