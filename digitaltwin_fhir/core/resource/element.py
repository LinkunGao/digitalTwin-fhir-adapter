from typing import List, Optional, Literal
from ..utils import transform_value


class Code:
    def __init__(self, value: str = ""):
        self.value = value if isinstance(value, str) else None

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
            "system": self.system if isinstance(self.system, str) else None,
            "version": self.version if isinstance(self.version, str) else None,
            "code": self.code.get() if isinstance(self.code, Code) else None,
            "display": self.display if isinstance(self.display, str) else None,
            "userSelected": self.user_selected if isinstance(self.user_selected, bool) else None
        }
        return {k: v for k, v in coding.items() if v not in ("", None)}


class CodeableConcept:

    def __init__(self, codings: List[Coding] = None, text: str = ""):
        self.codings = codings
        self.text = text

    def get(self):
        codeableconcept = {
            "coding": [coding.get() for coding in self.codings if isinstance(coding, Coding)] if isinstance(
                self.codings, list) else None,
            "text": self.text if isinstance(self.text, str) else None
        }

        return {k: v for k, v in codeableconcept.items() if v not in ("", None, [])}


class Period:

    def __init__(self, start: str = '', end: str = ''):
        self.start = start
        self.end = end

    def get(self):
        period = {
            "start": self.start if isinstance(self.start, str) else None,
            "end": self.end if isinstance(self.end, str) else None
        }
        return {k: v for k, v in period.items() if v not in ("", None)}


class Reference:

    def __init__(self, reference: str = "", display: str = ""):
        self.reference = reference
        self.display = display

    def get(self):
        reference = {
            "reference": self.reference if isinstance(self.reference, str) else None,
            "display": self.display if isinstance(self.display, str) else None
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
            "use": self.use.get() if isinstance(self.use, Code) else None,
            "system": self.system if isinstance(self.system, str) else None,
            "value": self.value if isinstance(self.value, str) else None,
            "period": self.period.get() if isinstance(self.period, Period) else None,
            "assigner": self.assigner.get() if isinstance(self.assigner, Reference) else None
        }

        return {k: v for k, v in identifier.items() if v not in ("", None)}


class Profile:

    def __init__(self, url):
        self.url = url if isinstance(url, str) else None

    def get(self):
        return self.url


class Meta:

    def __init__(self, profile: List[Profile] = None):
        self.profile = profile

    def get(self):
        meta = {
            "profile": [p for p in self.profile if isinstance(p, Profile)] if isinstance(self.profile, list) else None
        }
        return {k: v for k, v in meta.items() if v not in ("", None, [])}


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
            "use": self.use if self.use in ["usual", "official", "temp", "nickname", "anonymous", "old",
                                            "maiden"] else None,
            "text": self.text if isinstance(self.text, str) else None,
            "family": self.family if isinstance(self.family, str) else None,
            "given": [g for g in self.given if isinstance(g, str)] if isinstance(self.given, list) else None,
            "prefix": [p for p in self.prefix if isinstance(p, str)] if isinstance(self.prefix, list) else None,
            "suffix": [s for s in self.suffix if isinstance(s, str)] if isinstance(self.suffix, list) else None,
            "period": self.period.get() if isinstance(self.period, Period) else None
        }
        return {k: v for k, v in name.items() if v not in ("", None, [])}


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
            "system": self.system if self.system in ["phone", "fax", "email", "pager", "url", "sms", "other"] else None,
            "value": self.value if isinstance(self.value, str) else None,
            "use": self.use if self.use in ["home", "work", "temp", "old", "mobile"] else None,
            "rank": self.rank if isinstance(self.rank, int) else None,
            "period": self.period.get() if isinstance(self.period, Period) else None
        }
        return {k: v for k, v in contactpoint.items() if v not in ("", None)}


