from abc import ABC, abstractmethod


class AbstractSearch(ABC):
    core = None

    def __init__(self, core):
        self.core = core

    @abstractmethod
    def search_resource(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resources(self, resource_type, identifier):
        pass


class Search(AbstractSearch):
    async_client = None

    def __init__(self, core):
        super().__init__(core)
        self.async_client = self.core.async_client

    async def search_resource(self, resource_type, identifier):
        resources_search_set = self.async_client.resources(resource_type)
        searched_resource = await resources_search_set.search(identifier=identifier).first()
        return searched_resource

    async def search_resources(self, resource_type, identifier=None):
        resources_search_set = self.async_client.resources(resource_type)
        if identifier is None:
            resources = await resources_search_set.search().fetch_all()
        else:
            resources = await resources_search_set.search(identifier=identifier).fetch_all()
        return resources
