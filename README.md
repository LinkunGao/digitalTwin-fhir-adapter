# Digitaltwins on FHIR

## Usage

- Setup and connect to FHIR server

```python
from digitaltwins_on_fhir.core import Adapter

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

await measurements.add_measurements_description(data).generate_resources()
```
- Add Practitioner (researcher) to FHIR server

```python
from digitaltwins_on_fhir.core.resource import Identifier, Code, HumanName, Practitioner

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
#### References in Task (workflow tool process) resource
- owner: `Patient` reference
- for: `PlanDefinition` (workflow) reference
- focus: `ActivityDefinition` (workflow tool) reference
- basedOn: `ResearchSubject` reference
- requester (Optional): `Practitioner` (researcher) reference
- references in input
  - ImagingStudy
  - Observation
- references in output
  - Observation

###### Example

- Find a specific workflow process
  - If known: patient, dataset, workflow tool and workflow uuids

```python
client = adapter.async_client

# Step 1: find the patient
patient = await client.resources("Patient").search(
                                    identifier="patient-xxxx").first()
# Step 2: find the dataset
dataset = await client.resources("ResearchStudy").search(
                                    identifier="dataset-xxxx").first()
# Step 3: find the workflow tool
workflow_tool = await client.resources("ActivityDefinition").search(
                                    identifier="workflow-tool-xxxx").first()
# Step 4: find the research subject
research_subject = await client.resources("ResearchSubject").search(
                                    patient=patient.to_reference().reference,
                                    study=dataset.to_reference().reference).first()
# Step 5: find workflow
workflow = await client.resources("PlanDefinition").search(
                                    identifier="sparc-workflow-uuid-001").first()
workflow_tool_process = await client.resources("Task").search(
                                    subject=workflow.to_reference(),
                                    focus=workflow_tool.to_reference(),
                                    based_on=research_subject.to_reference(),
                                    owner=patient.to_reference()).first()
```
- Find all input resources of the workflow tool process
```python
inputs = workflow_tool_process.get("input")
for i in inputs:
    input_reference = i.get("valueReference")
    input_resource = await input_reference.to_resource()
```
- Find the input data comes from with dataset
  - Assume we don't know the dataset and patient uuids at this stage
```python
composition = await client.resources("Composition").search(
                                    title="primary measurements", 
                                    entry=input_reference).first()
dataset = await composition.get("subject").to_resource()
```

- Find all output resources of the workflow tool process
```python
outputs = workflow_tool_process.get("output")
for output in outputs:
    output_reference = output.get("valueReference")
    output_resource = await output_reference.to_resource()
```

#### References in PlanDefinition (workflow) resource
- action
  - definition_canonical: ActivityDefinition (workflow tool) reference

###### Example
- If known workflow uuid
  - Find all related workflow tools
    ```python
    workflow = await client.resources("PlanDefinition").search(
                                        identifier="sparc-workflow-uuid-001").first()
    actions = workflow.get("action")
    
    for a in actions:
        if a.get("definitionCanonical") is None:
            continue
        resource_type, _id = a.get("definitionCanonical").split("/")
        workflow_tool = await client.reference(resource_type, _id).to_resource()
    ```
  - Find all related workflow processes
    ```python
    workflow_tool_processes = await client.resources("Task").search(
                                        subject=workflow.to_reference()).fetch_all()
    ```
## Reference in resource
- `Patient`
  - generalPractitioner: [ Practitioner reference ]
- `ResearchSubject`
  - individual(patient): Patient reference
  - study: ResearchStudy reference
  - consent: Consent reference
- `ResearchStudy`
  - principalInvestigator: Practitioner reference
- `Composition` - primary measurements
  - author: [ Patient reference, Practitioner reference ]
  - subject: ResearchStudy reference
  - entry: [ Observation reference, ImagingStudy reference]
- `ImagingStudy`
  - subject: Patient reference
  - endpoint: [ Endpoint Reference ]
  - referrer: Practitioner reference
- `Observation` - primary measurements
  - subject: Patient reference
- `PlanDefinition`:
  - action.definitionCanonical: ActivityDefinition reference string
- `ActivityDefinition`:
  - participant: [ software uuid, model uuid]
- `Task`:
  - owner: patient reference 
  - for(subject): workflow reference
  - focus: workflow tool reference
  - basedOn: research subject reference
  - requester (Optional): practitioner reference
  - input: [ Observation reference, ImagingStudy reference ]
  - output: [ Observation reference, ImagingStudy reference ]
- `Composition` - workflow tool result
  - author: Patient reference
  - subject: Task (workflow tool process) reference
  - section:
    - entry: Observations
    - focus: ActivityDefinition (workflow tool) reference
- `Observation` - workflow tool result
  - focus: [ActivityDefinition reference]

## DigitalTWIN on FHIR Diagram
![DigitalTWIN on FHIR](https://copper3d-brids.github.io/ehr-docs/fhir/03-roadmap/vlatest.png)