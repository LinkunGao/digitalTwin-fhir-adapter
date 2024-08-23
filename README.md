# digitalTwinOnFHIR

## Usage

- Setup and connect to FHIR server

```python
from digitaltwin_on_fhir.core import Adapter

adapter = Adapter("http://localhost:8080/fhir/")
```

### Load data to FHIR server

#### Primary measurements

- Load FHIR bundle
```python
 await adapter.loader().load_fhir_bundle('./dataset/dataset-fhir-bundles')
```
- Load DigitalTWIN Clinical Description (primary measurements)
```python
measurements = adapter.loader().load_sparc_dataset_primary_measurements()
with open('./dataset/measurements.json', 'r') as file:
    data = json.load(file)

await measurements.add_measurements_description(data)
        .generate_measurements_via_cda_descriptions()
        .generate_resources()
```
- Add Practitioner (researcher) to FHIR server

```python
from digitaltwin_on_fhir.core.resource import Identifier, Code, HumanName, Practitioner

await measurements.add_practitioner(researcher=Practitioner(
    active=True,
    identifier=[
        Identifier(use=Code("official"), system="sparc.org",
                   value='sparc-d557ac68-f365-0718-c945-8722ec')],
    name=[HumanName(use="usual", text="Xiaoming Li", family="Li", given=["Xiaoming"])],
    gender="male"
))
```

#### Workflow

### Search

## DigitalTWIN on FHIR Diagram
![DigitalTWIN on FHIR](https://copper3d-brids.github.io/ehr-docs/fhir/03-roadmap/v1.0.0.png)