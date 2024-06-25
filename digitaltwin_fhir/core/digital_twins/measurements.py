from abc import ABC, abstractmethod
from .digital_twins import AbstractDigitalTWINBase
import pandas as pd
from pathlib import Path
import uuid
from pprint import pprint
from digitaltwin_fhir.core.resource import (
    Code, Coding, CodeableConcept, ResearchStudy, Identifier,
    Practitioner, Patient, Group, GroupMember, GroupValue, Characteristic, Reference, Appointment,
    AppointmentParticipant, Encounter, Endpoint
)
from .knowledgebase import DIGITALTWIN_ON_FHIR_SYSTEM


class Measurements(AbstractDigitalTWINBase, ABC):

    def __init__(self, operator, dataset_path):
        self.primary_measurements = None
        # self._duplicate_upload = False
        super().__init__(operator)
        self._analysis_dataset(dataset_path)

    def _analysis_dataset(self, dataset_path):
        dataset_path = Path(dataset_path)
        primary_folder = dataset_path / "primary"
        mapping_file = dataset_path / "mapping.xlsx"

        if mapping_file.exists():
            self.primary_measurements = {}
        else:
            return

        df = pd.read_excel(mapping_file)
        self.primary_measurements["research_study"] = {
            "id": df["dataset_id"].unique().tolist()[0],
            "uuid": df["dataset_uuid"].unique().tolist()[0],
            "path": dataset_path,
            "resource": None
        }
        self.primary_measurements["group"] = {
            "uuid": df["dataset_uuid"].unique().tolist()[0] + "_" + "group",
            "resource": None
        }
        self.primary_measurements["practitioner"] = {
            "uuid": "",
            "resource": None
        }
        self.primary_measurements["patients"] = []

        # Generate patients information - Identifier
        for pid, puid in zip(df["subject_id"].unique().tolist(), df["subject_uuid"].unique().tolist()):
            self.primary_measurements["patients"].append({
                "uuid": puid,
                "resource": None,
                "path": primary_folder / pid,
                "appointment": {
                    "uuid": self.primary_measurements["research_study"]["uuid"] + "_" + puid + "_" + "appointment",
                    "resource": None
                },
                "encounter": {
                    "uuid": self.primary_measurements["research_study"]["uuid"] + "_" + puid + "_" + "encounter",
                    "resource": None
                },
                "imaging_study": [],
                "observation": []
            })

        # Generate ImagingStudy information - identifier, endpoint
        for p in self.primary_measurements["patients"]:
            temp_df = df[df["subject_uuid"] == p["uuid"]]
            image_studies = temp_df["(DUKE) Subject UID"].unique().tolist()
            for image_id in image_studies:
                p["imaging_study"].append({
                    "id": image_id,
                    "uuid": p["uuid"] + "_" + image_id,
                    "resource": None,
                    "path": p["path"] / image_id,
                    "endpoint": {
                        "uuid": p["uuid"] + "_" + image_id + "_" + "study-endpoint",
                        "resource": None
                    },
                    "series": []
                })
            # Generate Imagingstudy series information: series number, instance number
            for image in p["imaging_study"]:
                sample_ids = temp_df["sample_id"].unique().tolist()
                sample_uuids = temp_df["sample_uuid"].unique().tolist()
                sample_duke_ids = temp_df["(DUKE) Series UID"].unique().tolist()
                for s_id, s_uuid, s_duke_ids in zip(sample_ids, sample_uuids, sample_duke_ids):
                    image["series"].append({
                        "id": s_id,
                        "series_id": s_duke_ids,
                        "series_uuid": s_uuid,
                        "path": image["path"] / s_id,
                        "endpoint": {
                            "uuid": p["uuid"] + "_" + s_id + "sample-endpoint",
                            "resource": None
                        }
                    })

    async def add_practitioner(self, researcher: Practitioner):
        practitioner = await self.operator.create(researcher).save()
        if practitioner is None:
            return
        self.primary_measurements["practitioner"]["uuid"] = practitioner["identifier"][0]["value"]
        self.primary_measurements["practitioner"]["resource"] = practitioner
        return self

    async def generate_resources(self):
        if self.primary_measurements["practitioner"]["resource"] is None:
            print("Please provide researcher/practitioner info first!")
            return
            # Generate ResearchStudy
        await self._generate_research_study()
        # Generate Patient
        await self._generate_patients()
        # Generate Group
        await self._generate_group()
        # Generate Patient's Appointment and Encounter
        await self._generate_appointment_encounter()

        pprint(self.primary_measurements)
        return self

    async def _generate_research_study(self):
        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                value=self.primary_measurements["research_study"]["uuid"])
        research_study = ResearchStudy(status="active", identifier=[identifier])
        resource = await self.operator.create(research_study).save()
        self.primary_measurements["research_study"]["resource"] = resource

    async def _generate_patients(self):
        self.patients = []
        practitioner = self.primary_measurements["practitioner"]["resource"]
        for p in self.primary_measurements["patients"]:
            identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["uuid"])
            patient = Patient(active=True, identifier=[identifier], general_practitioner=[
                Reference(reference=practitioner.to_reference().reference,
                          display=practitioner["name"][0]["text"] if "name" in practitioner else "")])
            resource = await self.operator.create(patient).save()
            p["resource"] = resource

    async def _generate_group(self):
        research_study = self.primary_measurements["research_study"]["resource"]
        practitioner = self.primary_measurements["practitioner"]["resource"]

        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=self.primary_measurements["group"]["uuid"])
        group = Group(group_type="person",
                      identifier=[identifier],
                      active=True,
                      characteristic=[Characteristic(
                          code=CodeableConcept(
                              codings=[Coding(code=Code(self.primary_measurements["research_study"]["id"]))],
                              text="dataset group member"),
                          value=GroupValue(value_reference=Reference(
                              reference=research_study.to_reference().reference, display="Original dataset")
                          ),
                      )],
                      managing_entity=Reference(
                          reference=practitioner.to_reference().reference,
                          display=practitioner["name"][0]["text"] if "name" in practitioner else ""),
                      member=[])

        for p in self.primary_measurements["patients"]:
            group.member.append(GroupMember(entity=Reference(reference=p["resource"].to_reference().reference,
                                                             display=p["resource"]["name"][0]["text"] if "name" in p[
                                                                 "resource"] else "")))
        resource = await self.operator.create(group).save()
        self.primary_measurements["group"]["resource"] = resource

    async def _generate_appointment_encounter(self):
        research_study = self.primary_measurements["research_study"]["resource"]
        practitioner = self.primary_measurements["practitioner"]["resource"]
        for p in self.primary_measurements["patients"]:
            ai = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["appointment"]["uuid"])
            ei = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["encounter"]["uuid"])
            appointment = Appointment(status="fulfilled", identifier=[ai], supporting_information=[
                Reference(reference=research_study.to_reference().reference, display="Original dataset")],
                                      participant=[
                                          AppointmentParticipant(status="accepted", actor=Reference(
                                              reference=practitioner.to_reference().reference,
                                              display=practitioner["name"][0]["text"] if "name" in practitioner else ""
                                          )),
                                          AppointmentParticipant(status="accepted", actor=Reference(
                                              reference=p["resource"].to_reference().reference,
                                              display=p["resource"]["name"][0]["text"] if "name" in p[
                                                  "resource"] else ""
                                          ))
                                      ])
            appointment_resource = await self.operator.create(appointment).save()
            p["appointment"]["resource"] = appointment_resource

            encounter = Encounter(status="finished", identifier=[ei],
                                  encounter_class=Coding(code=Code("VR"), system=DIGITALTWIN_ON_FHIR_SYSTEM),
                                  subject=Reference(
                                      reference=p["resource"].to_reference().reference,
                                      display=p["resource"]["name"][0]["text"] if "name" in p[
                                          "resource"] else ""
                                  ),
                                  appointment=[Reference(reference=appointment_resource.to_reference().reference)])
            encounter_resource = await self.operator.create(encounter).save()
            p["encounter"]["resource"] = encounter_resource
