import asyncio
from digitaltwins_on_fhir.core import Adapter, transform_value
from digitaltwins_on_fhir.core.resource import Patient, CodeableConcept, Coding, Reference, Identifier, Code, \
    HumanName, Practitioner, ImagingStudy, DiagnosticReport
import datetime
from fhir_cda.ehr import Measurement
from pathlib import Path
from utils import tools
from pprint import pprint
import json
from typing import Literal

class Test:
    adapter = Adapter("http://localhost:8080/fhir/")

    search = adapter.search()

    async def get_patient_all_measurements(self):
        measurements = await self.search.get_patient_measurements("c6923eb4-a5c2-4239-8b7a-16d1268b108d")
        pprint(measurements)

    async def get_derived_data_provenance(self):
        res = await self.search.get_workflow_details_by_derived_data("Observation", "231d9946-949a-4fee-8695-5887209bd2db_2673e5a3-8437-41f5-9fef-0983f5662e93_Workflow-Process-Output-Observation-0-0")
        pprint(res)

    async def get_derived_data_all_primary_inputs(self):
        res = await self.search.get_all_inputs_by_derived_data("Observation", "231d9946-949a-4fee-8695-5887209bd2db_2673e5a3-8437-41f5-9fef-0983f5662e93_Workflow-Process-Output-Observation-0-0")
        pprint(res)

    async def get_all_tools_via_workflow(self):
        res = await self.search.get_all_workflow_tools_by_workflow(name="Automated torso model generation - script")
        pprint(res)

    async def get_inputs_outputs_of_workflow_tool(self):
        res = await self.search.get_all_inputs_outputs_of_workflow_tool(name="Tumour Position Correction (Manual) Tool")
        pprint(res)

if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.get_inputs_outputs_of_workflow_tool())