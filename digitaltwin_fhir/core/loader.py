import json
import sys
from pathlib import Path
class Loader:
    def __init__(self, client):
        self.client = client

    async def _import_bundle(self, filename):
        with open(filename, encoding='utf-8') as fd:
            patient_json = json.load(fd)
        bundle = self.client.resource('Bundle')
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
