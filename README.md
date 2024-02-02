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

- **Querying for each responsibility without context memory consumes too many prompt tokens**: Each query contains RAG context and instructions, therefore total query token count hovers around 1K. Strategy change needed asap if we rely on 3rd party computation power.

## Backlog

- **Predetermine whether scrapped data contains a valid job description** - Not every page scraped via the extension will contain a job vacancy. We shouldn't allow generating scrubbed JSON data if scrapped page description has nothing to do with job vacancy. I don't know a good way to do this.
- **Context window is too small for scraped data** - Some scraped site data (LinkedIn, for example) contains too much text. We may need to look into better ways to obtain relevant text from scraped data.
- **Scraped data is sometimes not accurate** - Related to the item above, irrelevant details found in the scrapted text bloat the context and yield irrelevant output.
- [x] **Stream LLM Output** - Unstructured string responses could be streamed. However, currently, project only deals with structured responses.
- [x] **Speed up llama.cpp grammar** - Done, enabled GPU acceleration for Metal.