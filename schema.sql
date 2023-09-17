CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    comment TEXT,
    creator_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    discussion_id INTEGER REFERENCES discussions ON DELETE CASCADE,
    content TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);