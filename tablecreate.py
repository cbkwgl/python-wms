import sqlite3


def create_tables():
    connection = sqlite3.connect("wms.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS SHIPMENT_INBOUND 
        (SITE TEXT NOT NULL, ASN TEXT NOT NULL, PRODUCT TEXT NOT NULL, QUANTITY INTEGER DEFAULT 0, QUANTITY_RECEIVED INTEGER DEFAULT 0,
        CONSTRAINT PK_SHP_INB PRIMARY KEY (SITE, ASN, PRODUCT))
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS GOODS_RECEIPT 
        (SITE TEXT NOT NULL, ASN TEXT NOT NULL, PRODUCT TEXT NOT NULL, QUANTITY INTEGER DEFAULT 0)
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS AUDIT 
        (TIME_STAMP INT, TRANS_DATE TEXT, TRANS_TIME TEXT, SITE TEXT, TRANS_TYPE TEXT, TRANS_SUBTYPE TEXT, 
        REASON_CODE TEXT, REFERENCE TEXT, PRODUCT TEXT, QUANTITY INTEGER)
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS PRODUCT_QTY 
        (SITE TEXT NOT NULL, PRODUCT TEXT NOT NULL, QUANTITY_AVAILABLE INTEGER DEFAULT 0, QUANTITY_QUALITY INTEGER DEFAULT 0, 
        QUANTITY_ORDERED INTEGER DEFAULT 0, QUANTITY_PICKED INTEGER DEFAULT 0, QUANTITY_TO_DESPATCH INTEGER DEFAULT 0,
        CONSTRAINT PRODUCT_QTY_PRIMARY PRIMARY KEY (SITE, PRODUCT))
        """
    )