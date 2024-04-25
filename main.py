import flet as ft
import sqlite3
import datetime


def main(page: ft.Page):
    connection = sqlite3.connect("wms.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS GOODS_RECEIPT (ASN TEXT, PRODUCT TEXT, QUANTITY INTEGER)"
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS AUDIT 
        (TIME_STAMP INT, TRANS_DATE STRING, TRANS_TIME STRING, TRANS_TYPE TEXT, TRANS_SUBTYPE TEXT, 
        REASON_CODE TEXT, REFERENCE TEXT, PRODUCT TEXT, QUANTITY INTEGER)"""
    )

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
        entry = (text_field1.value, text_field2a.value, text_field2b.value)
        new_task.value = ""
        cursor.execute("INSERT INTO GOODS_RECEIPT VALUES (?, ?, ?)", entry)
        connection.commit()
        audit_entry = (
            int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")),
            datetime.datetime.now().strftime("%d-%m-%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"),
            "RECEIPT",
            "",
            "",
            text_field1.value,
            text_field2a.value,
            text_field2b.value,
        )
        cursor.execute(
            "INSERT INTO AUDIT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", audit_entry
        )
        connection.commit()
        page.update()

    new_task = ft.Row(controls=[text_field2a, text_field2b], visible=False)

    btn_text2 = ft.ElevatedButton(
        text="Enter Product and Quantity", on_click=add_clicked, visible=False
    )

    page.add(ft.Row(controls=[new_task, btn_text2, btn_text3]))

    page.update()


ft.app(main)
