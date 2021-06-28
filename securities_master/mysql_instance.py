from __future__ import print_function # I have no idea why this is here someone explain

import mysql.connector
from mysql.connector import errorcode

DB_HOST = 'localhost'
DB_USER = 'sec_user'
DB_PASS = 'password'
DB_NAME = 'securities_master'

# Connects to the MySQL instance
def connect_mysql_instance():
    try:
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                                host=DB_HOST)
        cursor = cnx.cursor()
        print("Connected to MySQL instance")

    except mysql.connector.Error as err:
        print(err.msg)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Invalid database")
        else:
            print("Unexpected error has occured")
        exit(1)
    
    # Connects to MySQL database/creates one if does not exist
    def create_database():
        try:
            cursor.execute(
                "CREATE DATABASE {}".format(DB_NAME)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}\n{}".format(DB_NAME, err.msg))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME)) # tries to connect to db
        print("Connected to database: {}".format(DB_NAME))

    except mysql.connector.Error as err:
        print("Database: {} does not exist".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("Database created successfully")
            cnx.database = DB_NAME
        else:
            print(err.msg)
            exit(1)
    
    return cnx, cursor


        