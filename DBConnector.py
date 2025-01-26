import mysql.connector
from mysql.connector import errorcode

# Secure database connection configuration
config = {
    "user": "root",
    "password": "12345678",
    "host": "127.0.0.1",
    "database": "vbMobil",
    "port": 3306,
    "ssl_ca": "/path/to/ca-cert.pem",  # Path to your SSL certificate authority file
    "ssl_verify_cert": False
}

DB_Error = mysql.connector.Error
def get_db_connection():
    try:
        conn = mysql.connector.connect(**config)
        print("Database connection established successfully.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        return None

# Example usage
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
