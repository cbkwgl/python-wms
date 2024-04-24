import flet as ft
import time


def main(page: ft.Page):
    t = ft.Text(value="Enter Shipment Number", color="cyan", size=33)
    page.controls.append(t)
    text_field1 = ft.TextField(label="Enter Shipment Number")

    def btn_text1_clicked(self):
        t.value = "Entered Shipment Number: " + text_field1.value
        text_field1.visible = False
        btn_text1.visible = False
        page.add(btn_text2)
        page.update()

    text_field2a = ft.TextField(label="Enter Product")
    text_field2b = ft.TextField(label="Enter Quantity")

    def btn_text2_clicked(self):
        btn_text2.visible = False
        page.add(ft.Row(controls=[text_field2a, text_field2b, btn_text3]))

    def btn_text3_clicked(self):
        print(text_field2a, text_field2b)
        page.add(ft.Row(controls=[text_field2a, text_field2b, btn_text3]))

    btn_text1 = ft.ElevatedButton(
        text="Enter Shipment Number", on_click=btn_text1_clicked
    )
    btn_text2 = ft.ElevatedButton(
        text="Enter Product Details", on_click=btn_text2_clicked
    )
    btn_text3 = ft.ElevatedButton(text="Add another", on_click=btn_text3_clicked)

    page.add(ft.Row(controls=[text_field1, btn_text1]))

    # page.add(ft.ElevatedButton("Enter Product Details", on_click=text_field2))
    page.update()


ft.app(main)
