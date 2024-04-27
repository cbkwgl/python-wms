import flet as ft
import sqlite3
import datetime

# What's Pending?
# 1. SHIPMENT_INBOUND's Actual Receipt is not getting updated
# 2. Audit Updates for Over GR and Non Advised Receipt


def main(page: ft.Page):

    SITE = "0001"
    # Define tables - SHIPMENT_INBOUND, GOODS_RECEIPT, AUDIT, PRODUCT_QTY - Extend the logic to include site.
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

    # Test Data: This data should come from reading an XML batch which comes from a queue
    # cursor.execute("INSERT INTO SHIPMENT_INBOUND VALUES ('0001','PRQS', '1234', 10, 0)")
    # connection.commit
    #
    # cursor.execute("INSERT INTO SHIPMENT_INBOUND VALUES ('0001','ABCD', '1234', 10, 0)")
    # connection.commit

    page.adaptive = True
    t = ft.Text(value="Enter Shipment Number", color="cyan", size=33)
    page.controls.append(t)
    text_field1 = ft.TextField(label="Enter Shipment Number")
    text_field2a = ft.TextField(label="Enter Product")
    text_field2b = ft.TextField(label="Enter Quantity")

    def btn_text1_clicked(self):
        t.value = "Entered Shipment Number: " + text_field1.value
        text_field1.visible = False
        btn_text1.visible = False
        ft.Text(value="Enter Product and Quantity")
        new_task.visible = True
        btn_text2.visible = True
        btn_text3.visible = True
        page.update()

    def close_window(e):
        page.window_destroy()

    btn_text1 = ft.ElevatedButton(
        text="Enter Shipment Number", on_click=btn_text1_clicked
    )

    btn_text3 = ft.ElevatedButton(
        text="Close Session",
        on_click=close_window,
        icon="close",
        icon_color="red",
        color="red",
        visible=False,
    )

    page.add(ft.Row(controls=[text_field1, btn_text1]))

    def add_clicked(e):
        page.add(
            ft.Text(
                value="Product: "
                + text_field2a.value
                + "     Quantity:"
                + text_field2b.value
            )
        )
        entry = (SITE, text_field1.value, text_field2a.value, text_field2b.value)
        new_task.value = ""
        cursor.execute("INSERT INTO GOODS_RECEIPT VALUES (?, ?, ?, ?)", entry)
        connection.commit()
        audit_entry = (
            int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")),
            datetime.datetime.now().strftime("%d-%m-%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"),
            SITE,
            "RECEIPT",
            "",
            "",
            text_field1.value,
            text_field2a.value,
            text_field2b.value,
        )
        cursor.execute(
            "INSERT INTO AUDIT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", audit_entry
        )
        connection.commit()
        shipment_inbound_update_entry = (
            text_field2b.value,
            SITE,
            text_field1.value,
            text_field2a.value,
        )
        print(shipment_inbound_update_entry)
        cursor.execute(
            """UPDATE SHIPMENT_INBOUND 
            SET QUANTITY_RECEIVED = QUANTITY_RECEIVED + ? 
            WHERE SITE = ? AND ASN = ? AND PRODUCT = ?
            """,
            shipment_inbound_update_entry,
        )
        connection.commit()
        site_product = (SITE, text_field2a.value)

        cursor.execute(
            """
            INSERT OR IGNORE INTO product_qty (site, product) values (?,?)
            """,
            site_product,
        )
        connection.commit()
        site_product_qty = (text_field2b.value, SITE, text_field2a.value)
        cursor.execute(
            """
            UPDATE product_qty 
            SET quantity_available = quantity_available + ? WHERE site = ? and product = ?
            """,
            site_product_qty,
        )

        page.update()

    new_task = ft.Row(controls=[text_field2a, text_field2b], visible=False)

    btn_text2 = ft.ElevatedButton(
        text="Enter Product and Quantity", on_click=add_clicked, visible=False
    )

    page.add(ft.Row(controls=[new_task, btn_text2, btn_text3]))

    page.update()


ft.app(main)
