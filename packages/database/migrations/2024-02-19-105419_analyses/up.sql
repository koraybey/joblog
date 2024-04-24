-- Your SQL goes here
CREATE TABLE Analyses (
    pk SERIAL PRIMARY KEY,
    uid VARCHAR NOT NULL,
    company VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    match VARCHAR NOT NULL,
    relevance VARCHAR NOT NULL,
    reason TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_uid
      FOREIGN KEY(uid) 
        REFERENCES Vacancies(uid)
);
