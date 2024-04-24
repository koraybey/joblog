-- Your SQL goes here
CREATE TABLE Vacancies (
    pk SERIAL PRIMARY KEY,
    uid VARCHAR NOT NULL,
    company_logo VARCHAR NOT NULL,
    company VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR NOT NULL,
    workplace_type VARCHAR,
    url VARCHAR NOT NULL,
    company_url VARCHAR NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    experience_level VARCHAR,
    contract_type VARCHAR
);