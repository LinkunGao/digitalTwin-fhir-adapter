import asyncio
from digitaltwin_fhir.core import Adpter
from utils import tools

async def test():
    adapter = Adpter("http://localhost:8080/fhir/")

    # await adapter.loader.import_dataset('./dataset')

    patientResource = adapter.client.resources('Patient')
    patients = await patientResource.search(name=['John', 'Thompson']).fetch_all()
    tools.printPatients(patients)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())