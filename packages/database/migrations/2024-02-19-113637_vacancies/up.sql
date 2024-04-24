-- Your SQL goes here
ALTER TABLE Vacancies
ADD CONSTRAINT fk_uid UNIQUE(uid);