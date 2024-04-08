import asyncio
from digitaltwin_fhir.core import Adpter
from utils import tools

async def test():
    adapter = Adpter("http://localhost:8080/fhir/")

    # TODO 1: test load bundle dataset
    # await adapter.load_fhir_bundle_dataset('./dataset')

    # TODO 2: test search Patient by name
    await adapter.load_dicom_dataset("/")
    patientResource = adapter.client.resources('Patient')
    # # patients = await patientResource.search(name=['John', 'Thompson']).fetch_all()
    patients = await patientResource.search(identifier="yyds-2").fetch_all()
    print(patients)
    tools.printPatients(patients)
    # p = patients[0]
    # p['meta']['profile'] = ["http://hl7.org.nz/fhir/StructureDefinition/NzPatient"]
    # await p.save()

    # TODO 3:
    # await adapter.load_dicom_dataset('')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())