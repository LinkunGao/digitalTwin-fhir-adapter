from typing import List, Optional, Literal
from ..utils import transform_value


class Code:
    def __init__(self, value: str = ""):
        self.value = value

    def get(self):
        return self.value


class Coding:

    def __init__(self, system: str = "", version: str = "", code: Code = None, display: str = "",
                 user_selected: bool = ""):
        self.system = system
        self.version = version
        self.code = code
        self.display = display
        self.user_selected = user_selected

    def get(self):
        coding = {
            "system": self.system,
            "version": self.version,
            "code": self.code.get() if isinstance(self.code, Code) else None,
            "display": self.display,
            "userSelected": self.user_selected
        }
        return {k: v for k, v in coding.items() if v not in ("", None)}


class CodeableConcept:

    def __init__(self, codings: List[Coding] = None, text: str = ""):
        self.codings = codings
        self.text = text

    def get(self):
        codeableconcept = {
            "coding": [coding.get() for coding in self.codings if isinstance(coding, Coding)],
            "text": self.text
        }

        return {k: v for k, v in codeableconcept.items() if v not in ("", None)}


class Period:

    def __init__(self, start: str = '', end: str = ''):
        self.start = transform_value(start)
        self.end = transform_value(end)

    def get(self):
        period = {
            "start": self.start,
            "end": self.end
        }
        return {k: v for k, v in period.items() if v not in ("", None)}


class Reference:

    def __init__(self, reference: str = "", display: str = ""):
        self.reference = reference
        self.display = display

    def get(self):
        reference = {
            "reference": self.reference,
            "display": self.display
        }
        return {k: v for k, v in reference.items() if v not in ("", None)}


class Identifier:

    def __init__(self, use: Code = None, system: str = "", value: str = "", period: Period = None,
                 assigner: Reference = None):
        self.use = use
        self.system = system
        self.value = value
        self.period = period if isinstance(period, Period) else None
        self.assigner = assigner if isinstance(assigner, Reference) else None

    def get(self):
        identifier = {
            "use": self.use,
            "system": self.system,
            "value": self.value,
            "period": self.period,
            "assigner": self.assigner
        }

        return {k: v for k, v in identifier.items() if v not in ("", None)}


class Profile:

    def __init__(self, url):
        self.url = url

    def get(self):
        return self.url


class Meta:

    def __init__(self, profile: List[Profile] = None):
        self.profile = profile

    def get(self):
        meta = {
            "profile": self.profile
        }
        return {k: v for k, v in meta.items() if v not in ("", None)}


class HumanName:

    def __init__(self, use: Literal["usual", "official", "temp", "nickname", "anonymous", "old", "maiden", ""] = "",
                 text: str = "", family: str = "", given: List[str] = None,
                 prefix: List[str] = None, suffix: List[str] = None, period: Optional[Period] = None):
        self.use = use
        self.text = text
        self.family = family
        self.given = given
        self.prefix = prefix
        self.suffix = suffix
        self.period = period

    def get(self):
        name = {
            "use": self.use,
            "text": self.text,
            "family": self.family,
            "given": self.given,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "period": self.period
        }
        return {k: v for k, v in name.items() if v not in ("", None)}


class ContactPoint:

    def __init__(self, system: Literal["phone", "fax", "email", "pager", "url", "sms", "other", ""] = "",
                 value: str = "", use: Literal["home", "work", "temp", "old", "mobile", ""] = "",
                 rank: Optional[int] = None,
                 period: Optional[Period] = None):
        self.system = system
        self.value = value
        self.use = use
        self.rank = rank
        self.period = period

    def get(self):
        contactpoint = {
            "system": self.system,
            "value": self.value,
            "use": self.use,
            "rank": self.rank,
            "period": self.period
        }
        return {k: v for k, v in contactpoint.items() if v not in ("", None)}


class Address:

    def __init__(self, use: Literal["home", "work", "temp", "old", "billing", ""] = "", text: str = "",
                 line: List[str] = None, city: str = "", district: str = "", state: str = "", postal_code: str = "",
                 country: str = "", period: Optional[Period] = None):
        self.use = use
        self.text = text
        self.line = line
        self.city = city
        self.district = district
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.period = period

    def get(self):
        address = {
            "use": self.use,
            "text": self.text,
            "line": self.line,
            "city": self.city,
            "district": self.district,
            "state": self.state,
            "postalCode": self.postal_code,
            "country": self.country,
            "period": self.period.get() if isinstance(self.period, Period) else None
        }

        return {k: v for k, v in address.items() if v not in ("", None)}


class Attachment:

    def __init__(self, content_type: Optional[Code] = None, language: Optional[Code] = None, data: str = "",
                 url: str = "", size: Optional[int] = None, hash: str = "", title: str = "", creation: str = ""):
        self.content_type = content_type
        self.language = language
        self.data = data
        self.url = url
        self.size = size
        self.hash = hash
        self.title = title
        self.creation = creation

    def get(self):
        attachment = {
            "contentType": self.content_type.get() if isinstance(self.content_type, Code) else None,
            "language": self.language.get() if isinstance(self.language, Code) else None,
            "data": self.data,
            "url": self.url,
            "size": self.size,
            "hash": self.hash,
            "title": self.title,
            "creation": self.creation
        }
        return {k: v for k, v in attachment.items() if v not in ("", None)}
