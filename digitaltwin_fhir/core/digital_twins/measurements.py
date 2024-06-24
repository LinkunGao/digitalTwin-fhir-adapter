from abc import ABC, abstractmethod
from .digital_twins import AbstractDigitalTWINBase
import pandas as pd
from pathlib import Path
import uuid
from pprint import pprint
from digitaltwin_fhir.core.resource import (
    Code, Coding, CodeableConcept, ResearchStudy, Identifier
)


class Measurements(AbstractDigitalTWINBase, ABC):

    def __init__(self, operator, dataset_path):
        self.dataset_info = None
        self.measurements = None
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
        self.dataset_info["dataset_uuid"] = df["dataset_uuid"].unique().tolist()[0]
        self.dataset_info["group_uuid"] = df["dataset_uuid"].unique().tolist()[0] + "_" + str(uuid.uuid4())
        self.dataset_info["patients"] = []

        # Generate patients information - Identifier
        for pid, puid in zip(df["subject_id"].unique().tolist(), df["subject_uuid"].unique().tolist()):
            self.dataset_info["patients"].append({
                "patient_uuid": puid,
                "path": primary_folder / pid,
                "appointment_uuid": self.dataset_info["dataset_uuid"] + "_" + puid + "_" + str(uuid.uuid4()),
                "encounter_uuid": self.dataset_info["dataset_uuid"] + "_" + puid + "_" + str(uuid.uuid4()),
                "imagingstudy": [],
                "observation": []
            })

        # Generate ImagingStudy information - identifier, endpoint
        for p in self.dataset_info["patients"]:
            temp_df = df[df["subject_uuid"] == p["patient_uuid"]]
            imagestudies = temp_df["(DUKE) Subject UID"].unique().tolist()
            for image_id in imagestudies:
                p["imagingstudy"].append({
                    "imagingstudy_id": image_id,
                    "imagingstudy_uuid": p["patient_uuid"] + "_" + image_id,
                    "path": p["path"] / image_id,
                    "endpoint_uuid": p["patient_uuid"] + "_" + image_id + "_" + str(uuid.uuid4()),
                    "series": []
                })
            # Generate Imagingstudy series information: series number, instance number
            for image in p["imagingstudy"]:
                sample_ids = temp_df["sample_id"].unique().tolist()
                sample_uuids = temp_df["sample_uuid"].unique().tolist()
                sample_duke_ids = temp_df["(DUKE) Series UID"].unique().tolist()
                for s_id, s_uuid, s_duke_ids in zip(sample_ids, sample_uuids, sample_duke_ids):
                    image["series"].append({
                        "id": s_id,
                        "series_id": s_duke_ids,
                        "series_uuid": s_uuid,
                        "path": image["path"] / s_id,
                        "endpoint_uuid": p["patient_uuid"] + "_" + s_id + str(uuid.uuid4()),
                    })

        # test = {
        #     "dataset_uuid": "dataset-1",
        #     "group_uuid": "dataset-1_group-uuid",
        #     "patients": [
        #         {
        #             "patient_uuid": "p-001",
        #             "appointment_uuid": "dataset-1_p-001_appointment-uuid",
        #             "encounter_uuid": "dataset-1_p-001_encounter-uuid",
        #             "imagingstudy": [
        #                 {
        #                     "id": "p-001_(DUKE) Subject UID",
        #                     "endpoint": "p-001_(DUKE) Subject UID_endpoint_uuid",
        #                     "series": [
        #                         {
        #                             "id": "(DUKE) Series UID",
        #                             "endpoint": "p-001_(DUKE) Series UID_endpoint_uuid",
        #                             "instance": [
        #                                 {
        #                                     "id": "(0008, 0018) SOP Instance UID",
        #                                     "sopClass": ""
        #                                 }
        #                             ]
        #                         }
        #                     ]
        #                 }
        #             ]
        #         }
        #     ]
        # }

    def generate_resources(self):
        self.measurements = {}
        # generate ResearchStudy
        self._generate_research_study()
        # self.operator.create()

        pprint(self.dataset_info)

    def _generate_research_study(self):
        identifier = Identifier(system="")
        research_study = ResearchStudy(status="active", identifier=[])
