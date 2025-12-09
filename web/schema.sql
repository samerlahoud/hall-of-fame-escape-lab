DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS secrets;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    course TEXT,
    grade TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    text TEXT
);

CREATE TABLE secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    value TEXT
);

INSERT INTO users (username, password, role) VALUES
('alice', 'alice123', 'student'),
('bob', 'bob123', 'student'),
('prof', 'prof123', 'instructor');

INSERT INTO grades (student, course, grade) VALUES
('alice', 'CSCI4178', 'B'),
('bob', 'CSCI4178', 'C'),
('alice', 'CSCI3130', 'A'),
('bob', 'CSCI3130', 'B');

INSERT INTO comments (author, text) VALUES
('alice', 'Great course!'),
('bob', 'I wish the term was longer.');

INSERT INTO secrets (name, value) VALUES
('hall_of_fame_secret', 'This portal is horribly insecure and reveals secrets via UNION attacks.');
