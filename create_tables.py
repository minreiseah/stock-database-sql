from __future__ import print_function # I have no idea why this is here someone explain

import mysql.connector
from mysql.connector import errorcode

# Connects to the MySQL instance
DB_HOST = 'localhost'
DB_USER = 'sec_user'
DB_PASS = 'password'
DB_NAME = 'securities_master'

try:
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST)
    cursor = cnx.cursor()

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
            "CREATE DATABASE {} DEFAULT CHARACTERS SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}\n{}".format(DB_NAME, err.msg))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME)) # tries to connect to db

except mysql.connector.Error as err:
    print("Database: {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database()
        print("Database created successfully")
        cnx.database = DB_NAME
    else:
        print(err.msg)
        exit(1)


# TABLES
TABLES = {}
TABLES['Exchange'] = ("""
    CREATE TABLE IF NOT EXISTS Exchange
    (
    id                integer NOT NULL AUTO_INCREMENT ,
    abbrev            varchar(32) NOT NULL ,
    name              varchar(255) NOT NULL ,
    city              varchar(255) NULL ,
    country           varchar(255) NULL ,
    currency          varchar(64) NULL ,
    created_date      timestamp NOT NULL ,
    last_updated_date timestamp NOT NULL ,

    PRIMARY KEY (id)
    ) AUTO_INCREMENT=1 ENGINE=INNODB;
""")

TABLES['DataVendor'] = ("""
    CREATE TABLE IF NOT EXISTS DataVendor
    (
    id                integer NOT NULL AUTO_INCREMENT ,
    name              varchar(255) NOT NULL ,
    website_url       varchar(255) NULL ,
    API_endpoint      varchar(255) NULL ,
    created_date      timestamp NOT NULL ,
    last_updated_time timestamp NOT NULL ,

    PRIMARY KEY (id)
    ) AUTO_INCREMENT=1 ENGINE=INNODB;
""")

TABLES['Symbol'] = ("""
    CREATE TABLE IF NOT EXISTS Symbol
    (
    id                integer NOT NULL AUTO_INCREMENT ,
    exchange_id       integer NOT NULL ,
    ticker            varchar(32) NOT NULL ,
    instrument        varchar(64) NOT NULL ,
    name              varchar(255) NULL ,
    sector            varchar(255) NULL ,
    currency          varchar(64) NULL ,
    created_date      timestamp NOT NULL ,
    last_updated_date timestamp NOT NULL ,

    PRIMARY KEY (id),
    KEY index_exchange_id (exchange_id),
    CONSTRAINT FK_1 FOREIGN KEY index_exchange_id (exchange_id) REFERENCES Exchange (id)
    ) AUTO_INCREMENT=1 ENGINE=INNODB;
""")

TABLES['DailyPrice'] = ("""
    CREATE TABLE IF NOT EXISTS DailyPrice 
    (
    id                integer NOT NULL AUTO_INCREMENT ,
    data_vendor_id    integer NOT NULL ,
    symbol_id         integer NOT NULL ,
    price_date        timestamp NOT NULL ,
    open_price        decimal(19,4) NULL ,
    high_price        decimal(19,4) NULL ,
    low_price         decimal(19,4) NULL ,
    close_price       decimal(19,4) NULL ,
    adj_close_price   decimal(19,4) NULL ,
    volume            bigint NULL ,
    created_date      timestamp NOT NULL ,
    last_updated_date timestamp NOT NULL ,

    PRIMARY KEY (id),
    KEY index_data_vendor_id (data_vendor_id),
    CONSTRAINT FK_2 FOREIGN KEY index_data_vendor_id (data_vendor_id) REFERENCES DataVendor (id),
    KEY index_symbol_id (symbol_id),
    CONSTRAINT FK_3 FOREIGN KEY index_symbol_id (symbol_id) REFERENCES Symbol (id)
    ) AUTO_INCREMENT=1 ENGINE=INNODB;
""")

# Create database
def create_table(table):
    table_description = TABLES[table]
    print("Creating table {}".format(table))
    try:
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_ALREADY_EXISTS:
            print("Table: {} already exists.".format(table))
        else:
            print("Failed to create table: {}\n{}".format(table, err.msg))
        exit(1)

for table in TABLES:
    create_table(table)
    print('OK')





cursor.close()
cnx.close()



