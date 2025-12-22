import mysql.connector

def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Microsoft@18",
            database="gp_insp_db"
        )
        return conn
    except mysql.connector.Error as err:
        print("DB CONNECTION ERROR:", err)
        raise
