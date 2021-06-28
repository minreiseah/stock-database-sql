import mysql.connector
from mysql.connector import errorcode
from securities_master.mysql_instance import connect_mysql_instance

# Connects to the MySQL instance
cnx, cursor = connect_mysql_instance()

# TABLES
TABLES = {}

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
    ticker            varchar(32) NOT NULL ,
    instrument        varchar(64) NOT NULL ,
    exchange          varchar(64) NOT NULL ,
    market            varchar(64) NULL ,
    name              varchar(255) NULL ,
    sector            varchar(255) NULL ,
    industry          varchar(255) NULL ,
    currency          varchar(64) NULL ,
    created_date      timestamp NOT NULL ,
    last_updated_date timestamp NOT NULL ,

    PRIMARY KEY (id)
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
    CONSTRAINT FK_1 FOREIGN KEY index_data_vendor_id (data_vendor_id) REFERENCES DataVendor (id),
    KEY index_symbol_id (symbol_id),
    CONSTRAINT FK_2 FOREIGN KEY index_symbol_id (symbol_id) REFERENCES Symbol (id)
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



