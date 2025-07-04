-- noinspection SqlCurrentSchemaInspectionForFile

-- Очистка всех таблиц с каскадным удалением зависимых данных
TRUNCATE TABLE
    agent_activities,
    agent_builds,
    agents,
    behavior_templates,
    roles
    RESTART IDENTITY CASCADE;

-- === Таблица roles ===
INSERT INTO public.roles (name, description, category, is_active)
VALUES ('Agent', 'Standard agent role', 'agent', TRUE),
       ('Admin', 'Administrator role', 'admin', TRUE);

-- === Таблица behavior_templates ===
INSERT INTO public.behavior_templates (name, role_id, template_data, os_type, version, is_active)
VALUES ('Default Template',
        1,
        '{"tasks": ["open_browser", "simulate_activity"], "interval": 10}',
        'Windows',
        'v1.0',
        TRUE),
       ('Simple Windows Tasks',
        1,
        '{"tasks": ["start_explorer", "start_calc", "simulate_activity"], "interval": 5}',
        'Windows',
        'v1.0',
        TRUE),
       -- === Новый шаблон с полным набором действий === (
       ('Full Test Template',
        2, -- Admin role_id
        '{
          "tasks": [
            {"action": "open_app", "app": "word", "delay": 2, "weight": 2},
            {"action": "open_app", "app": "docker", "delay": 1, "weight": 2},
            {"action": "open_browser", "urls": ["https://admin.microsoft.com", "https://docs.microsoft.com"], "delay": 2, "weight": 3},
            {"action": "run_terminal_command", "terminal": "powershell", "command": "Get-Service", "delay": 2, "weight": 2},
            {"action": "edit_file", "path": "C:\\\\Users\\\\%USERNAME%\\\\Documents\\\\admin_notes.txt", "delay": 2, "weight": 1},
            {"action": "simulate_activity", "weight": 1},
            {"action": "os_settings", "weight": 1},
            {"action": "ad_utilities", "weight": 1},
            {"action": "sleep", "seconds": 10, "weight": 1},
            {"action": "terminate", "delay": 5, "weight": 1}
          ],
          "interval": 10
        }',
        'Windows',
        'v1.0',
        TRUE);


-- === Таблица agents ===
INSERT INTO public.agents (agent_id, name, role_id, template_id, status, os_type, config,
                           injection_target, stealth_level, last_seen, last_activity)
VALUES ('agent_001',
        'Agent Smith',
        1,
        1,
        'active',
        'Windows',
        '{"interval": 1, "randomize": true}',
        'explorer.exe',
        'medium',
        NOW(),
        'launched browser'),
       ('agent_002',
        'Agent Neo',
        1,
        2,
        'active',
        'Windows',
        '{"interval": 5, "randomize": false}',
        'calc.exe',
        'low',
        NOW(),
        'started calc'),
       ('agent_admin_dc1ba1be30dd',
        'Admin Workstation',
        2, -- role_id для Admin (согласно твоему INSERT в roles)
        3, -- используем первый шаблон behavior_templates
        'active',
        'Windows',
        '{"interval": 10, "randomize": false}',
        'explorer.exe',
        'medium',
        NOW(),
        'initialized');

-- === Таблица agent_activities ===
INSERT INTO public.agent_activities (agent_id, activity_type, activity_data)
VALUES (1,
        'open_browser',
        '{"browser": "chrome", "url": "https://example.com"}'),
       (2,
        'start_calc',
        '{"exe": "calc.exe"}');

-- === Таблица agent_builds ===
INSERT INTO public.agent_builds (agent_id, build_config, binary_path, binary_size, build_status,
                                 build_log, build_time, completed_at)
VALUES (1,
        '{"target": "x64", "obfuscation": "basic"}',
        '/binaries/agent_001.exe',
        123456,
        'completed',
        'Build succeeded with no errors.',
        15,
        NOW()),
       (2,
        '{"target": "x64", "obfuscation": "none"}',
        '/binaries/agent_002.exe',
        654321,
        'completed',
        'Build finished.',
        8,
        NOW());
