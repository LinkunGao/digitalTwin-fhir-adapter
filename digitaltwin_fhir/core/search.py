from abc import ABC, abstractmethod


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
