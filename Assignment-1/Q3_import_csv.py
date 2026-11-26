import csv
import sqlite3

csv_path = "Employees.csv"
db_path = "employees.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        designation TEXT,
        manager TEXT,
        location TEXT,
        joining_date TEXT,
        experience_years REAL,
        work_mode TEXT
    )
""")

inserted = 0
skipped = 0

with open(csv_path, "r", encoding="utf-8", newline="") as file:
    # if your file is actually tab-separated like the sample, add delimiter="\t" here
    reader = csv.DictReader(file)

    for row in reader:
        emp_id = row["EmployeeID"].strip()
        name = row["EmployeeName"].strip()

        if emp_id == "" or name == "":
            skipped += 1
            continue

        dept = row["Department"].strip()
        role = row["Designation"].strip()
        mgr = row["Manager"].strip()
        city = row["Location"].strip()
        join_dt = row["JoiningDate"].strip()
        mode = row["WorkMode"].strip()

        exp_str = row["Experience_Years"].strip()
        if exp_str != "":
            exp = float(exp_str)
        else:
            exp = None

        cur.execute(
            "INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (emp_id, name, dept, role, mgr, city, join_dt, exp, mode)
        )

        if cur.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

conn.commit()
conn.close()

print("Inserted:", inserted)
print("Skipped:", skipped)