CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  event_name TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  run_id TEXT,
  participant_id TEXT,
  hook_id TEXT,
  arm TEXT,
  prior_exposure INTEGER,
  reading_seconds INTEGER,
  quiz_response_seconds INTEGER,
  score INTEGER,
  attribution_json TEXT,
  artifact_json TEXT
);
CREATE INDEX IF NOT EXISTS events_name_time ON events(event_name, occurred_at);
CREATE INDEX IF NOT EXISTS events_run ON events(run_id);
