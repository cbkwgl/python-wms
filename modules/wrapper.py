import flet as ft


def main(page: ft.Page):

    functions = [
        ("Storage", "Storage Clicked"),
        ("Picking", "Picking Clicked"),
        ("Packing", "Packing Clicked"),
        ("Slotting", "Slotting Clicked"),
        ("Despatch", "Despatch Clicked"),
        ("Adjustments", "Adjustments Clicked"),
        ("Ordering", "Ordering Clicked"),
        ("Order Confirmation", "Order Confirmation Clicked"),
        ("Loading", "Loading Clicked"),
        ("Receiving", "Receiving Clicked"),
    ]

    page.title = "Warehouse Management System"
    page.padding = 50
    page.update()

    page.appbar = ft.AppBar(
        actions=[
            ft.IconButton(
                ft.icons.HOME,
                icon_color=ft.colors.BLUE_800,
                icon_size=60,
                tooltip="Home Page",
                on_click=lambda _: page.go("/"),
            ),
        ],
    )

    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=350,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    page.add(images)

    def button_clicked(e):
        for label, message in functions:
            if label == e.control.content.value:
                print(message)

    for i in range(0, len(functions)):
        images.controls.append(
            ft.TextButton(
                content=ft.Text(functions[i - 1][0], size=40),
                on_click=button_clicked,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(
                        radius=20,
                    ),
                    bgcolor=ft.colors.BLUE_50,
                ),
            )
        )
    page.update()


ft.app(target=main)
