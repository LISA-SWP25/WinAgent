import getpass
import os
import subprocess
import sys
import uuid

# === Проверка аргумента ===
if len(sys.argv) < 2:
    print("[❌] Please provide the path to your behavior template JSON file.")
    print("Usage: python generate_and_run_sql.py path/to/template.json")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.isfile(json_file_path):
    print(f"[❌] JSON file '{json_file_path}' not found.")
    sys.exit(1)

# === Get current username ===
username = getpass.getuser()


# === Get MAC address ===
def get_mac():
    mac = uuid.getnode()
    return format(mac, '012x')


mac_address = get_mac()

print(f"[*] Detected username: {username}")
print(f"[*] Detected MAC address: {mac_address}")
print(f"[*] Using template file: {json_file_path}")

# === Load the JSON ===
with open(json_file_path, "r", encoding="utf-8") as f:
    json_str = f.read().strip()

# === Read original SQL ===
INPUT_SQL = "БД.Заполнение таблиц.sql"
with open(INPUT_SQL, "r", encoding="utf-8") as f:
    sql_content = f.read()

# === Replace placeholders ===
old_id = "agent_TESTUSERNAME_TESTMACADDRESS"
new_id = f"agent_{username}_{mac_address}"

sql_content = sql_content.replace(old_id, new_id)
sql_content = sql_content.replace("TEST_BEHAVIOR_TEMPLATE_DATA", f"'{json_str}'")

# === Save updated SQL ===
output_sql = "init_with_real_agent.sql"
with open(output_sql, "w", encoding="utf-8") as f:
    f.write(sql_content)

print(f"[+] Updated SQL saved as '{output_sql}'")

# === PostgreSQL connection settings ===
PG_USER = "postgres"
PG_DB = "lisa_dev"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_PASSWORD = "pass"  # HARDCODE

# === Run psql ===
env = os.environ.copy()
env["PGPASSWORD"] = PG_PASSWORD

print(f"[*] Running script on database '{PG_DB}'...")
result = subprocess.run(
    ["psql", "-h", PG_HOST, "-p", PG_PORT, "-U", PG_USER, "-d", PG_DB, "-f", output_sql],
    env=env,
    shell=True
)

if result.returncode == 0:
    print("[✅] SQL executed successfully!")
else:
    print("[❌] SQL execution failed. Check details.")
