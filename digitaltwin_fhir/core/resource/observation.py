from abc import ABC
from .abstract_resource import AbstractResource
from .element import (Meta, Identifier, CodeableConcept, Reference, Period, Timing, Quantity, Range, Ratio, SampledData,
                      Annotation, Coding, Code)
from typing import Optional, List, Literal


class ObservationEffective:
    def __init__(self, effective_date_time: Optional[str] = None, effective_period: Optional[Period] = None,
                 effective_timing: Optional[Timing] = None, effective_instant: Optional[str] = None):
        self.effective_date_time = effective_date_time
        self.effective_period = effective_period
        self.effective_timing = effective_timing
        self.effective_instant = effective_instant

    def get(self):
        effective = {
            "effectiveDateTime": self.effective_date_time if isinstance(self.effective_date_time, str) else None,
            "effectivePeriod": self.effective_period.get() if isinstance(self.effective_period, Period) else None,
            "effectiveTiming": self.effective_timing.get() if isinstance(self.effective_timing, Timing) else None,
            "effectiveInstant": self.effective_instant if isinstance(self.effective_instant, str) else None
        }
        return {k: v for k, v in effective.items() if v not in ("", None)}


class ObservationValue:

    def __init__(self, value_quantity: Optional[Quantity] = None,
                 value_codeable_concept: Optional[CodeableConcept] = None, value_string: Optional[str] = None,
                 value_boolean: Optional[bool] = None, value_integer: Optional[int] = None,
                 value_range: Optional[Range] = None, value_ratio: Optional[Ratio] = None,
                 value_sampled_data: Optional[SampledData] = None, value_time: Optional[str] = None,
                 value_date_time: Optional[str] = None, value_period: Optional[Period] = None):
        self.value_quantity = value_quantity
        self.value_codeable_concept = value_codeable_concept
        self.value_string = value_string
        self.value_boolean = value_boolean
        self.value_integer = value_integer
        self.value_range = value_range
        self.value_ratio = value_ratio
        self.value_sampled_data = value_sampled_data
        self.value_time = value_time
        self.value_date_time = value_date_time
        self.value_period = value_period

    def set(self, key, value):
        if key == "valueQuantity":
            self.value_quantity = Quantity(value=value.get("value"), unit=value.get("unit"), system=value.get("system"),
                                           code=Code(value=value.get("code")))
        elif key == "valueCodeableConcept":
            self.value_codeable_concept = CodeableConcept(
                codings=[
                    Coding(code=Code(value=c.get("code")), version=c.get("version"), display=c.get("display"),
                           user_selected=c.get("userSelected"))
                    for c in value.get("coding", [])], text=value.get("text"))
        elif key == "valueString":
            self.value_string = value
        elif key == "valueBoolean":
            self.value_boolean = value
        elif key == "valueInteger":
            self.value_integer = value
        elif key == "valueRange":
            self.value_range = Range(low=value.get("low"), high=value.get("high"))
        elif key == "valueRatio":
            self.value_ratio = Ratio(
                numerator=Quantity(value=value.get("numerator").get("value"), unit=value.get("numerator").get("unit"),
                                   system=value.get("numerator").get("system"),
                                   code=value.get("numerator").get("code")),
                denominator=Quantity(value=value.get("denominator").get("value"),
                                     unit=value.get("denominator").get("unit"),
                                     system=value.get("denominator").get("system"),
                                     code=value.get("denominator").get("code")))
        elif key == "valueSampledData":
            self.value_sampled_data = SampledData(origin=value.get("origin"), period=value.get("period"),
                                                  dimensions=value.get("dimensions"), data=value.get("data"),
                                                  lower_limit=value.get("lowerLimit"),
                                                  upper_limit=value.get("upperLimit"), factor=value.get("factor"))
        elif key == "valueTime":
            self.value_time = value
        elif key == "valueDateTime":
            self.value_date_time = value
        elif key == "valuePeriod":
            self.value_period = Period(start=value.get("start"), end=value.get("end"))

    def get(self):
        value = {
            "valueQuantity": self.value_quantity.get() if isinstance(self.value_quantity, Quantity) else None,
            "valueCodeableConcept": self.value_codeable_concept.get() if isinstance(self.value_codeable_concept,
                                                                                    CodeableConcept) else None,
            "valueString": self.value_string if isinstance(self.value_string, str) else None,
            "valueBoolean": self.value_boolean if isinstance(self.value_boolean, bool) else None,
            "valueInteger": self.value_integer if isinstance(self.value_integer, int) else None,
            "valueRange": self.value_range.get() if isinstance(self.value_range, Range) else None,
            "valueRatio": self.value_ratio.get() if isinstance(self.value_ratio, Ratio) else None,
            "valueSampledData": self.value_sampled_data.get() if isinstance(self.value_sampled_data,
                                                                            SampledData) else None,
            "valueTime": self.value_time if isinstance(self.value_time, str) else None,
            "valueDateTime": self.value_date_time if isinstance(self.value_date_time, str) else None,
            "valuePeriod": self.value_period.get() if isinstance(self.value_period, Period) else None
        }
        return {k: v for k, v in value.items() if v not in ("", None)}


