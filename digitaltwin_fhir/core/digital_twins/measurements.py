from abc import ABC, abstractmethod
from .digital_twins import AbstractDigitalTWINBase
import pandas as pd
from pathlib import Path
import pydicom
from pydicom.uid import UID
from datetime import datetime
import uuid
from pprint import pprint
from digitaltwin_fhir.core.resource import (
    Code, Coding, CodeableConcept, ResearchStudy, Identifier,
    Practitioner, Patient, Group, GroupMember, GroupValue, Characteristic, Reference, Appointment,
    AppointmentParticipant, Encounter, Endpoint, ImagingStudy, ImagingStudySeries, ImagingStudyInstance
)
from .knowledgebase import DIGITALTWIN_ON_FHIR_SYSTEM, SNOMEDCT


class Measurements(AbstractDigitalTWINBase, ABC):

    def __init__(self, operator, dataset_path):
        self.primary_measurements = None
        self._practitioner = None
        self._practitioner_ref = None
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
                    "path": p["path"],
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
        self.primary_measurements["practitioner"]["resource"] = self._practitioner = practitioner
        self.primary_measurements["practitioner"][
            "reference"] = self._practitioner_ref = practitioner.to_reference().reference
        return self

    async def generate_resources(self):
        if self.primary_measurements["practitioner"]["resource"] is None:
            print("Please provide researcher/practitioner info first! - via add_practitioner method")
            return

        # Generate ResearchStudy
        await self._generate_research_study()
        # Generate Patient
        await self._generate_patients()
        # Generate Group
        await self._generate_group()
        # Generate Patient's Appointment and Encounter
        await self._generate_appointment_encounter()
        # Generate Patient's ImagingStudy
        await self._generate_imaging_study()

        pprint(self.primary_measurements["patients"][0]["imaging_study"])
        return self

    async def _generate_research_study(self):
        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                value=self.primary_measurements["research_study"]["uuid"])
        research_study = ResearchStudy(status="active", identifier=[identifier])
        resource = await self.operator.create(research_study).save()
        self.primary_measurements["research_study"]["resource"] = resource
        self.primary_measurements["research_study"]["reference"] = resource.to_reference().reference

    async def _generate_patients(self):
        self.patients = []
        for p in self.primary_measurements["patients"]:
            identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["uuid"])
            patient = Patient(active=True, identifier=[identifier], general_practitioner=[
                Reference(reference=self._practitioner_ref,
                          display=self._practitioner["name"][0]["text"] if "name" in self._practitioner else "")])
            resource = await self.operator.create(patient).save()
            p["resource"] = resource
            p["reference"] = resource.to_reference().reference

    async def _generate_group(self):
        research_study_ref = self.primary_measurements["research_study"]["reference"]

        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=self.primary_measurements["group"]["uuid"])
        group = Group(group_type="person",
                      identifier=[identifier],
                      active=True,
                      characteristic=[Characteristic(
                          code=CodeableConcept(
                              codings=[Coding(code=Code(research_study_ref))],
                              text="dataset group member"),
                          value=GroupValue(value_reference=Reference(
                              reference=research_study_ref, display="Original dataset")
                          ),
                      )],
                      managing_entity=Reference(
                          reference=self._practitioner_ref,
                          display=self._practitioner["name"][0]["text"] if "name" in self._practitioner else ""),
                      member=[])

        for p in self.primary_measurements["patients"]:
            group.member.append(GroupMember(entity=Reference(reference=p["reference"],
                                                             display=p["resource"]["name"][0]["text"] if "name" in p[
                                                                 "resource"] else "")))
        resource = await self.operator.create(group).save()
        self.primary_measurements["group"]["resource"] = resource
        self.primary_measurements["group"]["reference"] = resource.to_reference().reference

    async def _generate_appointment_encounter(self):
        research_study_ref = self.primary_measurements["research_study"]["reference"]
        for p in self.primary_measurements["patients"]:
            ai = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["appointment"]["uuid"])
            ei = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["encounter"]["uuid"])
            appointment = Appointment(status="fulfilled", identifier=[ai], supporting_information=[
                Reference(reference=research_study_ref, display="Original dataset")],
                                      participant=[
                                          AppointmentParticipant(status="accepted", actor=Reference(
                                              reference=self._practitioner_ref,
                                              display=self._practitioner["name"][0][
                                                  "text"] if "name" in self._practitioner else ""
                                          )),
                                          AppointmentParticipant(status="accepted", actor=Reference(
                                              reference=p["reference"],
                                              display=p["resource"]["name"][0]["text"] if "name" in p[
                                                  "resource"] else ""
                                          ))
                                      ])
            appointment_resource = await self.operator.create(appointment).save()
            p["appointment"]["resource"] = appointment_resource
            p["appointment"]["reference"] = appointment_resource.to_reference().reference

            encounter = Encounter(status="finished", identifier=[ei],
                                  encounter_class=Coding(code=Code("VR"), system=DIGITALTWIN_ON_FHIR_SYSTEM),
                                  subject=Reference(
                                      reference=p["reference"],
                                      display=p["resource"]["name"][0]["text"] if "name" in p[
                                          "resource"] else ""
                                  ),
                                  appointment=[Reference(reference=p["appointment"]["reference"])])
            encounter_resource = await self.operator.create(encounter).save()
            p["encounter"]["resource"] = encounter_resource
            p["encounter"]["reference"] = encounter_resource.to_reference().reference

    async def _generate_imaging_study(self):
        """
            (0020, 000d) Study Instance UID
            (0020, 000e) Series Instance UID
            (0008, 0018) SOP Instance UID
            (0020, 0013) Instance Number
            (0008,0016) SOP Class UID
            (0008, 0030) Study Time
            (0020,1208) Number of Study Related Instances
            (0020,1206) Number of Study Related Series
            (0020,1209) Number of Series Related Instances
            (0018, 0010) Contrast/Bolus Agent                LO: 'Magnevist'
            (0018, 0015) Body Part Examined                  CS: 'BREAST'
        """
        for p in self.primary_measurements["patients"]:
            for image in p["imaging_study"]:
                endpoint_image = self._generate_endpoint(identifier_value=image["endpoint"]["uuid"],
                                                         url="http://where?")
                endpoint_image_resource = await self.operator.create(endpoint_image).save()
                image["endpoint"]["resource"] = endpoint_image_resource
                image["endpoint"]["reference"] = endpoint_image_resource.to_reference().reference

                # Generate imaging series
                result = await self._generate_imaging_study_series(image["series"])

                # Generate ImagingStudy resources based on first dicom file

                dcm = next(image["series"][0]["path"].glob('*.dcm'), None)
                dicom_file = pydicom.dcmread(dcm)

                study_uid = dicom_file[(0x0020, 0x000d)].value

                try:
                    dicom_study_time = dicom_file[(0x0008, 0x0030)].value
                    started_time = datetime.strptime(dicom_study_time, "%H%M%S.%f").strftime("%Y-%m-%dT%H:%M:%S")
                except:
                    started_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                try:
                    number_of_series = int(dicom_file[(0x0020, 0x1206)].value)
                except:
                    number_of_series = len(image["series"])

                try:
                    number_of_instances = int(dicom_file[(0x0020, 0x1208)].value)
                except:
                    number_of_instances = result["number_of_instances"]

                identifier = Identifier(system="urn:dicom:uid", value=image["uuid"])
                imaging_study = ImagingStudy(identifier=[identifier],
                                             status="available",
                                             started=started_time,
                                             subject=Reference(reference=p["reference"],
                                                               display=p["resource"]["name"][0]["text"] if "name" in p[
                                                                   "resource"] else None),
                                             encounter=Reference(reference=p["encounter"]["reference"]),
                                             endpoint=[Reference(reference=image["endpoint"]["reference"],
                                                                 display="Imaging Study Endpoint")],
                                             referrer=Reference(reference=self._practitioner_ref,
                                                                display=self._practitioner["name"][0][
                                                                    "text"] if "name" in self._practitioner else ""),
                                             number_of_series=number_of_series,
                                             number_of_instances=number_of_instances,
                                             series=result["series"]
                                             )
                imaging_study_resource = await self.operator.create(imaging_study).save()
                image["resource"] = imaging_study_resource
                image["reference"] = imaging_study_resource.to_reference().reference

    async def _generate_imaging_study_series(self, series):
        series_components = []
        number_of_instances = 0
        for s in series:
            dcm_files = list(s["path"].glob('*.dcm'))
            dcm_file_count = len(dcm_files)
            number_of_instances += dcm_file_count
            endpoint_series = self._generate_endpoint(identifier_value=s["endpoint"]["uuid"],
                                                      url="https://where.the.series?")
            endpoint_image_resource = await self.operator.create(endpoint_series).save()
            s["endpoint"]["resource"] = endpoint_image_resource
            s["endpoint"]["reference"] = endpoint_image_resource.to_reference().reference

            # Generate ImagingStudy series instances
            instances = self._generate_imaging_study_instance(dcm_files)

            s_dcm = next(s["path"].glob("*.dcm"), None)
            s_dicom_file = pydicom.dcmread(s_dcm)

            body_part_examined = s_dicom_file.get((0x0018, 0x0015), 'Not Found')

            try:
                body_site = SNOMEDCT[body_part_examined.value.upper()]
            except KeyError:
                body_site = None

            try:
                number_of_series_instances = int(s_dicom_file[(0x0020, 0x1209)].value)
            except KeyError:
                number_of_series_instances = dcm_file_count

            series_component = ImagingStudySeries(
                uid=s_dicom_file[(0x0020, 0x000e)].value,
                modality=Coding(
                    system="http://dicom.nema.org/resources/ontology/DCM",
                    code=Code("MR")),
                number_of_instances=number_of_series_instances,
                endpoint=[Reference(reference=s["endpoint"]["reference"], display="Series Endpoint")],
                body_site=Coding(code=Code(body_site["code"]), display=body_site["display"],
                                 system=body_site["system"]) if body_site is not None else None,
                instance=instances
            )
            series_components.append(series_component)
        return {
            "number_of_instances": number_of_instances,
            "series": series_components
        }

    @staticmethod
    def _generate_imaging_study_instance(dcm_files):
        instance_components = []
        for d in dcm_files:
            dcm = pydicom.dcmread(d)

            # Get the SOP Class UID
            sop_class_uid = dcm.SOPClassUID
            # Get the SOP Class Name using the UID dictionary
            sop_class_name = UID(sop_class_uid).name

            instance = ImagingStudyInstance(
                uid=dcm[(0x0008, 0x0018)].value,
                sop_class=Coding(code=Code(sop_class_uid), display=sop_class_name),
                number=dcm[(0x0020, 0x0013)].value
            )
            instance_components.append(instance)
        return instance_components

    @staticmethod
    def _generate_endpoint(identifier_value, url):
        return Endpoint(status="active",
                        identifier=[Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM,
                                               value=identifier_value)],
                        connection_type=Coding(code=Code("dicom-wado-rs"),
                                               display="DICOM WADO-RS"),
                        address=url,
                        payload_type=[CodeableConcept(codings=[
                            Coding(code=Code("urn:ihe:pat:apsr:cancer:breast:2010"),
                                   display="Anatomic Pathology Structured Report Cancer Breast")])])
