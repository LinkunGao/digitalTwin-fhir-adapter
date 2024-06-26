import json
import sys
from pathlib import Path
from abc import ABC, abstractmethod
from .resource import Code, Coding, CodeableConcept


class AbstractCRUD(ABC):
    core = None
    operator = None

    def __init__(self, operator, core):
        self.operator = operator
        self.core = core


class Loader(AbstractCRUD):

    def __init__(self, operator, core):
        super().__init__(operator, core)

    async def _import_bundle(self, filename):
        with open(filename, encoding='utf-8') as fd:
            patient_json = json.load(fd)
        bundle = self.core.async_client.resource('Bundle')
        bundle['type'] = 'transaction'
        bundle['entry'] = patient_json['entry']
        await bundle.save()

    async def import_dataset(self, dataset_path):
        sys.stdout.write("Import progress: 0%   \r")

        dataset_root = Path(dataset_path)

        filenames = [
            filename.name for filename in dataset_root.iterdir()
            if filename.name.endswith('.json')]

        total_count = len(filenames)
        for index, filename in enumerate(filenames):
            await self._import_bundle(dataset_root / filename)
            progress = int(float(index + 1) / float(total_count) * 100)
            sys.stdout.write("Import progress: %d%%   \r" % progress)
            sys.stdout.flush()
        sys.stdout.write("Import progress: 100%\n")
        sys.stdout.write("{0} bundles imported".format(total_count))


class Create(AbstractCRUD):
    def __init__(self, operator, core):
        self.resource = None
        super().__init__(operator, core)

    async def create_resource(self, resource_type, identifier, **kwargs):
        is_exist = await self._is_resource_exist(resource_type, identifier)
        if is_exist:
            return
        self.resource = self._create_resource(resource_type, identifier)
        for k, v in kwargs:
            self.resource[k] = v
        return self

    async def update_reference(self, **kwargs):
        if self.resource is None:
            return


    def save(self):
        self.resource.save()



    def _create_resource(self, resource_type, identifier, system="http://sparc.sds.dataset"):
        resource = self.core.sync_client.resource(resource_type)

        resource['identifier'] = [
            {
                "use": "official",
                "system": system,
                "value": identifier
            }
        ]
        return resource

    async def _is_resource_exist(self, resource_type, identifier):
        resources = await self.core.search().search_resource(resource_type=resource_type, identifier=identifier)
        if len(resources) > 0:
            print(f"the {resource_type} already exist! identifier: {identifier}")
            return True
        return False
