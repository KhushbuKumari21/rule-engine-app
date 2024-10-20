CREATE TABLE rules (
    id SERIAL PRIMARY KEY,  -- Using SERIAL for auto-incrementing in PostgreSQL
    rule_string TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
