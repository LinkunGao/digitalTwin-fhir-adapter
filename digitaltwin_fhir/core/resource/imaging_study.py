from abc import ABC
from .abstract_resource import AbstractResource
from .element import (Meta, Identifier, Annotation, Coding, CodeableConcept, Reference)
from typing import Optional, List, Literal


class ImagingStudyPerformer:
    def __init__(self, actor: Reference, function: Optional[CodeableConcept] = None):
        self.actor = actor
        self.function = function

    def get(self):
        performer = {
            "function": self.function.get() if isinstance(self.function, CodeableConcept) else None,
            "actor": self.actor.get() if isinstance(self.actor, Reference) else None
        }

        return {k: v for k, v in performer.items() if v not in ("", None)}


class ImagingStudyInstance:

    def __init__(self, uid: str, sop_class: Coding, number: Optional[int], title: Optional[str]):
        self.uid = uid
        self.sop_class = sop_class
        self.number = number
        self.title = title

    def get(self):
        instance = {
            "uid": self.uid if isinstance(self.uid, str) else None,
            "sopClass": self.sop_class.get() if isinstance(self.sop_class, Coding) else None,
            "number": self.number if isinstance(self.number, int) and self.number >= 0 else None,
            "title": self.title if isinstance(self.title, str) else None
        }
        return {k: v for k, v in instance.items() if v not in ("", None)}


class ImagingStudySeries:

    def __init__(self, uid: str, modality: Coding, number: Optional[int] = None, description: Optional[str] = None,
                 number_of_instances: Optional[int] = None, endpoint: Optional[List[Reference]] = None,
                 body_site: Optional[Coding] = None, laterality: Optional[Coding] = None,
                 specimen: Optional[List[Reference]] = None, started: Optional[str] = None,
                 performer: Optional[List[ImagingStudyPerformer]] = None,
                 instance: Optional[List[ImagingStudyInstance]] = None):
        self.uid = uid
        self.modality = modality
        self.number = number
        self.description = description
        self.number_of_instances = number_of_instances
        self.endpoint = endpoint
        self.body_site = body_site
        self.laterality = laterality
        self.specimen = specimen
        self.started = started
        self.performer = performer
        self.instance = instance

    def get(self):
        series = {
            "uid": self.uid if isinstance(self.uid, str) else None,
            "number": self.number if isinstance(self.number, int) and self.number >= 0 else None,
            "modality": self.modality.get() if isinstance(self.modality, Coding) else None,
            "description": self.description if isinstance(self.description, str) else None,
            "numberOfInstances": self.number_of_instances if isinstance(self.number_of_instances,
                                                                        int) and self.number_of_instances >= 0 else None,
            "endpoint": [e.get() for e in self.endpoint if isinstance(e, Reference)] if isinstance(self.endpoint,
                                                                                                   list) else None,
            "bodySite": self.body_site.get() if isinstance(self.body_site, Coding) else None,
            "laterality": self.laterality.get() if isinstance(self.laterality, Coding) else None,
            "specimen": [s.get() for s in self.specimen if isinstance(s, Reference)] if isinstance(self.specimen,
                                                                                                   list) else None,
            "started": self.started if isinstance(self.started, str) else None,
            "performer": [p.get() for p in self.performer if isinstance(p, ImagingStudyPerformer)] if isinstance(
                self.performer, list) else None,
            "instance": [i.get() for i in self.instance if isinstance(i, ImagingStudyInstance)] if isinstance(
                self.instance, list) else None
        }
        return {k: v for k, v in series.items() if v not in ("", None, [])}


