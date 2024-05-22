from typing import List
class Code:
    def __init__(self, value: str = ""):
        self.value = value

    def get(self):
        return self.value


class Coding:

    def __init__(self, system: str = "", version: str = "", code: Code = None, display: str = "",
                 userSelected: bool = ""):
        self.system = system
        self.version = version
        self.code = code
        self.display = display
        self.userSelected = userSelected

    def get(self):
        coding = {
            "system": self.system,
            "version": self.version,
            "code": self.code.get() if isinstance(self.code, Code) else None,
            "display": self.display,
            "userSelected": self.userSelected
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

class Reference:

    def __init__(self, reference, display:str = ""):
        pass