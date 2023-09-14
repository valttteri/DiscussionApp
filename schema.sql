CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    comment TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    discussion_id INTEGER REFERENCES discussions ON DELETE CASCADE,
    content TEXT
);