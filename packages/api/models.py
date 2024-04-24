from pydantic import BaseModel, Field


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

class LinkedInJobPost(BaseModel):
    company_logo: str
    company: str
    title: str
    description: str
    experience_level: str | None  # Internship, Entry, Associate, Mid-Senior, Director, Executive
    contract_type: str | None  # Full-time, Part-time, Contract, Internship
    location: str
    workplace_type: str | None  # On-site, Hybrid, Remote
    url: str
    company_url: str