class ObservationReferenceRange:
    def __init__(self, low: Optional[str] = None, high: Optional[str] = None,
                 reference_range_type: Optional[CodeableConcept] = None,
                 applies_to: Optional[List[CodeableConcept]] = None, age: Optional[Range] = None,
                 text: Optional[str] = None):
        self.low = low
        self.high = high
        self.reference_range_type = reference_range_type
        self.applies_to = applies_to
        self.age = age
        self.text = text

    def get(self):
        reference_range = {
            "low": self.low if isinstance(self.low, str) else None,
            "high": self.high if isinstance(self.high, str) else None,
            "type": self.reference_range_type.get() if isinstance(self.reference_range_type, CodeableConcept) else None,
            "appliesTo": [a.get() for a in self.applies_to if isinstance(a, CodeableConcept)] if isinstance(
                self.applies_to, list) else None,
            "age": self.age.get() if isinstance(self.age, Range) else None,
            "text": self.text if isinstance(self.text, str) else None
        }
        return {k: v for k, v in reference_range.items() if v not in ("", None, [])}


class ObservationComponent:
    def __init__(self, code: CodeableConcept, value: Optional[ObservationValue] = None,
                 data_absent_reason: Optional[CodeableConcept] = None,
                 interpretation: Optional[List[CodeableConcept]] = None,
                 reference_range: Optional[List[ObservationReferenceRange]] = None):
        self.code = code
        self.value = value
        self.data_absent_reason = data_absent_reason
        self.interpretation = interpretation
        self.reference_range = reference_range

    def get(self):
        component = {
            "code": self.code.get() if isinstance(self.code, CodeableConcept) else None,
            "valueQuantity": self.value.get().get("valueQuantity") if isinstance(self.value,
                                                                                 ObservationValue) else None,
            "valueCodeableConcept": self.value.get().get("valueCodeableConcept") if isinstance(self.value,
                                                                                               ObservationValue) else None,
            "valueString": self.value.get().get("valueString") if isinstance(self.value,
                                                                             ObservationValue) else None,
            "valueBoolean": self.value.get().get("valueBoolean") if isinstance(self.value,
                                                                               ObservationValue) else None,
            "valueInteger": self.value.get().get("valueInteger") if isinstance(self.value,
                                                                               ObservationValue) else None,
            "valueRange": self.value.get().get("valueRange") if isinstance(self.value,
                                                                           ObservationValue) else None,
            "valueRatio": self.value.get().get("valueRatio") if isinstance(self.value,
                                                                           ObservationValue) else None,
            "valueSampledData": self.value.get().get("valueSampledData") if isinstance(self.value,
                                                                                       ObservationValue) else None,
            "valueTime": self.value.get().get("valueTime") if isinstance(self.value,
                                                                         ObservationValue) else None,
            "valueDateTime": self.value.get().get("valueDateTime") if isinstance(self.value,
                                                                                 ObservationValue) else None,
            "valuePeriod": self.value.get().get("valuePeriod") if isinstance(self.value,
                                                                             ObservationValue) else None,
            "dataAbsentReason": self.data_absent_reason.get() if isinstance(self.data_absent_reason,
                                                                            CodeableConcept) else None,
            "interpretation": [i.get() for i in self.interpretation if isinstance(i, CodeableConcept)] if isinstance(
                self.interpretation, list) else None,
            "referenceRange": [r.get() for r in self.reference_range if
                               isinstance(r, ObservationReferenceRange)] if isinstance(self.reference_range,
                                                                                       list) else None
        }
        return {k: v for k, v in component.items() if v not in ("", None, [])}


