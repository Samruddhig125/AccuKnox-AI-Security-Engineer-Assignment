
import csv
import sqlite3

# File paths for the employee CSV and the SQLite database
csv_path = "Employees.csv"
db_path = "employees.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create the employees table
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
    # Using DictReader so we can access values directly by column name
    reader = csv.DictReader(file)

    for row in reader:
        emp_id = row["EmployeeID"].strip()
        name = row["EmployeeName"].strip()

        # Employee ID and name are required, so skip the row if either is missing
        if emp_id == "" or name == "":
            skipped += 1
            continue

        # Pick the remaining employee details from the current CSV row
        dept = row["Department"].strip()
        role = row["Designation"].strip()
        mgr = row["Manager"].strip()
        city = row["Location"].strip()
        join_dt = row["JoiningDate"].strip()
        mode = row["WorkMode"].strip()

        # Convert experience into a number; keep it NULL if no value is provided
        exp_str = row["Experience_Years"].strip()
        if exp_str != "":
            exp = float(exp_str)
        else:
            exp = None

        # Insert the employee record.
        # If the employee ID already exists, SQLite ignores the duplicate.
        cur.execute(
            "INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (emp_id, name, dept, role, mgr, city, join_dt, exp, mode)
        )

        # rowcount tells us whether this record was actually inserted
        if cur.rowcount == 1:
            inserted += 1
        else:
            skipped += 1


conn.commit()
conn.close()


print("Inserted:", inserted)
print("Skipped:", skipped)