class ImagingStudy(AbstractResource, ABC):

    def __init__(self, status: Literal["registered", "available", "cancelled", "entered-in-error", "unknown"],
                 subject: Reference, meta: Optional[Meta] = None, identifier: Optional[List[Identifier]] = None,
                 modality: Optional[List[Coding]] = None, encounter: Optional[Reference] = None,
                 started: Optional[str] = None, based_on: Optional[List[Reference]] = None,
                 referrer: Optional[Reference] = None, interpreter: Optional[List[Reference]] = None,
                 endpoint: Optional[List[Reference]] = None, number_of_series: Optional[int] = None,
                 number_of_instances: Optional[int] = None, procedure_reference: Optional[Reference] = None,
                 procedure_code: Optional[List[CodeableConcept]] = None, location: Optional[Reference] = None,
                 reason_code: Optional[List[CodeableConcept]] = None,
                 reason_reference: Optional[List[Reference]] = None, note: Optional[List[Annotation]] = None,
                 description: Optional[str] = None, series: Optional[List[ImagingStudySeries]] = None):
        super().__init__(meta, identifier)
        self.status = status
        self.subject = subject
        self.modality = modality
        self.encounter = encounter
        self.started = started
        self.based_on = based_on
        self.referrer = referrer
        self.interpreter = interpreter
        self.endpoint = endpoint
        self.number_of_series = number_of_series
        self.number_of_instances = number_of_instances
        self.procedure_reference = procedure_reference
        self.procedure_code = procedure_code
        self.location = location
        self.reason_code = reason_code
        self.reason_reference = reason_reference
        self.note = note
        self.description = description
        self.series = series

    def get(self):
        imagingstudy = {
            "meta": self.meta.get() if isinstance(self.meta, Meta) else None,
            "identifier": [i.get() for i in self.identifier if
                           isinstance(i, Identifier)] if isinstance(self.identifier, list) else None,
            "status": self.status if self.status in ["registered", "available", "cancelled", "entered-in-error",
                                                     "unknown"] else None,
            "modality": [m.get() for m in self.modality if isinstance(m, Coding)] if isinstance(self.modality,
                                                                                                list) else None,
            "subject": self.subject.get() if isinstance(self.subject, Reference) else None,
            "encounter": self.encounter.get() if isinstance(self.encounter, Reference) else None,
            "started": self.started if isinstance(self.started, str) else None,
            "basedOn": [b.get() for b in self.based_on if isinstance(b, Reference)] if isinstance(self.based_on,
                                                                                                  list) else None,
            "referrer": self.referrer.get() if isinstance(self.referrer, Reference) else None,
            "interpreter": [i.get() for i in self.interpreter if isinstance(i, Reference)] if isinstance(
                self.interpreter, list) else None,
            "endpoint": [e.get() for e in self.endpoint if isinstance(e, Reference)] if isinstance(self.endpoint,
                                                                                                   list) else None,
            "numberOfSeries": self.number_of_series if isinstance(self.number_of_series,
                                                                  int) and self.number_of_series >= 0 else None,
            "numberOfInstances": self.number_of_instances if isinstance(self.number_of_instances,
                                                                        int) and self.number_of_instances >= 0 else None,
            "procedureReference": self.procedure_reference.get() if isinstance(self.procedure_reference,
                                                                               Reference) else None,
            "procedureCode": [pc.get() for pc in self.procedure_code if
                              isinstance(self.procedure_code, CodeableConcept)] if isinstance(self.procedure_code,
                                                                                              list) else None,
            "location": self.location.get() if isinstance(self.location, Reference) else None,
            "reasonCode": [r.get() for r in self.reason_code if isinstance(r, CodeableConcept)] if isinstance(
                self.reason_code, list) else None,
            "reasonReference": [r.get() for r in self.reason_reference if isinstance(r, CodeableConcept)] if isinstance(
                self.reason_reference, list) else None,
            "note": [n.get() for n in self.note if isinstance(n, Annotation)] if isinstance(self.note, list) else None,
            "description": self.description if isinstance(self.description, str) else None,
            "series": [s.get() for s in self.series if isinstance(s, ImagingStudySeries)] if isinstance(self.series,
                                                                                                        list) else None
        }

        return {k: v for k, v in imagingstudy.items() if v not in ("", None, [])}

    def convert(self):
        pass
