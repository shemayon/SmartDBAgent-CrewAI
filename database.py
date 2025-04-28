import mysql.connector

#MySQL Database Connection Setup
def get_db_conection():
    return mysql.connector.connect(
        host="localhost",
        user="crewai",
        password="crewai",
        database="Student",
        port=3306
    )