CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    comment TEXT,
    creator_id INTEGER REFERENCES users,
    time TIMESTAMP,
    title TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    discussion_id INTEGER REFERENCES discussions ON DELETE CASCADE,
    content TEXT,
    creator_id INTEGER,
    time TIMESTAMP,
    creator_name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT,
    lastactivity TIMESTAMP
);

CREATE TABLE private_discussions (
    id SERIAL PRIMARY KEY,
    title TEXT,
    creator_id, INTEGER REFERENCES users ON DELETE CASCADE,
    lastactivity TIMESTAMP
);

CREATE TABLE private_rights (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    discussion_id, INTEGER REFERENCES private_discussions ON DELETE CASCADE
);

CREATE TABLE private_comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    discussion_id INTEGER REFERENCES private_discussions ON DELETE CASCADE,
    creator_id INTEGER REFERENCES users ON DELETE CASCADE,
    time TIMESTAMP,
    creator_name TEXT
);

INSERT INTO users (username, password, admin) VALUES ("NormalUser", "1234", 'FALSE');
INSERT INTO users (username, password, admin) VALUES ("AdminUser", "1234", 'TRUE');

INSERT INTO topics (name, lastactivity) VALUES ('Aihepiiri', NOW());
INSERT INTO discussions (topic, comment, creator_id, time, title) VALUES ('Aihepiiri', 'Keskustelunavaus', 1, NOW(), 'Keskustelun otsikko');
INSERT INTO comments (discussion_id, content, creator_id, time, creator_name) VALUES (1, 'Kommentti keskustelussa', 1, NOW(), 'NormalUser');