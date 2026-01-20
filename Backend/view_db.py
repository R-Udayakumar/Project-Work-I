import sqlite3

# Connect to the database
conn = sqlite3.connect('venv/var/nexus.db')  # Or 'instance/nexus.db' if it's inside that folder
cursor = conn.cursor()

# Get all students
print("\n--- STUDENTS IN DATABASE ---")
try:
    cursor.execute("SELECT id, name, target_role, skills FROM student")
    rows = cursor.fetchall()

    if not rows:
        print("No students found.")
    
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Role: {row[2]} | Skills: {row[3]}")

except Exception as e:
    print(f"Error: {e}")

conn.close()