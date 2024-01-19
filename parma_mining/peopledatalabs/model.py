"""Pydantic models for the Parma Mining API."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Naic(BaseModel):
    """Pydantic model for the NAIC entity."""

    naics_code: str | None
    sector: str | None
    sub_sector: str | None
    industry_group: str | None
    naics_industry: str | None
    national_industry: str | None


class SicItem(BaseModel):
    """Pydantic model for the SIC entity."""

    sic_code: str | None
    major_group: str | None
    industry_group: str | None
    industry_sector: str | None


class Location(BaseModel):
    """Pydantic model for the location entity."""

    name: str | None
    locality: str | None
    region: str | None
    metro: str | None
    country: str | None
    continent: str | None
    street_address: str | None
    address_line_2: str | None
    postal_code: str | None
    geo: str | None


class OrganizationModel(BaseModel):
    """Base model for the organization entity.

    To be extended with the premimum fields
    """

    status: int
    name: str
    display_name: str | None
    size: str | None
    employee_count: int | None
    id: str
    founded: int | None
    industry: str | None
    naics: list[Naic] | None
    sic: list[SicItem] | None
    location: Location | None
    linkedin_id: str | None
    linkedin_url: str | None
    facebook_url: str | None
    twitter_url: str | None
    profiles: list[str] | None
    website: str | None
    ticker: str | None
    gics_sector: Any | None
    mic_exchange: Any | None
    type: str | None
    summary: str | None
    tags: list[str] | None
    headline: str | None
    alternative_names: list[str] | None
    alternative_domains: list[str] | None
    affiliated_profiles: list[str] | None
    likelihood: int | None


class CompaniesRequest(BaseModel):
    """Base model for the companies request."""

    task_id: int
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Base model for the response model."""

    source_name: str
    company_id: str
    raw_data: OrganizationModel


class DiscoveryRequest(BaseModel):
    """Request model for the discovery endpoint."""

    company_id: str
    name: str


class DiscoveryResponse(BaseModel):
    """Define the output model for the discovery endpoint."""

    handles: list[str] = []


class FinalDiscoveryResponse(BaseModel):
    """Define the final discovery response model."""

    identifiers: dict[str, DiscoveryResponse]
    validity: datetime


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