class ContactDetail:

    def __init__(self, name: Optional[str] = None, telecom: Optional[List[ContactPoint]] = None):
        self.name = name
        self.telecom = telecom

    def get(self):
        contactdetail = {
            "name": self.name if isinstance(self.name, str) else None,
            "telecom": [t.get() for t in self.telecom if isinstance(t, ContactPoint)] if isinstance(self.telecom,
                                                                                                    list) else None
        }
        return {k: v for k, v in contactdetail.items() if v not in ("", None, [])}


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
            "use": self.use if self.use in ["home", "work", "temp", "old", "billing"] else None,
            "text": self.text if isinstance(self.text, str) else None,
            "line": [l for l in self.line if isinstance(l, str)] if isinstance(self.line, list) else None,
            "city": self.city if isinstance(self.city, str) else None,
            "district": self.district if isinstance(self.district, str) else None,
            "state": self.state if isinstance(self.state, str) else None,
            "postalCode": self.postal_code if isinstance(self.postal_code, str) else None,
            "country": self.country if isinstance(self.country, str) else None,
            "period": self.period.get() if isinstance(self.period, Period) else None
        }

        return {k: v for k, v in address.items() if v not in ("", None, [])}


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
            "data": self.data if isinstance(self.data, str) else None,
            "url": self.url if isinstance(self.url, str) else None,
            "size": self.size if isinstance(self.size, int) else None,
            "hash": self.hash if isinstance(self.hash, str) else None,
            "title": self.title if isinstance(self.title, str) else None,
            "creation": self.creation if isinstance(self.creation, str) else None
        }
        return {k: v for k, v in attachment.items() if v not in ("", None)}


class Quantity:

    def __init__(self, value: Optional[float] = None, comparator: Optional[Literal["<", "<=", ">=", ">"]] = None,
                 unit: Optional[str] = None, system: Optional[str] = None, code: Optional[Code] = None):
        self.value = value
        self.comparator = comparator
        self.unit = unit
        self.system = system
        self.code = code

    def get(self):
        quantity = {
            "value": self.value if isinstance(self.value, float) else None,
            "comparator": self.comparator if self.comparator in ["<", "<=", ">=", ">"] else None,
            "unit": self.unit if isinstance(self.unit, str) else None,
            "system": self.system if isinstance(self.system, str) else None,
            "code": self.code.get() if isinstance(self.code, Code) else None
        }
        return {k: v for k, v in quantity.items() if v not in ("", None)}


class Range:

    def __init__(self, low: Optional[float] = None, high: Optional[float] = None):
        self.low = low
        self.high = high

    def get(self):
        _range = {
            "low": self.low if isinstance(self.low, float) else None,
            "high": self.high if isinstance(self.high, float) else None
        }
        return {k: v for k, v in _range.items() if v not in ("", None)}


class RelatedArtifact:

    def __init__(self, related_artifact_type: Literal[
        "documentation", "justification", "citation", "predecessor", "successor", "derived-from", "depends-on", "composed-of"],
                 label: Optional[str] = None, display: Optional[str] = None, citation: Optional[str] = None,
                 url: Optional[str] = None, document: Optional[Attachment] = None, resource: Optional[str] = None):
        self.related_artifact_type = related_artifact_type
        self.label = label
        self.display = display
        self.citation = citation
        self.url = url
        self.document = document
        self.resource = resource

    def get(self):
        relatedartifact = {
            "type": self.related_artifact_type if self.related_artifact_type in [
                "documentation", "justification", "citation", "predecessor", "successor", "derived-from", "depends-on",
                "composed-of"] else None,
            "label": self.label if isinstance(self.label, str) else None,
            "display": self.display if isinstance(self.display, str) else None,
            "citation": self.citation if isinstance(self.citation, str) else None,
            "url": self.url if isinstance(self.url, str) else None,
            "document": self.document.get() if isinstance(self.document, Attachment) else None,
            "resource": self.resource if isinstance(self.resource, str) else None
        }
        return {k: v for k, v in relatedartifact.items() if v not in ("", None)}


class Author:

    def __init__(self, author_reference: Optional[Reference] = None, author_string: Optional[str] = None):
        self.author_reference = author_reference
        self.author_string = author_string

    def get(self):
        author = {
            "authorReference": self.author_reference if isinstance(self.author_reference, Reference) else None,
            "authorString": self.author_string if isinstance(self.author_string, str) else None
        }
        return {k: v for k, v in author.items() if v not in ("", None)}


class Annotation:

    def __init__(self, text: str, author: Optional[Author] = None, time: str = None):
        self.author = author
        self.time = time
        self.text = text

    def get(self):
        annotation = {
            "authorReference": self.author.get().get("authorReference") if isinstance(self.author, Author) else None,
            "authorString": self.author.get().get("authorString") if isinstance(self.author, Author) else None,
            "time": self.time if isinstance(self.time, str) else None,
            "text": self.text if isinstance(self.text, str) else None
        }
        return {k: v for k, v in annotation.items() if v not in ("", None)}


