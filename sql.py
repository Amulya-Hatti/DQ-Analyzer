# import sqlite3
# import csv
# import os
# from pathlib import Path
# import uuid
# from datetime import datetime

# DATABASE = "data_quality.db"
# UPLOAD_DIR = "uploads"

# def process_csv(file_path):
#     """Dynamically create table and import CSV data"""
#     table_name = Path(file_path).stem  # Use filename as table name
#     with open(file_path, 'r') as f:
#         reader = csv.reader(f)
#         headers = next(reader)
        
#         # Create table with dynamic schema
#         conn = sqlite3.connect(DATABASE)
#         cursor = conn.cursor()
        
#         # Generate column definitions
#         cols = ['"{}" TEXT'.format(header.replace(' ', '_')) for header in headers]
#         create_table = f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             {', '.join(cols)}
#         )
#         """
#         cursor.execute(create_table)
        
#         # Insert data
#         placeholders = ', '.join(['?'] * len(headers))
#         insert_sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
        
#         for row in reader:
#             cursor.execute(insert_sql, row)
        
#         conn.commit()
#         conn.close()

# def upload_files(csv_directory):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
    
#     for csv_file in Path(csv_directory).glob('*.csv'):
#         # Store file metadata
#         file_id = str(uuid.uuid4())
#         file_size = os.path.getsize(csv_file)
#         file_path = Path(UPLOAD_DIR) / csv_file.name
        
#         cursor.execute('''
#             INSERT INTO uploaded_files 
#             (id, filename, filepath, upload_date, size, processed)
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', (
#             file_id,
#             csv_file.name,
#             str(file_path),
#             datetime.now().isoformat(),
#             file_size,
#             0
#         ))
        
#         # Process CSV data
#         process_csv(csv_file)
        
#         # Mark as processed
#         cursor.execute('''
#             UPDATE uploaded_files 
#             SET processed = 1 
#             WHERE id = ?
#         ''', (file_id,))
        
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     # Create upload directory
#     Path(UPLOAD_DIR).mkdir(exist_ok=True)
    
#     # Upload all CSVs from a directory
#     upload_files('/home/sigmoid/datasets/sample-data.csv')


import os
import sqlite3
import pandas as pd

# Directory containing CSV files
CSV_FOLDER = "/home/sigmoid/datasets"
# SQLite database file
DB_FILE = "database.sqlite"

def csv_to_sqlite(csv_folder, db_file):
    # Connect to SQLite database (creates it if not exists)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Iterate through all CSV files in the directory
    for file in os.listdir(csv_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder, file)
            table_name = os.path.splitext(file)[0]  # Get file name without extension
            
            # Read CSV file into Pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Store DataFrame in SQLite (replacing table if it exists)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            
            print(f"Stored {file} in table {table_name}")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    csv_to_sqlite(CSV_FOLDER, DB_FILE)
    print("All CSV files have been stored in the SQLite database.")

