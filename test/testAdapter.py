import asyncio
from digitaltwins_on_fhir.core import Adapter, transform_value
from digitaltwins_on_fhir.core.resource import Patient, Identifier, Code, HumanName, Practitioner, ImagingStudy
import datetime
from fhir_cda.ehr import Measurement
from utils import tools
from pprint import pprint
import json


class Test:
    adapter = Adapter("http://localhost:8080/fhir/")
    # adapter = Adapter("http://130.216.217.173:8080/fhir")

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
        measurements = self.adapter.digital_twin().measurements()
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
        measurements = self.adapter.digital_twin().measurements()
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

        await measurements.add_measurements_description(data).generate_resources()
        # pprint(measurements.primary_measurements)

    async def test_workflow_tool_load_json_description(self):
        workflow_tool = self.adapter.digital_twin().workflow_tool()
        for i in range(7):
            with open(f'./dataset/tools/dataset-workflow-tool-{i + 1}/workflow_tool.json', 'r') as file:
                data = json.load(file)
            await workflow_tool.add_workflow_tool_description(data).generate_resources()
        pprint(workflow_tool.descriptions)

    async def test_workflow_load_json_description(self):
        workflow = self.adapter.digital_twin().workflow()
        with open('./dataset/dataset-workflow-ep4/workflow_fhir.json', 'r') as file:
            data = json.load(file)

        await workflow.add_workflow_description(data).generate_resources()

    async def test_workflow_tool_process_load_json_description(self):
        process = self.adapter.digital_twin().process()

        for i in range(7):
            with open(f'./dataset/process/dataset-workflow-tool-process-{i + 1}/workflow_tool_process.json',
                      'r') as file:
                data = json.load(file)
            await process.add_workflow_tool_process_description(data).generate_resources()
        pprint(process.descriptions)

    async def test_search_digital_twin(self):
        # workflow uuid: sparc-workflow-uuid-001
        # workflow tool 7 uuid: sparc-workflow-tool-clinical_report-777
        # dataset uuid: sparc-breast-dataset-001
        # patient 1 uuid: sparc-breast-patient-001
        client = self.adapter.async_client
        # TODO 1 If I know workflow uuid,
        # TODO 1.1 let's find all related workflow tools
        workflow = await client.resources("PlanDefinition").search(
            identifier="sparc-workflow-uuid-001").first()
        actions = workflow.get("action")
        print("list actions")
        pprint(actions)
        print(
            "******************************************List all workflow tool resources**********************************************")
        for a in actions:
            if a.get("definitionCanonical") is None:
                continue
            resource_type, _id = a.get("definitionCanonical").split("/")
            workflow_tool = await client.reference(resource_type, _id).to_resource()
            print(f"workflow tool: {workflow_tool.get('title')}", workflow_tool)
            # TODO 1.1.1 Find model and software uuid from a specific workflow tool
            print("workflow tool software and model uuid", workflow_tool.get("participant"))
        # TODO 1.2 let's find all related workflow tool process for that workflow
        print(
            "******************************************List all workflow tool process resources**********************************************")
        workflow_tool_processes = await client.resources("Task").search(
            subject=workflow.to_reference().reference).fetch_all()
        print(workflow_tool_processes)

        # TODO 2 If I know a patient uuid, workflow uuid, workflow tool uuid, and a dataset uuid
        # TODO 2.1 Get a specific workflow tool process which belongs to that patient in that dataset and generated by that workflow tool with executing that workflow
        print(
            "******************************************List a specific workflow tool process resource**********************************************")
        # Step 1: find the patient
        patient = await client.resources("Patient").search(identifier="sparc-breast-patient-001").first()
        # Step 2: find the dataset
        dataset = await client.resources("ResearchStudy").search(identifier="sparc-breast-dataset-001").first()
        # Step 3: find the workflow tool
        workflow_tool = await client.resources("ActivityDefinition").search(
            identifier="sparc-workflow-tool-clinical_report-777").first()
        # Step 4: find the research subject
        research_subject = await client.resources("ResearchSubject").search(patient=patient.to_reference().reference,
                                                                            study=dataset.to_reference().reference).first()
        print("research_subject: ", research_subject)
        workflow_tool_process = await client.resources("Task").search(subject=workflow.to_reference(),
                                                                      focus=workflow_tool.to_reference(),
                                                                      based_on=research_subject.to_reference(),
                                                                      owner=patient.to_reference()).first()
        print("workflow_tool_process: ", workflow_tool_process)

        # TODO 2.2 Now we get the breast workflow's step 7 workflow tool's workflow tool process which belongs to patient 1 in dataset 1
        # TODO 2.2.1 Get the input of the workflow tool process
        print(
            "******************************************List input resources in this workflow tool process**********************************************")
        inputs = workflow_tool_process.get("input")
        print("inputs: ", inputs)
        for i in inputs:
            composition = await client.resources("Composition").search(title="primary measurements",
                                                                       entry=i.get("valueReference")).first()
            print("primary measurement's composition: ", composition)
            dataset = await composition.get("subject").to_resource()
            print("dataset: ", dataset)

        # TODO 2.2.2 List all outputs of the workflow tool process
        outputs = workflow_tool_process.get("output")
        print("outputs: ", outputs)

        # TODO 3 I'm interested in a result observation, e.g, distance to nipple
        print(
            "******************************************The interested result observation (distance to nipple)**********************************************")
        ob = await client.resources("Observation").search(
            identifier="sparc-workflow-tool-clinical_report-777-workflow-tool-7-process-002-Observation-0").first()
        print("Step 0: We are interested in this observation (Tumour distance to nipple): ", ob)
        # TODO 3.1 Let's find the observation is generated by which workflow
        # step 1, Find this observation is assigned in which workflow result composition
        composition = await client.resources("Composition").search(title="workflow tool results",
                                                                   entry=ob.to_reference().reference).first()
        print("Step 1: the interested observation is assigned in this composition: ", composition)
        # step 2, Let's find which workflow tool process generates the composition
        workflow_tool_process = await composition.get("subject").to_resource()
        print("Step 2: the composition is generated by this workflow_tool_process: ", workflow_tool_process)
        # step 3, Now we can find the observation is related to which workflow
        workflow = await workflow_tool_process.get("for").to_resource()
        print("Step 3: Now we find the interested observation is related to this workflow: ", workflow)
        # step 3.1, Because we know the interested observation, so we can directly find which workflow tool generates it
        workflow_tool = await ob.get("focus")[0].to_resource()
        print("Step 3.1: We also can find the interested observation is related to this workflow_tool: ", workflow_tool)

        print("------------------------------------")

        # TODO 3.2 Let's also find the interested observation is related which dataset
        # step 4, let's find which research subject is related to this observation
        research_subject = await workflow_tool_process.get("basedOn")[0].to_resource()
        print("Step 4, the interested observation is related to this research_subject: ", research_subject)
        # step 4.1, we also can find this observation is generated by which patient
        patient = await composition.get("author")[0].to_resource()
        print("Step 4.1: the observation comes from this patient: ", patient)
        # step 5, now we can know the observation is related to which dataset
        dataset = await research_subject.get("study").to_resource()
        print("Step 5, Now we find the interested observation is related to this dataset: ", dataset)



if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test.test_search_digital_twin())
