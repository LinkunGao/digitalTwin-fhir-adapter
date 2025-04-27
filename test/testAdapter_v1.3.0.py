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
    # adapter = Adapter("http://localhost:8080/fhir/")
    adapter = Adapter("http://130.216.217.173:8080/fhir")

    async def test_measurements_load_json_description(self, root):
        # dataset/ep4/measurements/
        root = Path(root)
        measurements = self.adapter.digital_twin().measurements()
        with open(root / 'measurements.json', 'r') as file:
            data = json.load(file)

        await measurements.add_practitioner(researcher=Practitioner(
            active=True,
            identifier=[
                Identifier(use=Code("official"), system="sparc.org",
                           value='sparc-d557ac68-f365-0718-c945-8722ec')],
            name=[HumanName(use="usual", text="Prasad", family="", given=["Prasad"])],
            gender="male"
        ))
        # await measurements.add_practitioner(researcher=Practitioner(
        #     active=True,
        #     identifier=[
        #         Identifier(use=Code("official"), system="sparc.org",
        #                    value='sparc-f5635bbe-a3a7-4062-8f53-f4eb65683828')],
        #     name=[HumanName(use="usual", text="Linkun Gao", family="Gao", given=["Linkun"])],
        #     gender="male"
        # ))

        await measurements.add_measurements_description(data).generate_resources()

    async def test_workflow_tool_load_json_description(self, root):
        root = Path(root)
        subfolders = [entry for entry in root.iterdir() if entry.is_dir()]
        workflow_tool = self.adapter.digital_twin().workflow_tool()

        for folder in subfolders:
            with open(folder / 'workflow_tool.json', 'r') as file:
                data = json.load(file)
            await workflow_tool.add_workflow_tool_description(data).generate_resources()
        pprint(workflow_tool.descriptions)

    async def test_workflow_load_json_description(self, root):
        root = Path(root)
        subfolders = [entry for entry in root.iterdir() if entry.is_dir()]
        workflow = self.adapter.digital_twin().workflow()

        for folder in subfolders:
            with open(folder / 'workflow_fhir.json', 'r') as file:
                data = json.load(file)
            await workflow.add_workflow_description(data).generate_resources()

        pprint(workflow.descriptions)

    async def test_workflow_process_load_json_description(self, root):
        root = Path(root)
        processes = self.adapter.digital_twin().process()

        with open(root / 'workflow_tool_process.json', 'r') as file:
            data = json.load(file)
        await processes.add_workflow_tool_process_description(data).generate_resources()






if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test.test_measurements_load_json_description("./dataset/ep4/measurements/dataset-1"))
    # loop.run_until_complete(test.test_measurements_load_json_description("./dataset/ep4/measurements/dataset-2"))
    # loop.run_until_complete(test.test_workflow_tool_load_json_description("./dataset/ep4/tools"))
    # loop.run_until_complete(test.test_workflow_load_json_description("./dataset/ep4/workflow"))
    # loop.run_until_complete(test.test_workflow_process_load_json_description("./dataset/ep4/process/dataset-workflow-tool-process-1"))
    # loop.run_until_complete(
    #     test.test_workflow_process_load_json_description("./dataset/ep4/process/dataset-workflow-tool-process-2"))

    #  EP1
    # loop.run_until_complete(test.test_measurements_load_json_description("./dataset/ep1/measurements"))
    # loop.run_until_complete(test.test_workflow_tool_load_json_description("./dataset/ep1/tools"))
    # loop.run_until_complete(test.test_workflow_load_json_description("./dataset/ep1/workflow"))
    # loop.run_until_complete(
    #     test.test_workflow_process_load_json_description("./dataset/ep1/process/dataset-workflow-tool-process-1"))