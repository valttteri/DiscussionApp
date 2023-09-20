CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    comment TEXT,
    creator_id INTEGER REFERENCES users,
    time TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    discussion_id INTEGER REFERENCES discussions ON DELETE CASCADE,
    content TEXT,
    creator_id INTEGER,
    time TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT
);