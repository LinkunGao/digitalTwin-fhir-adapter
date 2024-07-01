from abc import ABC, abstractmethod
from digitaltwin_fhir.core.resource import ImagingStudy, Reference


class AbstractSearch(ABC):
    core = None

    def __init__(self, core):
        self.core = core

    @abstractmethod
    def search_resource_async(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resources_async(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resource_sync(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resources_sync(self, resource_type, identifier):
        pass


class Search(AbstractSearch):
    async_client = None

    def __init__(self, core):
        super().__init__(core)
        self.async_client = self.core.async_client
        self.sync_client = self.core.sync_client

    async def search_resource_async(self, resource_type, identifier):
        resources_search_set = self.async_client.resources(resource_type)
        searched_resource = await resources_search_set.search(identifier=identifier).first()
        return searched_resource

    async def search_resources_async(self, resource_type, identifier=None):
        resources_search_set = self.async_client.resources(resource_type)
        if identifier is None:
            resources = await resources_search_set.search().fetch_all()
        else:
            resources = await resources_search_set.search(identifier=identifier).fetch_all()
        return resources

    def search_resource_sync(self, resource_type, identifier):
        resources_search_set = self.sync_client.resources(resource_type)
        searched_resource = resources_search_set.search(identifier=identifier).first()
        return searched_resource

    def search_resources_sync(self, resource_type, identifier=None):
        resources_search_set = self.sync_client.resources(resource_type)
        if identifier is None:
            resources = resources_search_set.search().fetch_all()
        else:
            resources = resources_search_set.search(identifier=identifier).fetch_all()
        return resources

    async def get_dataset_information(self, dataset_identifier):
        infos = {}

        research_study = await self.search_resource_async("ResearchStudy", dataset_identifier)
        if research_study is None:
            return None
        group_search_set = self.async_client.resources("Group")
        group = await group_search_set.search(
            characteristic_value=research_study.to_reference()).first()
        practitioner = await group["managingEntity"].to_resource()

        infos["dataset"] = research_study
        infos["practitioner"] = practitioner
        infos["group"] = group
        infos["patients"] = []

        for p in group["member"]:
            appointment = await self.async_client.resources("Appointment").search(patient=p["entity"],
                                                                                  supporting_info=research_study.to_reference()).first()
            encounter = await self.async_client.resources("Encounter").search(patient=p["entity"],
                                                                              appointment=appointment.to_reference()).first()
            count_imaging_study = self.sync_client.resources('ImagingStudy').search(
                encounter=encounter.to_reference()).count()
            count_observation = self.sync_client.resources('Observation').search(
                encounter=encounter.to_reference()).count()

            imagings = await self.async_client.resources("ImagingStudy").search(
                encounter=encounter.to_reference()).limit(count_imaging_study).fetch()

            infos["patients"].append({
                "patient": await p["entity"].to_resource(),
                "appointment": appointment,
                "encounter": encounter,
                "observations": await self.async_client.resources("Observation").search(
                    encounter=encounter.to_reference()).limit(count_observation).fetch(),
                "imagingstudies": imagings
                # "imagingstudies": [{"imagingstudy": i, "endpoint": await i["endpoint"][0].to_resource()} for i in
                #                    imagings]
            })

        return infos
