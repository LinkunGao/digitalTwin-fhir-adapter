from abc import ABC

from .AbstractResource import AbstractResource
from .Element import Meta, Identifier, HumanName, ContactPoint, Address, CodeableConcept, Attachment, Reference, Period
from typing import Optional, List, Literal


class Deceased:
    def __init__(self, deceased_boolean: bool, deceased_date_time: str):
        self.deceased_boolean = deceased_boolean,
        self.deceased_date_time = deceased_date_time

    def get(self):
        deceased = {
            "deceasedBoolean": self.deceased_boolean,
            "deceasedDateTime": self.deceased_date_time
        }
        return {k: v for k, v in deceased.items() if v not in ("", None)}


class MultipleBrith:

    def __init__(self, multiple_birth_boolean: bool, multiple_birth_integer: int):
        self.multiple_birth_boolean = multiple_birth_boolean,
        self.multiple_birth_integer = multiple_birth_integer

    def get(self):
        multiple_brith = {
            "multipleBirthBoolean": self.multiple_birth_boolean,
            "multipleBirthInteger": self.multiple_birth_integer
        }
        return {k: v for k, v in multiple_brith.items() if v not in ("", None)}


class Contact:

    def __init__(self, relationship: Optional[List[CodeableConcept]] = None, name: Optional[HumanName] = None,
                 telecom: Optional[List[ContactPoint]] = None, address: Optional[Address] = None,
                 gender: Optional[Literal["male", "female", "other", "unknown", ""]] = None,
                 organization: Optional[Reference] = None, period: Optional[Period] = None):
        self.relationship = relationship
        self.name = name
        self.telecom = telecom
        self.address = address
        self.gender = gender
        self.organization = organization
        self.period = period

    def get(self):
        contact = {
            "relationship": [r.get() for r in self.relationship if isinstance(r, CodeableConcept)],
            "name": self.name.get() if isinstance(self.name, HumanName) else None,
            "telecom": [t.get() for t in self.telecom if isinstance(t, ContactPoint)],
            "address": self.address.get() if isinstance(self.address, Address) else None,
            "gender": self.gender,
            "organization": self.organization.get() if isinstance(self.organization, Reference) else None,
            "period": self.period.get() if isinstance(self.period, Period) else None
        }
        return {k: v for k, v in contact.items() if v not in ("", None)}


class Communication:

    def __init__(self, language: CodeableConcept, preferred: Optional[bool] = None):
        self.language = language
        self.preferred = preferred

    def get(self):
        communication = {
            "language": self.language.get() if isinstance(self.language, CodeableConcept) else None,
            "preferred": self.preferred
        }
        return {k: v for k, v in communication.items() if v not in ("", None)}


class Link:

    def __init__(self, other: Reference, _type: Literal["replaced-by", "replaces", "refer", "seealso"]):
        self.other = other
        self._type = _type

    def get(self):
        link = {
            "other": self.other.get() if isinstance(self.other, Reference) else None,
            "type": self._type
        }
        return {k: v for k, v in link.items() if v not in ("", None)}


class Patient(AbstractResource, ABC):

    def __init__(self, meta: Optional[Meta] = None, identifier: Optional[List[Identifier]] = None,
                 active: Optional[bool] = None, name: Optional[List[HumanName]] = None,
                 telecom: Optional[List[ContactPoint]] = None,
                 gender: Optional[Literal["male", "female", "other", "unknown", ""]] = None,
                 birth_date: Optional[str] = None, address: Optional[List[Address]] = None,
                 marital_status: Optional[CodeableConcept] = None, multiple_brith: Optional[MultipleBrith] = None,
                 photo: Optional[List[Attachment]] = None, contact: Optional[List[Contact]] = None,
                 communication: Optional[List[Communication]] = None,
                 general_practitioner: Optional[List[Reference]] = None,
                 managing_organization: Optional[Reference] = None, link: Optional[List[Link]] = None):
        super().__init__(meta, identifier)
        self.active = active
        self.name = name
        self.telecom = telecom
        self.gender = gender
        self.birth_date = birth_date
        self.address = address
        self.marital_status = marital_status
        self.multiple_brith = multiple_brith
        self.photo = photo
        self.contact = contact
        self.communication = communication
        self.general_practitioner = general_practitioner
        self.managing_organization = managing_organization
        self.link = link

    def get(self):
        patient = {
            "meta": self.meta.get() if isinstance(self.meta, Meta) else None,
            "identifier": [i.get() for i in self.identifier if isinstance(i, Identifier)],
            "active": self.active if isinstance(self.active, bool) else None
        }
