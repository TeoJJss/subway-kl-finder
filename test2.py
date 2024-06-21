import sqlite3

# Connect to the database (replace 'database.db' with your database file name)
conn = sqlite3.connect("outlets.db")

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT statement
cursor.execute("SELECT * FROM OUTLETS")

# Fetch and print all rows
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()