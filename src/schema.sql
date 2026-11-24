-- index.db schema — SQLite FTS5 hybrid archive
-- Mirrors the SCHEMA string in doclib.py (lines 134-180). Keep them identical.
-- PRAGMA user_version is set by setup.py / doclib.py to SCHEMA_VERSION.

CREATE TABLE IF NOT EXISTS files (
    file_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    collection  TEXT NOT NULL,
    name        TEXT NOT NULL,
    rel_path    TEXT NOT NULL,
    source_type TEXT NOT NULL,
    size        INTEGER,
    sha256      TEXT,
    n_chunks    INTEGER DEFAULT 0,
    added_at    TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(collection, rel_path)
);

CREATE TABLE IF NOT EXISTS chunks (
    file_id INTEGER NOT NULL,
    idx     INTEGER NOT NULL,
    page    INTEGER,
    text    TEXT NOT NULL,
    fts_key TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (file_id, idx),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    fts_key,
    content='chunks',
    content_rowid='rowid',
    tokenize="unicode61 remove_diacritics 2"
);

CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
    INSERT INTO chunks_fts(rowid, fts_key) VALUES (new.rowid, new.fts_key);
END;

CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, fts_key) VALUES ('delete', old.rowid, old.fts_key);
END;

CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, fts_key) VALUES ('delete', old.rowid, old.fts_key);
    INSERT INTO chunks_fts(rowid, fts_key) VALUES (new.rowid, new.fts_key);
END;

CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunks(file_id);
CREATE INDEX IF NOT EXISTS idx_files_coll ON files(collection);
