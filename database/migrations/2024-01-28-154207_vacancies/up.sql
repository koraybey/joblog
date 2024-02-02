-- Your SQL goes here
CREATE TABLE Vacancies (
    pk SERIAL PRIMARY KEY,
    uid VARCHAR NOT NULL,
    company VARCHAR NOT NULL,
    position VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    contract VARCHAR NOT NULL,
    remote VARCHAR NOT NULL,
    salary_min INTEGER,
    salary_max INTEGER,
    about TEXT NOT NULL,
    requirements TEXT NOT NULL,  
    responsibilities TEXT NOT NULL
);