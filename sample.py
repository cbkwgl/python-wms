    page.add(ft.Row(controls=[ft.Text("A"), ft.Text("B"), ft.Text("C")]))
    t = ft.Text()
    page.add(t)  # it's a shortcut for page.controls.append(t) and then page.update()
    for i in range(10):
        t.value = f"Step {i}"
        page.update()
        time.sleep(0.11)

    page.add(
        ft.Row(
            controls=[
                ft.TextField(label="Your name"),
                ft.ElevatedButton(text="Say my name!"),
            ]
        )
    )
