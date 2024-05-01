import sqlite3
import xml.etree.ElementTree as ET
import os

connection = sqlite3.connect("wms.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS PO 
        (PO_NUM TEXT NOT NULL, ORDER_DATE TEXT NOT NULL, SUPPLIER TEXT NOT NULL, PRODUCT TEXT NOT NULL, PRICE TEXT NOT NULL, QUANTITY INTEGER DEFAULT 0, QUANTITY_RECEIVED INTEGER DEFAULT 0,
        CONSTRAINT PK_ASN PRIMARY KEY (PO_NUM, SUPPLIER, PRODUCT))
        """
)
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS ASN 
        (SOURCE TEXT NOT NULL, DESTINATION TEXT NOT NULL, ASN_NUM TEXT NOT NULL, PO_NUM TEXT NOT NULL, SHIP_DATE TEXT NOT NULL, PRODUCT TEXT NOT NULL, QUANTITY INTEGER DEFAULT 0, QUANTITY_RECEIVED INTEGER DEFAULT 0,
        CONSTRAINT PK_ASN PRIMARY KEY (SOURCE, DESTINATION, PO_NUM, ASN_NUM, PRODUCT))
        """
)
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS ASN_PO 
        (SOURCE TEXT NOT NULL, DESTINATION TEXT NOT NULL, ASN_NUM TEXT NOT NULL, PO_NUM TEXT NOT NULL, PROCESSED TEXT,
        CONSTRAINT PK_ASNPO PRIMARY KEY (SOURCE, DESTINATION, PO_NUM, ASN_NUM))
        """
)


def po_load(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for item in root.findall("./Items/Item"):
        data_raw = dict(
            root.items()
            + [(root.getchildren()[0].tag, root.getchildren()[0].text)]
            + item.items()
            + [(item.getchildren()[2].tag, item.getchildren()[2].text)]
            + [(item.getchildren()[1].tag, item.getchildren()[1].text)]
        )
        data_raw = tuple(data_raw.values()) + (0,)
        try:
            cursor.execute("INSERT INTO PO VALUES (?, ?, ?, ?, ?, ?, ?)", data_raw)
            connection.commit()
        except:
            print("Attempt to insert Duplicate Records into PO ", data_raw)


def asn_load(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for item in root.findall("./Items/Item"):
        data_raw = dict(
            [(root.getchildren()[0].tag, root.getchildren()[0].text)]
            + [(root.getchildren()[1].tag, root.getchildren()[1].text)]
            + root.items()
            + item.items()
            + [(item.getchildren()[0].tag, item.getchildren()[0].text)]
        )
        data_raw = tuple(data_raw.values()) + (0,)
        try:
            cursor.execute("INSERT INTO ASN VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data_raw)
            connection.commit()
        except:
            print("Attempt to insert Duplicate Records into ASN ", data_raw)
        try:
            cursor.execute(
                "INSERT INTO ASN_PO VALUES (?, ?, ?, ?, ?)", data_raw[0:4] + ("",)
            )
            connection.commit()
        except:
            pass


for file in os.listdir("./inbound/purchase_order"):
    file = "./inbound/purchase_order" + "/" + file
    po_load(file)

for file in os.listdir("./inbound/receipt_asn"):
    file = "./inbound/receipt_asn" + "/" + file
    asn_load(file)
