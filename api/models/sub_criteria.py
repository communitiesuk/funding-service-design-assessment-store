import inspect
from dataclasses import dataclass
from typing import List, Dict
from api.models.theme import Theme
from stringcase import lowercase
from dataclasses import dataclass
from dataclass_dict_convert import dataclass_dict_convert


@dataclass_dict_convert()
@dataclass()
class SubCriteria:
    id: str
    name: str
    themes: List[Theme]
    funding_amount_requested: int
    project_name: str
    fund_id: str
    workflow_status: str


    def __post_init__(self):
        self.themes = [
            Theme.from_filtered_dict(theme) for theme in self.themes
        ]
        self.workflow_status = self.workflow_status.name

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
