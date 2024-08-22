from pathlib import Path
from digitaltwin_on_fhir.core.resource import AbstractResource
from abc import ABC, abstractmethod


class AbstractDigitalTWINBase(ABC):
    operator = None

    def __init__(self, operator):
        self.operator = operator

    # async def _get_existing_resource(self, resource: AbstractResource):
    #     if resource.identifier is None or len(resource.identifier) == 0:
    #         return
    #     resources = await self.operator.core.search().search_resource_async(resource_type=resource.resource_type,
    #                                                                         identifier=resource.identifier[0]["value"])
    #     return resources
