from pydantic import BaseModel
from typing import Optional


class Person(BaseModel):
    id: str
    name_ar: str
    name_en: str
    title: Optional[str] = None
    father_id: Optional[str] = None
    children_ids: list[str] = []
    generation: int
    type: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    is_highlighted: bool = False
    highlight_reason: Optional[str] = None


class LCARequest(BaseModel):
    ids: list[str]


class LCAResponse(BaseModel):
    lca_id: Optional[str]
    highlighted_ids: list[str]


class StatsResponse(BaseModel):
    total: int
    generations: int
    by_type: dict[str, int]
