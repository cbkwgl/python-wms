import flet as ft
import time


def main(page: ft.Page):
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
        page.update()

    btn_text1 = ft.ElevatedButton(
        text="Enter Shipment Number", on_click=btn_text1_clicked
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
        new_task.value = ""
        print(text_field2a.value, text_field2b.value)
        page.update()

    new_task = ft.Row(controls=[text_field2a, text_field2b], visible=False)

    btn_text2 = ft.ElevatedButton(
        text="Enter Product and Quantity", on_click=add_clicked, visible=False
    )

    page.add(ft.Row(controls=[new_task, btn_text2]))

    page.update()


ft.app(main)
