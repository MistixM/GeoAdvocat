import sqlite3
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log',  
    filemode='a'
) 

def create_connection(db_file):
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        
        logging.info(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        
    return conn


# Save cursor to the table
def save_cursor(conn, end_cursor):
    cursor = conn.cursor()
    cursor.execute(
        "REPLACE INTO end_cursors (id, cursor) VALUES (1, ?)",
        (end_cursor,)
    )
    conn.commit()


# Load cursor from the table
def load_cursor(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cursor FROM end_cursors WHERE id = 1")
    result = cursor.fetchone()
    return result[0] if result else None


# Add the post ID to the table
def add_post(conn, pk):
    cursor = conn.cursor()

    query = f"""
    INSERT INTO posts (pk)
    VALUES (?)
    """

    cursor.execute(query, (pk,))
    conn.commit()



# Check the post availability
def check_post(conn, pk):
    cursor = conn.cursor()

    query = f"""
    SELECT * FROM posts WHERE pk = ?
    """

    cursor.execute(query, (pk,))
    result = cursor.fetchone()

    return result is not None