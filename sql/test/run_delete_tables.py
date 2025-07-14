import os
import subprocess

# === PostgreSQL connection settings ===
PG_USER = "postgres"
PG_DB = "lisa_dev"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_PASSWORD = "pass"

# === SQL file name ===
SQL_FILE = "БД.Удаление таблиц.sql"

# === Run ===
env = os.environ.copy()
env["PGPASSWORD"] = PG_PASSWORD

print(f"[*] Running {SQL_FILE} on database '{PG_DB}'...")

result = subprocess.run(
    ["psql", "-h", PG_HOST, "-p", PG_PORT, "-U", PG_USER, "-d", PG_DB, "-f", SQL_FILE],
    env=env,
    shell=True
)

if result.returncode == 0:
    print("[✅] Tables deleted successfully!")
else:
    print("[❌] SQL execution failed.")
