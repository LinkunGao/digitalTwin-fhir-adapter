from abc import ABC
from .abstract_resource import AbstractResource
from .element import (Meta, Identifier, CodeableConcept, ContactDetail, Reference, UsageContext, RelatedArtifact,
                      Period, Timing,
                      Quantity, Range)
from typing import Optional, List, Literal


class PlanDefinitionSubject:
    def __init__(self, subject_codeable_concept: Optional[CodeableConcept] = None,
                 subject_reference: Optional[Reference] = None):
        self.subject_codeable_concept = subject_codeable_concept
        self.subject_reference = subject_reference

    def get(self):
        subject = {
            "subjectCodeableConcept": self.subject_codeable_concept.get() if isinstance(self.subject_codeable_concept,
                                                                                        CodeableConcept) else None,
            "subjectReference": self.subject_reference.get() if isinstance(self.subject_reference, Reference) else None
        }
        return {k: v for k, v in subject.items() if v not in ("", None)}


class PlanDefinitionTargetDetail:
    def __init__(self, detail_quantity: Optional[Quantity] = None, detail_range: Optional[Range] = None,
                 detail_codeable_concept: Optional[CodeableConcept] = None):
        self.detail_quantity = detail_quantity
        self.detail_range = detail_range
        self.detail_codeable_concept = detail_codeable_concept

    def get(self):
        detail = {
            "detailQuantity": self.detail_quantity.get() if isinstance(self.detail_quantity, Quantity) else None,
            "detailRange": self.detail_range.get() if isinstance(self.detail_range, Range) else None,
            "detailCodeableConcept": self.detail_codeable_concept.get() if isinstance(self.detail_codeable_concept,
                                                                                      CodeableConcept) else None
        }
        return {k: v for k, v in detail.items() if v not in ("", None)}


class PlanDefinitionTarget:

    def __init__(self, measure: Optional[CodeableConcept] = None, detail: Optional[PlanDefinitionTargetDetail] = None,
                 due: Optional[str] = None):
        self.measure = measure
        self.detail = detail
        self.due = due

    def get(self):
        target = {
            "measure": self.measure.get() if isinstance(self.measure, CodeableConcept) else None,
            "detailQuantity": self.detail.get().get("detailQuantity") if isinstance(self.detail,
                                                                                    PlanDefinitionTargetDetail) else None,
            "detailRange": self.detail.get().get("detailRange") if isinstance(self.detail,
                                                                              PlanDefinitionTargetDetail) else None,
            "detailCodeableConcept": self.detail.get().get("detailCodeableConcept") if isinstance(self.detail,
                                                                                                  PlanDefinitionTargetDetail) else None,
            "due": self.due if isinstance(self.due, str) else None
        }
        return {k: v for k, v in target.items() if v not in ("", None)}


class PlanDefinitionGoal:

    def __init__(self, description: CodeableConcept, category: Optional[CodeableConcept] = None,
                 priority: Optional[CodeableConcept] = None, start: Optional[CodeableConcept] = None,
                 addresses: Optional[List[CodeableConcept]] = None,
                 documentation: Optional[List[RelatedArtifact]] = None,
                 target: Optional[List[PlanDefinitionTarget]] = None):
        self.description = description
        self.category = category
        self.priority = priority
        self.start = start
        self.addresses = addresses
        self.documentation = documentation
        self.target = target

    def get(self):
        goal = {
            "category": self.category.get() if isinstance(self.category, CodeableConcept) else None,
            "description": self.description.get() if isinstance(self.description, CodeableConcept) else None,
            "priority": self.priority.get() if isinstance(self.priority, CodeableConcept) else None,
            "start": self.start.get() if isinstance(self.start, CodeableConcept) else None,
            "addresses": [a.get() for a in self.addresses if isinstance(a, CodeableConcept)] if isinstance(
                self.addresses, list) else None,
            "documentation": [d.get() for d in self.documentation if isinstance(d, RelatedArtifact)] if isinstance(
                self.documentation, list) else None,
            "target": [t.get() for t in self.target if isinstance(t, PlanDefinitionTarget)] if isinstance(self.target,
                                                                                                          list) else None
        }
        return {k: v for k, v in goal.items() if v not in ("", None, [])}


class PlanDefinitionAction:
    def __init__(self, prefix: Optional[str] = None, title: Optional[str] = None, description: Optional[str] = None,
                 text_equivalent: Optional[str] = None,
                 priority: Optional[Literal["routine", "urgent", "asap", "stat"]] = None,
                 code: Optional[List[CodeableConcept]] = None, reason: Optional[List[CodeableConcept]] = None,
                 documentation: Optional[List[RelatedArtifact]] = None, goal_id: Optional[List[str]] = None,
                 subject: Optional[PlanDefinitionSubject] = None):
        pass


class PlanDefinition(AbstractResource, ABC):

    def __init__(self, status: Literal["draft", "active", "retired", "unknown"], meta: Optional[Meta] = None,
                 identifier: Optional[List[Identifier]] = None,
                 url: Optional[str] = None, version: Optional[str] = None, name: Optional[str] = None,
                 title: Optional[str] = None, subtitle: Optional[str] = None,
                 plan_definition_type: Optional[CodeableConcept] = None, experimental: Optional[bool] = None,
                 subject: Optional[PlanDefinitionSubject] = None, date: Optional[str] = None,
                 contact: Optional[List[ContactDetail]] = None, description: Optional[str] = None,
                 use_context: Optional[List[UsageContext]] = None,
                 jurisdiction: Optional[List[CodeableConcept]] = None, purpose: Optional[str] = None,
                 usage: Optional[str] = None, copyright: Optional[str] = None, approval_date: Optional[str] = None,
                 last_review_date: Optional[str] = None, effective_period: Optional[str] = None,
                 topic: Optional[List[CodeableConcept]] = None, author: Optional[List[ContactDetail]] = None,
                 editor: Optional[List[ContactDetail]] = None, reviewer: Optional[List[ContactDetail]] = None,
                 endorser: Optional[List[ContactDetail]] = None,
                 related_artifact: Optional[List[RelatedArtifact]] = None, library: Optional[List[str]] = None, ):
        super().__init__(meta, identifier)
