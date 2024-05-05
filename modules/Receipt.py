import flet as ft
import sqlite3
import datetime
from tablecreate import create_tables

# What's Pending?
# 1. SHIPMENT_INBOUND's Actual Receipt is not getting updated
# 2. Audit Updates for Over GR and Non Advised Receipt


def main(page: ft.Page):

    SITE = "0001"
    # Initiate the cursor
    connection = sqlite3.connect("wms.db", check_same_thread=False)
    cursor = connection.cursor()

    # Create Tables
    create_tables()

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

        nonadvcheck_entry = (SITE, text_field1.value, text_field2a.value)

        nonadvcheck = cursor.execute(
            "SELECT *  FROM SHIPMENT_INBOUND WHERE SITE = ? AND ASN = ? AND PRODUCT = ?",
            nonadvcheck_entry,
        )
        if cursor.fetchone() is not None:
            receipt_subtype = ""
        else:
            receipt_subtype = "RECEIPTNONADV"

        audit_entry = (
            int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")),
            datetime.datetime.now().strftime("%d-%m-%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"),
            SITE,
            "RECEIPT",
            receipt_subtype,
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
