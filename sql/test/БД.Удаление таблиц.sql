-- === Drop tables in correct order to respect foreign keys ===

DROP TABLE IF EXISTS agent_activities CASCADE;
DROP TABLE IF EXISTS agent_builds CASCADE;
DROP TABLE IF EXISTS agents CASCADE;
DROP TABLE IF EXISTS applications_template CASCADE;
DROP TABLE IF EXISTS behavior_templates CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- === Optional: Check if everything is clean ===
-- \dt
