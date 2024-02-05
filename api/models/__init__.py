from typing import List, Optional

from pydantic import BaseModel, Field


class WorkHistory(BaseModel):
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Position held")
    date_start: str = Field(..., description="Date start of experience")
    date_end: str = Field(..., description="Date end of experience")
    responsibilities: List[str] = Field(
        ..., description="Responsibilities during the job"
    )


class Education(BaseModel):
    institution: str = Field(..., description="Institution name")
    program_or_degree: str = Field(..., description="Program or degree name")
    dateStart: str = Field(..., description="Date start of education")
    dateEnd: str = Field(..., description="Date end of education")


class Candidate(BaseModel):
    name: str = Field(..., description="Name of the person")
    location: str = Field(..., description="Location")
    work_history: List[WorkHistory] = Field(..., description="List of work history")
    education: List[Education] = Field(..., description="List of educational details")
    skills: List[str] = Field(None, description="List of skills")
    links: List[str] = Field(None, description="List of links")


class JobPosting(BaseModel):
    summary: str = Field(
        ..., description="Summary of job posting requirements and responsibilities."
    )
    skills: str = Field(..., description="List of skills required for the job.")
    requirements: List[str] = Field(
        ..., description="List of requirements for the job."
    )
    responsibilities: List[str] = Field(
        ..., description="List of responsibilities for the job."
    )


class CreateVacancy(BaseModel):
    company: str = Field(..., title="Company name")
    position: str = Field(..., title="Job Position")
    location: str = Field(..., title="Location")
    contract: str = Field(..., title="Contract type")
    remote: str = Field("No", title="Is it a Remote job?")
    salaryMin: Optional[float] = Field(None, gt=0, title="Minimum Salary")
    salaryMax: Optional[float] = Field(None, gt=0, title="Maximum Salary")
    about: str = Field(..., title="About the job")
    requirements: str = Field(..., title="Job Requirements")
    responsibilities: str = Field(..., title="Responsibilities")


class Evaluation(BaseModel):
    """Data model for candidate evaluation dimensions."""

    is_match: bool = False
    is_relevant: bool = False
    original_text: str = None
    relevance_or_match_reason: Optional[str]
    improved_text: Optional[str]
