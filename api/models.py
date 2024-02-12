from pydantic import BaseModel, Field


class WorkHistory(BaseModel):
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Position held")
    date_start: str = Field(..., description="Date start of experience")
    date_end: str = Field(..., description="Date end of experience")
    responsibilities: list[str] = Field(..., description="Responsibilities during the job")


class Education(BaseModel):
    institution: str = Field(..., description="Institution name")
    program_or_degree: str = Field(..., description="Program or degree name")
    date_start: str = Field(..., description="Date start of education")
    date_end: str = Field(..., description="Date end of education")


class Candidate(BaseModel):
    name: str = Field(..., description="Name of the person")
    location: str = Field(..., description="Location")
    work_history: list[WorkHistory] = Field(..., description="List of work history")
    education: list[Education] = Field(..., description="List of educational details")
    skills: list[str] = Field(..., description="List of skills")
    links: list[str] = Field(..., description="List of links")


class JobPosting(BaseModel):
    summary: str = Field(..., description="Summary of job posting requirements and responsibilities.")
    skills: str = Field(..., description="List of skills required for the job.")
    requirements: list[str] = Field(..., description="List of requirements for the job.")
    responsibilities: list[str] = Field(..., description="List of responsibilities for the job.")


class CreateVacancy(BaseModel):
    company: str = Field(..., title="Company name")
    position: str = Field(..., title="Job Position")
    location: str = Field(..., title="Location")
    contract: str = Field(..., title="Contract type")
    remote: str = Field("No", title="Is it a Remote job?")
    salaryMin: float | None = Field(..., title="Minimum Salary")  # noqa: N815 - Must fit GraphQL mutation schema input.
    salaryMax: float | None = Field(..., title="Maximum Salary")  # noqa: N815 - Must fit GraphQL mutation schema input.
    about: str = Field(..., title="Summary of role, requirements and description")
    requirements: str = Field(..., title="Job Requirements")
    responsibilities: str = Field(..., title="Responsibilities")


class LineAnalysis(BaseModel):
    is_match: bool
    is_relevant: bool
    relevance_or_match_reason: str
