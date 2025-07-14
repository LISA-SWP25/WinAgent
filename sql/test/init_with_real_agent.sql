-- Очистка всех таблиц с обнулением последовательностей
TRUNCATE TABLE
    agent_activities,
    agent_builds,
    agents,
    applications_template,
    behavior_templates,
    roles
    RESTART IDENTITY CASCADE;

-- === roles ===
INSERT INTO public.roles (name, description, category, is_active)
VALUES ('Agent', 'Standard agent role', 'agent', TRUE),
       ('Admin', 'Administrator role', 'admin', TRUE);

-- === behavior_templates ===
INSERT INTO public.behavior_templates (name, description, template_data, os_type, is_active)
VALUES ('Full Test Template',
        'Full test scenario with various actions',
        '{
  "tasks": [
    {
      "action": "update_file",
      "path": "C:\\\\Users\\\\%USERNAME%\\\\Documents\\\\word_doc.docx",
      "content": "Updated Word document content.",
      "delay": 1,
      "repeatable": false,
      "weight": 1
    },
    {
      "action": "update_file",
      "path": "C:\\\\Users\\\\%USERNAME%\\\\Documents\\\\notes.txt",
      "content": "Updated Notepad file content.",
      "delay": 1,
      "repeatable": false,
      "weight": 1
    },
    {
      "action": "update_file",
      "path": "C:\\\\Users\\\\%USERNAME%\\\\Documents\\\\vscode_note.txt",
      "content": "Updated VSCode file content.",
      "delay": 1,
      "repeatable": false,
      "weight": 1
    },
    {
      "action": "terminate",
      "delay": 0,
      "repeatable": false,
      "weight": 1
    }
  ],
  "interval": 0
}',
        'Windows',
        TRUE);


-- === applications_template ===
INSERT INTO public.applications_template (name, display_name, category, description, version, author, template_config,
                                          os_type, is_active)
VALUES ('WordApp',
        'Microsoft Word',
        'Office',
        'Launch Word and edit documents.',
        '1.0',
        'Admin',
        '{"path": "C:\\\\Program Files\\\\Microsoft Office\\\\word.exe"}',
        'Windows',
        TRUE);

-- === agents ===
INSERT INTO public.agents (agent_id, name, status, os_type, config, injection_target, stealth_level, role_id,
                           template_id)
VALUES ('agent_admin_dc1ba1be30dd',
        'Test User Agent',
        'active',
        'Windows',
        '{"interval": 0, "randomize": false}',
        'explorer.exe',
        2, -- stealth_level как Integer
        2, -- role_id (Admin)
        1 -- template_id (Full Test Template, первая и единственная запись)
       );

-- === agent_activities ===
INSERT INTO public.agent_activities (agent_id, activity_type, activity_data)
VALUES ((SELECT id FROM agents WHERE agent_id = 'agent_admin_dc1ba1be30dd'),
        'simulate_activity',
        '{"info": "Test activity for TESTUSERNAME"}');

-- === agent_builds ===
INSERT INTO public.agent_builds (agent_id, build_config, build_status, binary_path, binary_size, build_log)
VALUES ((SELECT id FROM agents WHERE agent_id = 'agent_admin_dc1ba1be30dd'),
        '{"target": "x64"}',
        'pending',
        '/binaries/agent_admin_dc1ba1be30dd.exe',
        0,
        'Build pending.');
