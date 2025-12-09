import sqlite3
import os

DB_PATH = "web/gradebook.db"
SCHEMA_PATH = "web/schema.sql"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, "r") as f:
    sql = f.read()
conn.executescript(sql)
conn.close()
