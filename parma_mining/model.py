from typing import Any, List, Optional

from pydantic import BaseModel


class Naic(BaseModel):
    naics_code: str
    sector: Optional[str]
    sub_sector: Optional[str]
    industry_group: Optional[str]
    naics_industry: Optional[str]
    national_industry: Optional[str]


class SicItem(BaseModel):
    sic_code: str
    major_group: Optional[str]
    industry_group: Optional[str]
    industry_sector: Optional[str]


class Location(BaseModel):
    name: Optional[str]
    locality: Optional[str]
    region: Optional[str]
    metro: Optional[str]
    country: Optional[str]
    continent: Optional[str]
    street_address: Optional[str]
    address_line_2: Optional[str]
    postal_code: Optional[str]
    geo: Optional[str]


class OrganizationModel(BaseModel):
    """Base model for the organization entity.

    To be extended with the premimum fields
    """

    status: int
    name: str
    display_name: Optional[str]
    size: Optional[str]
    employee_count: Optional[int]
    id: str
    founded: Optional[int]
    industry: Optional[str]
    naics: Optional[List[Naic]]
    sic: Optional[List[SicItem]]
    location: Optional[Location]
    linkedin_id: Optional[str]
    linkedin_url: Optional[str]
    facebook_url: Optional[str]
    twitter_url: Optional[str]
    profiles: Optional[List[str]]
    website: Optional[str]
    ticker: Optional[str]
    gics_sector: Optional[Any]
    mic_exchange: Optional[Any]
    type: Optional[str]
    summary: Optional[str]
    tags: Optional[List[str]]
    headline: Optional[str]
    alternative_names: Optional[List[str]]
    alternative_domains: Optional[List[str]]
    affiliated_profiles: Optional[List[str]]
    likelihood: int