class Observation(AbstractResource, ABC):

    def __init__(self, status: Literal["registered", "preliminary", "final", "amended"], code: CodeableConcept,
                 meta: Optional[Meta] = None, identifier: Optional[List[Identifier]] = None,
                 based_on: Optional[List[Reference]] = None, part_of: Optional[List[Reference]] = None,
                 category: Optional[List[CodeableConcept]] = None, subject: Optional[Reference] = None,
                 focus: Optional[List[Reference]] = None, encounter: Optional[Reference] = None,
                 effective: Optional[ObservationEffective] = None, issued: Optional[str] = None,
                 performer: Optional[List[Reference]] = None, value: Optional[ObservationValue] = None,
                 data_absent_reason: Optional[CodeableConcept] = None,
                 interpretation: Optional[List[CodeableConcept]] = None, note: Optional[List[Annotation]] = None,
                 body_site: Optional[CodeableConcept] = None, method: Optional[CodeableConcept] = None,
                 specimen: Optional[Reference] = None, device: Optional[Reference] = None,
                 reference_range: Optional[List[ObservationReferenceRange]] = None,
                 has_member: Optional[List[Reference]] = None, derived_from: Optional[List[Reference]] = None,
                 component: Optional[List[ObservationComponent]] = None):
        super().__init__(meta, identifier)
        self._resource_type = "Observation"
        self.status = status
        self.code = code
        self.based_on = based_on
        self.part_of = part_of
        self.category = category
        self.subject = subject
        self.focus = focus
        self.encounter = encounter
        self.effective = effective
        self.issued = issued
        self.performer = performer
        self.value = value
        self.data_absent_reason = data_absent_reason
        self.interpretation = interpretation
        self.note = note
        self.body_site = body_site
        self.method = method
        self.specimen = specimen
        self.device = device
        self.reference_range = reference_range
        self.has_member = has_member
        self.derived_from = derived_from
        self.component = component

    def get(self):
        observation = {
            "resourceType": self._resource_type,
            "meta": self.meta.get() if isinstance(self.meta, Meta) else None,
            "identifier": [i.get() for i in self.identifier if
                           isinstance(i, Identifier)] if isinstance(self.identifier, list) else None,
            "basedOn": [b.get() for b in self.based_on if isinstance(b, Reference)] if isinstance(self.based_on,
                                                                                                  list) else None,
            "partOf": [p.get() for p in self.part_of if isinstance(p, Reference)] if isinstance(self.part_of,
                                                                                                list) else None,
            "status": self.status if self.status in ["registered", "preliminary", "final", "amended"] else None,
            "category": [c.get() for c in self.category if isinstance(c, CodeableConcept)] if isinstance(self.category,
                                                                                                         list) else None,
            "code": self.code.get() if isinstance(self.code, CodeableConcept) else None,
            "subject": self.subject.get() if isinstance(self.subject, Reference) else None,
            "focus": [f.get() for f in self.focus if isinstance(f, Reference)] if isinstance(self.focus,
                                                                                             list) else None,
            "encounter": self.encounter.get() if isinstance(self.encounter, Reference) else None,
            "effectiveDateTime": self.effective.get().get("effectiveDateTime") if isinstance(self.effective,
                                                                                             ObservationEffective) else None,
            "effectivePeriod": self.effective.get().get("effectivePeriod") if isinstance(self.effective,
                                                                                         ObservationEffective) else None,
            "effectiveTiming": self.effective.get().get("effectiveTiming") if isinstance(self.effective,
                                                                                         ObservationEffective) else None,
            "effectiveInstant": self.effective.get().get("effectiveInstant") if isinstance(self.effective,
                                                                                           ObservationEffective) else None,
            "issued": self.issued if isinstance(self.issued, str) else None,
            "performer": [p.get() for p in self.performer if isinstance(p, Reference)] if isinstance(self.performer,
                                                                                                     list) else None,
            "valueQuantity": self.value.get().get("valueQuantity") if isinstance(self.value,
                                                                                 ObservationValue) else None,
            "valueCodeableConcept": self.value.get().get("valueCodeableConcept") if isinstance(self.value,
                                                                                               ObservationValue) else None,
            "valueString": self.value.get().get("valueString") if isinstance(self.value,
                                                                             ObservationValue) else None,
            "valueBoolean": self.value.get().get("valueBoolean") if isinstance(self.value,
                                                                               ObservationValue) else None,
            "valueInteger": self.value.get().get("valueInteger") if isinstance(self.value,
                                                                               ObservationValue) else None,
            "valueRange": self.value.get().get("valueRange") if isinstance(self.value,
                                                                           ObservationValue) else None,
            "valueRatio": self.value.get().get("valueRatio") if isinstance(self.value,
                                                                           ObservationValue) else None,
            "valueSampledData": self.value.get().get("valueSampledData") if isinstance(self.value,
                                                                                       ObservationValue) else None,
            "valueTime": self.value.get().get("valueTime") if isinstance(self.value,
                                                                         ObservationValue) else None,
            "valueDateTime": self.value.get().get("valueDateTime") if isinstance(self.value,
                                                                                 ObservationValue) else None,
            "valuePeriod": self.value.get().get("valuePeriod") if isinstance(self.value,
                                                                             ObservationValue) else None,
            "dataAbsentReason": self.data_absent_reason if isinstance(self.data_absent_reason,
                                                                      CodeableConcept) else None,
            "interpretation": [i.get() for i in self.interpretation if isinstance(i, CodeableConcept)] if isinstance(
                self.interpretation, list) else None,
            "note": [n.get() for n in self.note if isinstance(n, Annotation)] if isinstance(self.note, list) else None,
            "bodySite": self.body_site.get() if isinstance(self.body_site, CodeableConcept) else None,
            "method": self.method.get() if isinstance(self.method, CodeableConcept) else None,
            "specimen": self.specimen.get() if isinstance(self.specimen, Reference) else None,
            "device": self.device.get() if isinstance(self.device, Reference) else None,
            "referenceRange": [r.get() for r in self.reference_range if
                               isinstance(r, ObservationReferenceRange)] if isinstance(self.reference_range,
                                                                                       list) else None,
            "hasMember": [h.get() for h in self.has_member if isinstance(h, Reference)] if isinstance(self.has_member,
                                                                                                      list) else None,
            "derivedFrom": [d.get() for d in self.derived_from if isinstance(d, Reference)] if isinstance(
                self.derived_from, list) else None,
            "component": [c.get() for c in self.component if isinstance(c, ObservationComponent)] if isinstance(
                self.component, list) else None
        }
        return {k: v for k, v in observation.items() if v not in ("", None, [])}

    def convert(self, fhirpy_resource):
        pass
