-- CREATE USER applications WITH PASSWORD 'interlinked';
-- CREATE DATABASE portfolio OWNER applications;
CREATE TABLE Movies(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    normalized_title TEXT UNIQUE,
    title TEXT,
    year TEXT,
    rated TEXT,
    released TEXT,
    runtime TEXT,
    genre TEXT,
    director TEXT,
    writer TEXT,
    actors TEXT,
    plot TEXT,
    language TEXT
);