# Joblog

Joblog stores job vacancies from LinkedIn without manual data entry. Save listings for review and track your job search.

![preview](https://github.com/user-attachments/assets/22c859c9-fcb2-4583-8ae3-c586431e89b2)

> [!IMPORTANT]  
> Joblog is not an automated scraper. It's a tool for job seekers to save jobs they're actively viewing and interested in.

## Features

- **Job Capture**: Chrome extension saves LinkedIn job listings with keyboard shortcuts
- **Data Extraction**: Scrapes job details:
  - Job title and company
  - Location and workplace type
  - Job description
  - Company logo and URLs
  - Experience level
- **Storage**: PostgreSQL database for job data
- **Architecture**:
  - Python/BeautifulSoup scraping service
  - Rust/Diesel ORM
  - GraphQL API
  - Chrome extension

## Components

### 1. Chrome Extension (`/apps/extension`)
- Captures page content
- Sends to API
- Shows status messages

### 2. Python API (`/packages/api`)
- Flask service for extension requests
- BeautifulSoup scraping
- Data extraction
- GraphQL client

### 3. Database Service (`/packages/database`)
- GraphQL API in Rust
- PostgreSQL with Diesel ORM
- Data persistence
- Query interface

## Getting Started

[TODO: Add installation and setup instructions]

## Development Status

Currently in active development. Core job saving functionality is working, with more features planned:

- [ ] Job application tracking frontend
  - Track application status
  - Upload CV/cover letter versions
  - Store interview notes and feedback
  - Log recruiter conversations
- [ ] Search and filtering capabilities
- [ ] Data export options
- [ ] Analytics dashboard
- [ ] PostgreSQL deployment with Terraform
