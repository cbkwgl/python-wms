import flet as ft


def main(page):
    page.adaptive = True
    t = ft.Text(value="Quality Check", color="cyan", size=33)
    page.controls.append(t)

    # Pending -> Unlock, New Line, Table Data

    def btn_text1_clicked(e):
        if text_field2a.value + text_field1.value == "":
            pass
        elif text_field2a.value == "":
            page.add(
                ft.Text(
                    value="ASN/Slot: "
                    + text_field1.value
                    + " Reason: "
                    + text_field3.value
                )
            )
        elif text_field1.value == "":
            page.add(
                ft.Text(
                    value="Product: "
                    + text_field2a.value
                    + " Quantity: "
                    + text_field2b.value
                    + " Reason: "
                    + text_field3.value
                )
            )

    text_field1 = ft.TextField(label="Enter Reference")
    text_field2a = ft.TextField(label="Enter Product")
    text_field2b = ft.TextField(label="Enter Quantity")
    text_field3 = ft.TextField(label="Enter Reason")
    btn_text1 = ft.ElevatedButton(text="Confirm", on_click=btn_text1_clicked)

    def radiogroup_changed(e):
        cg.visible = False
        if e.control.value == "Product":
            page.add(
                ft.Row(controls=[text_field2a, text_field2b, text_field3, btn_text1])
            )
        if e.control.value in ("ASN", "Slot"):
            page.add(ft.Row(controls=[text_field1, text_field3, btn_text1]))

        page.update()

    t = ft.Text()
    cg = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Product", label="Product"),
                ft.Radio(value="ASN", label="ASN"),
                ft.Radio(value="Slot", label="Slot"),
            ]
        ),
        on_change=radiogroup_changed,
    )

    page.add(cg)


ft.app(target=main)
