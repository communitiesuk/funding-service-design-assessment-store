import inspect
from dataclasses import dataclass

from dataclass_dict_convert import dataclass_dict_convert


@dataclass_dict_convert()
@dataclass()
class Answer:
    field_id: str
    form_name: str
    field_type: str
    presentation_type: str
    question: str

    @classmethod
    def from_filtered_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(cls).parameters
            }
        )
