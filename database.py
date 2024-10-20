import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'rule_engine_db',
    'user': 'root',
    'password': 'khushbu123'  
}

def get_db_connection():
    """Establishes a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initializes the database and creates the necessary tables."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return
        
        cursor = conn.cursor()

        # Create the Rules table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Rules (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rule_string TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Create the RuleMetadata table
        cursor.execute('''CREATE TABLE IF NOT EXISTS RuleMetadata (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rule_id INT,
            attribute VARCHAR(255),
            condition VARCHAR(255),
            value VARCHAR(255),
            FOREIGN KEY (rule_id) REFERENCES Rules(id) ON DELETE CASCADE
        )''')

        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except Error as e:
        logging.error(f"Database initialization error: {e}")

def save_rule(rule_string):
    """Saves a new rule to the database."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return None
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Rules (rule_string) VALUES (%s)', 
                       (rule_string,))
        rule_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Rule saved successfully: %s", rule_string)
        return rule_id
    except Error as e:
        logging.error(f"Error saving rule: {e}")
        return None

def save_rule_metadata(rule_id, attribute, condition, value):
    """Saves rule metadata to the database."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return None
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO RuleMetadata (rule_id, attribute, condition, value) VALUES (%s, %s, %s, %s)', 
                       (rule_id, attribute, condition, value))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Rule metadata saved successfully for rule ID: %s", rule_id)
    except Error as e:
        logging.error(f"Error saving rule metadata: {e}")

def fetch_rule_by_id(rule_id):
    """Fetches a rule by its ID."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return None
        
        cursor = conn.cursor()
        cursor.execute('SELECT rule_string FROM Rules WHERE id = %s', (rule_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Error as e:
        logging.error(f"Error fetching rule by ID {rule_id}: {e}")
        return None

def update_rule(rule_id, rule_string):
    """Updates an existing rule in the database."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return
        
        cursor = conn.cursor()
        cursor.execute('UPDATE Rules SET rule_string = %s WHERE id = %s', 
                       (rule_string, rule_id))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Rule ID %d updated successfully.", rule_id)
    except Error as e:
        logging.error(f"Error updating rule ID {rule_id}: {e}")

def get_rules_by_ids(rule_ids):
    """Fetches rules by their IDs."""
    try:
        conn = get_db_connection()
        if conn is None:
            logging.error("Failed to connect to the database.")
            return []
        
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(rule_ids))
        cursor.execute(f'SELECT rule_string FROM Rules WHERE id IN ({format_strings})', tuple(rule_ids))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [result[0] for result in results] if results else []
    except Error as e:
        logging.error(f"Error fetching rules by IDs {rule_ids}: {e}")
        return []
