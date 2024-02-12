# Introduction

 Traditionally, candidate needs to read and analyse job description against their resume, remove irrelevant responsibilities from their experience, and paraphrase relevant responsibilities to match the job description, generate the tailored resume and write a tailored cover letter. Described process can sometimes take hours.

 This project aims to streamline this process by:

 - Scraping job description with the help of a Chrome extension.
 - Writing scraped jobs to a SQL database for tracking.
 - Analyses candidate's past experiences and responsibilities, offering match and relevance evaluation, improvement suggestions and example bullet points that matches job requirements and responsibilities via an interactive web interface.
 - Automatically generates tailored resume and cover letter for the job they are applying for.

 Moreover, there is a backlog of potential features to come:
 - Tracks resume version history for each application.
 - Track application status and automatically log feedback using an email plugin.
 - Provide analytics to measure candidate success.

# TODOs (Technical Backlog)

## Urgent

_Empty_

## Backlog

### Job scraping and logging

 *Implemented classic scraping methods in favor of LLM data extraction as the former is significantly faster and does not consume precious resources. Only downside is scraper needs constant maintenance and testing, which I haven't implemented.*

- [ ] **LinkedIn scraping bails when tag is missing or slice index is incorrect** - We need to account for optional fields, Which I forgot they exist.
- [ ] **Add recruiter information if present** - We could increase our chances of success by drafting a nice introduction message to the recruiter. Hence, good to have on the database.
- [x] **Predetermine whether scrapped data contains a valid job description** - Not every page scraped via the extension will contain a job vacancy. We shouldn't allow generating scrubbed JSON data if scrapped page description has nothing to do with job vacancy. I don't know a good way to do this.
- [x] **Context window is too small for scraped data** - Some scraped site data (LinkedIn, for example) contains too much text. We may need to look into better ways to obtain relevant text from scraped data. *See above*
- [x] **Scraped data is sometimes not accurate** - Related to the item above, irrelevant details found in the scrapted text bloat the context and yield irrelevant output. *See above*

### Other

- [ ] **Resume line analysis consumes too many tokens**: Each query contains RAG context and instructions, therefore total query token count hovers around 1K. Yet to find a reliable strategy for fast and simple reasoning tasks.
- [x] **Stream LLM Output** - Unstructured string responses could be streamed. However, currently, project only deals with structured responses.
- [x] **Speed up llama.cpp grammar** - Done, enabled GPU acceleration for Metal.
