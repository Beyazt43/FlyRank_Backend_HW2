CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done) VALUES
    ('Buy milk', false),
    ('Walk the dog', false),
    ('Read a book', true)
ON CONFLICT DO NOTHING;
