from abc import ABC
from .digital_twins import AbstractDigitalTWINBase
from datetime import datetime, timezone
from digitaltwin_on_fhir.core.utils import transform_value
from digitaltwin_on_fhir.core.resource import (Identifier, ObservationValue, Observation, CodeableConcept,
                                               Code, Coding, Reference, Task, TaskInputOutput, Composition,
                                               CompositionSection)
from .knowledgebase import DIGITALTWIN_ON_FHIR_SYSTEM
from typing import Dict, Any, List


class WorkflowToolProcess(AbstractDigitalTWINBase, ABC):
    def __init__(self, core, operator):
        self.descriptions: Dict[str, Any] = {}
        self.cda_descriptions = None

        super().__init__(core, operator)

    def add_workflow_tool_process_description(self, descriptions):
        """
        :param descriptions: json format data
        :return:
        """
        if not isinstance(descriptions, (dict, list)):
            raise ValueError("description must be json format data")
        if not isinstance(descriptions.get("process"), dict):
            raise ValueError(
                "description must be SPARC Clinic Description Annotator Workflow tool process json format data")
        self.cda_descriptions = descriptions
        return self._generate_workflow_tool_process_via_cda_descriptions()

    def _generate_workflow_tool_process_via_cda_descriptions(self):
        process = self.cda_descriptions.get("process")
        self.descriptions = {
            "workflow": {
                "uuid": process.get("workflow"),
                "reference": None,
            },
            "workflow_tool": {
                "uuid": process.get("workflow_tool"),
                "reference": None,
            },
            "research_study": {
                "uuid": process.get("dataset"),
                "reference": None,
            },
            "processes": []
        }

        for p in process.get("patients"):
            process = {
                "uuid": p.get("process_uuid"),
                "patient": {
                    "uuid": p.get("patient_uuid"),
                    "reference": None,
                },
                "research_subject": {
                    "reference": None,
                },
                "date": p.get("date"),
                "input": p.get("input"),
                "output": p.get("output"),
                "composition": {
                    "uuid": f"{p.get('patient_uuid')}-{p.get('process_uuid')}-composition",
                }
            }
            self.descriptions["processes"].append(process)
        return self

    async def generate_resources(self):
        await self._generate_related_references()
        for p in self.descriptions["processes"]:
            await self._generate_task_outputs(p)
            await self._generate_task(p)
            await self._generate_composition(p)
        return self

    async def _generate_related_references(self):
        research_study_resource = await self.get_resource("ResearchStudy", self.descriptions["research_study"]["uuid"])
        workflow_resource = await self.get_resource("PlanDefinition", self.descriptions["workflow"]["uuid"])
        workflow_tool_resource = await self.get_resource("ActivityDefinition",
                                                         self.descriptions["workflow_tool"]["uuid"])
        self.descriptions["workflow"]["reference"] = Reference(
            reference=workflow_resource.to_reference().reference, display=workflow_resource.get("name"))
        self.descriptions["workflow_tool"]["reference"] = Reference(
            reference=workflow_tool_resource.to_reference().reference, display=workflow_tool_resource.get("name"))
        for p in self.descriptions.get("processes"):
            patient_resource = await self.get_resource("Patient", p["patient"]["uuid"])
            p["patient"]["reference"] = Reference(patient_resource.to_reference().reference, display="Patient")

            research_subject_resource = await self.client.resources("ResearchSubject").search(
                patient=patient_resource.to_reference().reference,
                study=research_study_resource.to_reference().reference).first()
            p["research_subject"]["reference"] = Reference(research_subject_resource.to_reference().reference,
                                                           display="ResearchSubject")

    async def _generate_task_outputs(self, process):
        outputs = process.get("output")
        if len(outputs) == 0:
            return
        for idx, output in enumerate(outputs):
            if output.get("resource_type") != "Observation":
                print("The output value only supports Observation at this stage")
                continue
            identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                    value=f"{self.descriptions.get('workflow_tool').get('uuid')}-{process.get('uuid')}-{output.get('resource_type')}-{idx}")
            value_keys = output.get("value").keys()
            value_key = list(value_keys)[0]
            ob_value = ObservationValue()
            ob_value.set(key=value_key, value=output.get("value").get(value_key))

            ob = Observation(identifier=[identifier],
                             status="final",
                             code=CodeableConcept(
                                 codings=[
                                     Coding(
                                         system=output.get("codeSystem"),
                                         code=Code(value=output.get("code")),
                                         display=output.get("display"))],
                                 text=output.get("display")),
                             value=ob_value,
                             subject=process.get("patient").get("reference"),
                             focus=[self.descriptions.get("workflow_tool").get("reference")]
                             )

            resource = await self.operator.create(ob).save()
            output.update({"reference": Reference(reference=resource.to_reference().reference,
                                                  display=output.get("resource_type"))})

    async def _generate_task(self, process):
        """
        FHIR Task Resource:
            owner: patient reference
            for: workflow reference
            focus: workflow tool reference
            basedOn: research subject reference
            requester (Optional): practitioner reference
        """
        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                value=process.get("uuid"))
        task_input = []
        task_output = []
        if len(process.get("input")) > 0:
            for i in process.get("input"):
                resource = await self.get_resource(i.get("resource_type"), i.get("uuid"))
                task_input.append(TaskInputOutput(
                    CodeableConcept(
                        codings=[
                            Coding(system="http://hl7.org/fhir/resource-types",
                                   code=Code(value=i.get("resource_type")),
                                   display=i.get("resource_type"))],
                        text=i.get("resource_type")),
                    value=Reference(reference=resource.to_reference().reference, display=i.get("resource_type"))
                ))
        if len(process.get("output")) > 0:
            for o in process.get("output"):
                task_output.append(TaskInputOutput(
                    CodeableConcept(
                        codings=[
                            Coding(system="http://hl7.org/fhir/resource-types",
                                   code=Code(value=o.get("resource_type")),
                                   display=o.get("resource_type"))],
                        text=o.get("resource_type")),
                    value=o.get("reference")
                ))
        task = Task(identifier=[identifier], status="accepted", intent="unknown",
                    description=f"Workflow process for {self.descriptions.get('workflow_tool').get('reference').get().get('display')}",
                    authored_on=process.get("date"),
                    last_modified=process.get("date"),
                    based_on=[process.get("research_subject").get("reference")],
                    owner=process.get("patient").get("reference"),
                    task_for=self.descriptions.get("workflow").get("reference"),
                    focus=self.descriptions.get("workflow_tool").get("reference"),
                    task_input=task_input,
                    task_output=task_output)

        resource = await self.operator.create(task).save()
        process.update(
            {"reference": Reference(reference=resource.to_reference().reference, display="Workflow Tool Process")})

    async def _generate_composition(self, process):
        """
        Composition Resource:
            author: Patient reference
            subject: Task (workflow tool process) reference
            section:
                entry: Observations
                focus: ActivityDefinition (workflow tool) reference

        """
        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                value=process.get("composition").get("uuid"))

        entry = [ob.get("reference") for ob in process.get("output")]

        c = Composition(
            identifier=[identifier],
            status="final",
            composition_type=CodeableConcept(codings=[
                Coding(system=DIGITALTWIN_ON_FHIR_SYSTEM, code=Code(value="workflow tool results"),
                       display="workflow tool results")], text="workflow tool results"),
            title="workflow tool results",
            date=transform_value(datetime.now(timezone.utc)),
            subject=process.get("reference"),
            author=[process.get("patient").get("reference")],
            section=[CompositionSection(
                title="workflow tool results",
                focus=self.descriptions.get("workflow_tool").get("reference"),
                entry=entry,
            )]
        )
        resource = await self.operator.create(c).save()
        process["composition"]["reference"] = Reference(reference=resource.to_reference().reference,
                                                        display="Workflow Tool Result Composition")
