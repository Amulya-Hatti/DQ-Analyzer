# import sqlite3

# DB_FILE = "database.sqlite"

# def count_tables(db_file):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     # cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     table_count = cursor.fetchone()[0]

#     conn.close()
#     return table_count

# if __name__ == "__main__":
#     num_tables = count_tables(DB_FILE)
#     print(f"Number of tables in the database: {num_tables}")


import sqlite3

DB_FILE = "database.sqlite"

def list_tables(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    conn.close()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

if __name__ == "__main__":
    list_tables(DB_FILE)

