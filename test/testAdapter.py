import asyncio
from digitaltwin_fhir.core import Adapter, transform_value
from digitaltwin_fhir.core.resource import Patient, Identifier, Code, HumanName, Practitioner, ImagingStudy
import datetime
from fhir_cda.ehr import Measurement
from utils import tools
from pprint import pprint
import json


class Test:
    adapter = Adapter("http://localhost:8080/fhir/")

    async def test_load_bundle(self):
        # TODO 1: test load bundle dataset
        await self.adapter.loader().load_fhir_bundle('./dataset/dataset-fhir-bundles')
        # TODO 3:
        # await adapter.load_dicom_dataset('')

    async def test_search(self):
        # TODO 2: test search Patient by name
        # t = await self.adapter.create().create_resource("Patient", "d557ac68-f365-0718-c945-8722ec109c07")
        # print(t)
        p = await self.adapter.search().search_resource_async('Patient', 'd557ac68-f365-0718-c945-8722ec109c07')
        print(p)
        ps = await self.adapter.search().search_resources_async('Patient')
        print(ps)

        patient = Patient(active=True, identifier=[
            Identifier(use=Code("temp"), system="sparc.org", value='sparc-d557ac68-f365-0718-c945-8722ec109c07')],
                          name=[HumanName(use="usual", text="test li",
                                          family="li",
                                          given=["test"])], birth_date=transform_value(datetime.date(2019, 1, 1)))
        await self.adapter.operator().create(resource=patient).save()

    async def test_measurements_analysis_dataset(self):
        measurements = self.adapter.loader().load_sparc_dataset_primary_measurements()
        annotator = measurements.analysis_dataset("./dataset/dataset-sparc")
        m1 = Measurement(value="0.15", code="21889-1", units="cm")
        m2 = Measurement(value="0.15", code="21889-1", units="cm", code_system="http://loinc.org",
                         units_system="http://unitsofmeasure.org")
        annotator.add_measurements(["sub-001", "sub-002"], [m1, m2])
        annotator.save()
        # await measurements.add_practitioner(researcher=Practitioner(
        #     active=True,
        #     identifier=[
        #         Identifier(use=Code("official"), system="sparc.org",
        #                    value='sparc-d557ac68-f365-0718-c945-8722ec109c07')],
        #     name=[HumanName(use="usual", text="Xiaoming Li", family="Li", given=["Xiaoming"])],
        #     gender="male"
        # ))
        # pprint(measurements.primary_measurements)
        # await measurements.generate_resources()

    async def test_measurements_load_json_description(self):
        measurements = self.adapter.loader().load_sparc_dataset_primary_measurements()
        with open('./dataset/dataset-sparc/measurements.json', 'r') as file:
            data = json.load(file)

        await measurements.add_practitioner(researcher=Practitioner(
            active=True,
            identifier=[
                Identifier(use=Code("official"), system="sparc.org",
                           value='sparc-d557ac68-f365-0718-c945-8722ec')],
            name=[HumanName(use="usual", text="Xiaoming Li", family="Li", given=["Xiaoming"])],
            gender="male"
        ))

        await measurements.add_measurements_description(
            data).generate_measurements_via_cda_descriptions().generate_resources()
        # pprint(measurements.primary_measurements)

    async def test_search_dataset(self):
        # a = await self.adapter.search().get_dataset_information(dataset_identifier="21e7de6e-01bc-11ef-878e-484d7e9beb16")
        # pprint(a)
        a = await self.adapter.search().get_patient_measurements(
            patient_identifier="ae5808a8-26db-11ef-9766-484d7e9beb16",
            patient_id=3)


if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.test_measurements_load_json_description())
