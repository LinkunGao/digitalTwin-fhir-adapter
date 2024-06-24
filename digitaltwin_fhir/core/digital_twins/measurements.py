from abc import ABC, abstractmethod
from .digital_twins import AbstractDigitalTWINBase
import pandas as pd
from pathlib import Path
import uuid
from pprint import pprint
from digitaltwin_fhir.core.resource import (
    Code, Coding, CodeableConcept, ResearchStudy, Identifier,
    Practitioner
)
from .knowledgebase import DIGITALTWIN_ON_FHIR_SYSTEM


class Measurements(AbstractDigitalTWINBase, ABC):

    def __init__(self, operator, dataset_path):
        self.dataset_info = None
        super().__init__(operator)
        self._analysis_dataset(dataset_path)

    def _analysis_dataset(self, dataset_path):
        dataset_path = Path(dataset_path)
        print(dataset_path)
        primary_folder = dataset_path / "primary"
        mapping_file = dataset_path / "mapping.xlsx"

        if mapping_file.exists():
            self.dataset_info = {}
        else:
            return

        df = pd.read_excel(mapping_file)
        self.dataset_info["research_study"] = {
            "id": df["dataset_id"].unique().tolist()[0],
            "uuid": df["dataset_uuid"].unique().tolist()[0],
            "path": dataset_path,
            "resource": None
        }
        self.dataset_info["group"] = {
            "uuid": df["dataset_uuid"].unique().tolist()[0] + "_" + str(uuid.uuid4()),
            "resource": None
        }
        self.dataset_info["practitioner"] = {
            "uuid": "",
            "resource": None
        }
        self.dataset_info["patients"] = []

        # Generate patients information - Identifier
        for pid, puid in zip(df["subject_id"].unique().tolist(), df["subject_uuid"].unique().tolist()):
            self.dataset_info["patients"].append({
                "uuid": puid,
                "resource": None,
                "path": primary_folder / pid,
                "appointment": {
                    "uuid": self.dataset_info["research_study"]["uuid"] + "_" + puid + "_" + str(uuid.uuid4()),
                    "resource": None
                },
                "encounter": {
                    "uuid": self.dataset_info["research_study"]["uuid"] + "_" + puid + "_" + str(uuid.uuid4()),
                    "resource": None
                },
                "imaging_study": [],
                "observation": []
            })

        # Generate ImagingStudy information - identifier, endpoint
        for p in self.dataset_info["patients"]:
            temp_df = df[df["subject_uuid"] == p["uuid"]]
            image_studies = temp_df["(DUKE) Subject UID"].unique().tolist()
            for image_id in image_studies:
                p["imaging_study"].append({
                    "id": image_id,
                    "uuid": p["uuid"] + "_" + image_id,
                    "resource": None,
                    "path": p["path"] / image_id,
                    "endpoint": {
                        "uuid":p["uuid"] + "_" + image_id + "_" + str(uuid.uuid4()),
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
                            "uuid": p["uuid"] + "_" + s_id + str(uuid.uuid4()),
                            "resource": None
                        }
                    })

    async def add_practitioner(self, researcher: Practitioner):
        self.dataset_info["practitioner"]["resource"] = await self.operator.create(researcher).save()

    async def generate_resources(self):
        # Generate ResearchStudy
        # await self._generate_research_study()
        # # Generate Patient
        # await self._generate_patients()

        pprint(self.dataset_info)

    async def _generate_research_study(self):
        identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=self.dataset_info["dataset_uuid"])
        research_study = ResearchStudy(status="active", identifier=[identifier])
        self.research_study = await self.operator.create(research_study).save()

    async def _generate_patients(self):
        self.patients = []
        for p in self.dataset_info["patients"]:
            identifier = Identifier(system=DIGITALTWIN_ON_FHIR_SYSTEM, value=p["patient_uuid"])
