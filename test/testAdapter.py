import asyncio
from digitaltwin_fhir.core import Adapter
from utils import tools


class Test:
    adapter = Adapter("http://localhost:8080/fhir/")

    async def test_load_bundle(self):

        # TODO 1: test load bundle dataset
        await self.adapter.loader().import_dataset('./dataset')
        # TODO 3:
        # await adapter.load_dicom_dataset('')

    async def test_search(self):
        # TODO 2: test search Patient by name
        t = await self.adapter.create().create_resource("Patient", "d557ac68-f365-0718-c945-8722ec109c07")
        print(t)
        p = await self.adapter.search().search_resource('Patient', 'd557ac68-f365-0718-c945-8722ec109c07')
        print(p)
        ps = await self.adapter.search().search_resources('Patient')
        print(ps)


if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.test_search())