class RepeatBounds:

    def __init__(self, bounds_duration: Optional[str] = None, bounds_range: Optional[Range] = None,
                 bounds_period: Optional[Period] = None):
        self.bounds_duration = bounds_duration
        self.bounds_range = bounds_range
        self.bounds_period = bounds_period

    def get(self):
        bounds = {
            "boundsDuration": self.bounds_duration if isinstance(self.bounds_duration, str) else None,
            "boundsRange": self.bounds_range.get() if isinstance(self.bounds_range, Range) else None,
            "boundsPeriod": self.bounds_period.get() if isinstance(self.bounds_period, Period) else None
        }
        return {k: v for k, v in bounds.items() if v not in ("", None)}


class Repeat:

    def __init__(self, bounds: Optional[RepeatBounds] = None, count: Optional[int] = None,
                 count_max: Optional[int] = None, duration: Optional[float] = None,
                 duration_max: Optional[float] = None,
                 duration_unit: Optional[Literal["s", "min", "h", "d", "wk", "mo", "a"]] = None,
                 frequency: Optional[int] = None, frequency_max: Optional[int] = None,
                 period: Optional[float] = None, period_max: Optional[float] = None,
                 period_unit: Optional[Literal["s", "min", "h", "d", "wk", "mo", "a"]] = None,
                 day_of_week: Optional[List[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]] = None,
                 time_of_day: Optional[List[str]] = None, when: Optional[List[Code]] = None,
                 offset: Optional[int] = None):
        self.bounds = bounds
        self.count = count
        self.count_max = count_max
        self.duration = duration
        self.duration_max = duration_max
        self.duration_unit = duration_unit
        self.frequency = frequency
        self.frequency_max = frequency_max
        self.period = period
        self.period_max = period_max
        self.period_unit = period_unit
        self.day_of_week = day_of_week
        self.time_of_day = time_of_day
        self.when = when
        self.offset = offset

    def get(self):
        repeat = {
            "boundsDuration": self.bounds.get().get("boundsDuration") if isinstance(self.bounds,
                                                                                    RepeatBounds) else None,
            "boundsRange": self.bounds.get().get("boundsRange") if isinstance(self.bounds, RepeatBounds) else None,
            "boundsPeriod": self.bounds.get().get("boundsPeriod") if isinstance(self.bounds, RepeatBounds) else None,
            "count": self.count if isinstance(self.count, int) and self.count > 0 else None,
            "countMax": self.count_max if isinstance(self.count_max, int) and self.count_max > 0 else None,
            "duration": self.duration if isinstance(self.duration, float) else None,
            "durationMax": self.duration_max if isinstance(self.duration_max, float) else None,
            "durationUnit": self.duration_unit if self.duration_unit in ["s", "min", "h", "d", "wk", "mo",
                                                                         "a"] else None,
            "frequency": self.frequency if isinstance(self.frequency, int) and self.frequency > 0 else None,
            "frequencyMax": self.frequency_max if isinstance(self.frequency_max,
                                                             int) and self.frequency_max > 0 else None,
            "period": self.period if isinstance(self.period, float) else None,
            "periodMax": self.period_max if isinstance(self.period_max, float) else None,
            "periodUnit": self.period_unit if self.period_unit in ["s", "min", "h", "d", "wk", "mo",
                                                                   "a"] else None,
            "dayOfWeek": [d for d in self.day_of_week if
                          d in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]] if isinstance(self.day_of_week,
                                                                                                list) else None,
            "timeOfDay": [t for t in self.time_of_day if isinstance(t, str)] if isinstance(self.time_of_day,
                                                                                           list) else None,
            "when": [w.get() for w in self.when if isinstance(w, Code)] if isinstance(self.when, list) else None,
            "offset": self.offset if isinstance(self.offset, int) and self.offset > 0 else None
        }
        return {k: v for k, v in repeat.items() if v not in ("", None, [])}


class Timing:

    def __init__(self, event: Optional[List[str]] = None, repeat: Optional[Repeat] = None,
                 code: Optional[CodeableConcept] = None):
        self.event = event
        self.repeat = repeat
        self.code = code

    def get(self):
        timing = {
            "event": [e for e in self.event if isinstance(e, str)] if isinstance(self.event, list) else None,
            "repeat": self.repeat.get() if isinstance(self.repeat, Repeat) else None,
            "code": self.code.get() if isinstance(self.code, CodeableConcept) else None
        }
        return {k: v for k, v in timing.items() if v not in ("", None, [])}


