# import sqlite3
# from sqlite3 import Error
# import pandas as pd
# from src.config.settings import settings

# class DatabaseService:
#     def __init__(self):
#         self.db_path = settings.sqlite_db_path

#     def get_connection(self):
#         """Create and return a database connection"""
#         try:
#             conn = sqlite3.connect(self.db_path)
#             return conn
#         except Error as e:
#             raise Exception(f"Database connection error: {str(e)}")

#     def get_tables(self):
#         """Get list of tables in the database"""
#         conn = self.get_connection()
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             tables = cursor.fetchall()
#             return [table[0] for table in tables]
#         except Error as e:
#             raise Exception(f"Error fetching tables: {str(e)}")
#         finally:
#             conn.close()

#     def get_table_data(self, table_name):
#         """Get data from a specific table as pandas DataFrame"""
#         conn = self.get_connection()
#         try:
#             query = f"SELECT * FROM {table_name}"
#             df = pd.read_sql_query(query, conn)
#             return df
#         except Error as e:
#             raise Exception(f"Error fetching table data: {str(e)}")
#         finally:
#             conn.close()











import sqlite3
from sqlite3 import Error
import pandas as pd
from src.config.settings import settings
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.db_path = settings.sqlite_db_path
        self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            # Create data_validation_rules table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_validation_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    column_name TEXT NOT NULL,
                    rule_text TEXT NOT NULL,
                    rule_reason TEXT NOT NULL,
                    sql_query TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create data_validation_results table for storing validation results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_validation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_id INTEGER NOT NULL,
                    validation_date TIMESTAMP NOT NULL,
                    pass_count INTEGER NOT NULL,
                    fail_count INTEGER NOT NULL,
                    failure_examples TEXT,
                    FOREIGN KEY (rule_id) REFERENCES data_validation_rules(id)
                )
            ''')
            
            conn.commit()
        except Error as e:
            raise Exception(f"Database initialization error: {str(e)}")
        finally:
            conn.close()

    def get_connection(self):
        """Create and return a database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Error as e:
            raise Exception(f"Database connection error: {str(e)}")

    def get_tables(self):
        """Get list of tables in the database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Error as e:
            raise Exception(f"Error fetching tables: {str(e)}")
        finally:
            conn.close()

    def get_table_data(self, table_name):
        """Get data from a specific table as pandas DataFrame"""
        conn = self.get_connection()
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            return df
        except Error as e:
            raise Exception(f"Error fetching table data: {str(e)}")
        finally:
            conn.close()
    
    def store_validation_rules(self, table_name, rules_data):
        """Store generated validation rules in the database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Extract rules from the JSON structure
            for column_rule in rules_data.get("rules", []):
                column_name = column_rule.get("column")
                rules = column_rule.get("rules", [])
                
                for rule in rules:
                    rule_text = rule.get("rule")
                    rule_reason = rule.get("reason")
                    
                    # Insert rule into database
                    cursor.execute('''
                        INSERT INTO data_validation_rules 
                        (table_name, column_name, rule_text, rule_reason)
                        VALUES (?, ?, ?, ?)
                    ''', (table_name, column_name, rule_text, rule_reason))
            
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise Exception(f"Error storing validation rules: {str(e)}")
        finally:
            conn.close()
    
    def get_validation_rules(self, table_name=None, column_name=None):
        """Retrieve validation rules with optional filtering"""
        conn = self.get_connection()
        try:
            query = "SELECT * FROM data_validation_rules WHERE 1=1"
            params = []
            
            if table_name:
                query += " AND table_name = ?"
                params.append(table_name)
            
            if column_name:
                query += " AND column_name = ?"
                params.append(column_name)
                
            df = pd.read_sql_query(query, conn, params=params)
            return df.to_dict('records')
        except Error as e:
            raise Exception(f"Error retrieving validation rules: {str(e)}")
        finally:
            conn.close()
    
    def update_rule_sql_query(self, rule_id, sql_query):
        """Update a rule with the generated SQL query"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE data_validation_rules
                SET sql_query = ?, updated_at = ?
                WHERE id = ?
            ''', (sql_query, datetime.now(), rule_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            raise Exception(f"Error updating rule SQL query: {str(e)}")
        finally:
            conn.close()
    
    def run_validation_query(self, rule_id, sql_query):
        """Run a validation SQL query and store results"""
        conn = self.get_connection()
        try:
            # Get the failing records (limit to 5 examples)
            failure_examples_df = pd.read_sql_query(f"{sql_query} LIMIT 5", conn)
            failure_examples = failure_examples_df.to_json(orient='records') if not failure_examples_df.empty else None
            
            # Count the fails
            fail_count_df = pd.read_sql_query(f"SELECT COUNT(*) as count FROM ({sql_query})", conn)
            fail_count = fail_count_df['count'].iloc[0] if not fail_count_df.empty else 0
            
            # Get the rule details to determine table and column
            rule_df = pd.read_sql_query("SELECT table_name, column_name FROM data_validation_rules WHERE id = ?", 
                                         conn, params=[rule_id])
            
            if not rule_df.empty:
                table_name = rule_df['table_name'].iloc[0]
                # Count total rows in the table to calculate pass count
                total_count_df = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table_name}", conn)
                total_count = total_count_df['count'].iloc[0] if not total_count_df.empty else 0
                pass_count = total_count - fail_count
                
                # Store the validation results
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO data_validation_results
                    (rule_id, validation_date, pass_count, fail_count, failure_examples)
                    VALUES (?, ?, ?, ?, ?)
                ''', (rule_id, datetime.now(), pass_count, fail_count, failure_examples))
                
                conn.commit()
                
                return {
                    "rule_id": rule_id,
                    "pass_count": pass_count, 
                    "fail_count": fail_count,
                    "failure_examples": failure_examples_df.to_dict('records') if not failure_examples_df.empty else []
                }
            
            return None
        except Error as e:
            conn.rollback()
            raise Exception(f"Error running validation query: {str(e)}")
        finally:
            conn.close()