class Ratio:

    def __init__(self, numerator: Optional[Quantity] = None, denominator: Optional[Quantity] = None):
        self.numerator = numerator
        self.denominator = denominator

    def get(self):
        ratio = {
            "numerator": self.numerator.get() if isinstance(self.numerator, Quantity) else None,
            "denominator": self.denominator.get() if isinstance(self.denominator, Quantity) else None
        }
        return {k: v for k, v in ratio.items() if v not in ("", None)}


class SampledData:

    def __init__(self, origin: str, period: float, dimensions: int, factor: Optional[float] = None,
                 lower_limit: Optional[float] = None, upper_limit: Optional[float] = None, data: Optional[str] = None):
        self.origin = origin
        self.period = period
        self.dimensions = dimensions
        self.factor = factor
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.data = data

    def get(self):
        sampled_data = {
            "origin": self.origin if isinstance(self.origin, str) else None,
            "period": self.period if isinstance(self.period, float) else None,
            "factor": self.factor if isinstance(self.factor, float) else None,
            "lowerLimit": self.lower_limit if isinstance(self.lower_limit, float) else None,
            "upperLimit": self.upper_limit if isinstance(self.upper_limit, float) else None,
            "dimensions": self.dimensions if isinstance(self.dimensions, int) and self.dimensions > 0 else None,
            "data": self.data if isinstance(self.data, str) else None
        }
        return {k: v for k, v in sampled_data.items() if v not in ("", None)}


class UsageContextValue:

    def __init__(self, value_codeable_concept: Optional[CodeableConcept] = None,
                 value_quantity: Optional[Quantity] = None, value_range: Optional[Range] = None,
                 value_reference: Optional[Reference] = None):
        self.value_codeable_concept = value_codeable_concept
        self.value_quantity = value_quantity
        self.value_range = value_range
        self.value_reference = value_reference

    def get(self):
        value = {
            "valueCodeableConcept": self.value_codeable_concept if isinstance(self.value_codeable_concept,
                                                                              CodeableConcept) else None,
            "valueQuantity": self.value_quantity if isinstance(self.value_quantity, Quantity) else None,
            "valueRange": self.value_range if isinstance(self.value_range, Range) else None,
            "valueReference": self.value_reference if isinstance(self.value_reference, Reference) else None
        }
        return {k: v for k, v in value.items() if v not in ("", None)}


class UsageContext:

    def __init__(self, code: Coding, value: UsageContextValue):
        self.code = code
        self.value = value

    def get(self):
        context = {
            "code": self.code if isinstance(self.code, Coding) else None,
            "valueCodeableConcept": self.value.get().get("valueCodeableConcept") if isinstance(self.value,
                                                                                               UsageContextValue) else None,
            "valueQuantity": self.value.get().get("valueQuantity") if isinstance(self.value,
                                                                                 UsageContextValue) else None,
            "valueRange": self.value.get().get("valueRange") if isinstance(self.value,
                                                                           UsageContextValue) else None,
            "valueReference": self.value.get().get("valueReference") if isinstance(self.value,
                                                                                   UsageContextValue) else None,
        }
        return {k: v for k, v in context.items() if v not in ("", None)}


class TriggerDefinitionTiming:

    def __init__(self, timing_timing: Optional[Timing], timing_reference: Optional[Reference] = None,
                 timing_date: Optional[str] = None, timing_date_time: Optional[str] = None):
        self.timing_timing = timing_timing
        self.timing_reference = timing_reference
        self.timing_date = timing_date
        self.timing_date_time = timing_date_time

    def get(self):
        timing = {
            "timingTiming": self.timing_timing.get() if isinstance(self.timing_timing, Timing) else None,
            "timingReference": self.timing_reference.get() if isinstance(self.timing_reference, Reference) else None,
            "timingDate": self.timing_date if isinstance(self.timing_date, str) else None,
            "timingDateTime": self.timing_date_time if isinstance(self.timing_date_time, str) else None
        }
        return {k: v for k, v in timing.items() if v not in ("", None)}


class TriggerDefinition:

    def __init__(self, trigger_definition_type: Literal[
        "named-event", "periodic", "data-changed", "data-added", "data-modified", "data-removed", "data-accessed", "data-access-ended"],
                 name: Optional[str] = None, timing:Optional[TriggerDefinitionTiming] = None, ):
        pass