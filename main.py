import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = "To-Do List"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    filter_type = "all"

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(
                create_task_row(task_id, task_text, completed)
            )
        page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_tasks()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(
            value=task_text,
            read_only=True,
            expand=True
        )

        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(_):
            task_field.read_only = False
            task_field.focus()
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, new_task=task_field.value)
            task_field.read_only = True
            load_tasks()

        return ft.Row([
            checkbox,
            task_field,
            ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit),
            ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task),
        ])

    def add_task(_):
        if task_input.value:
            main_db.add_task(task_input.value)
            task_input.value = ""
            load_tasks()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_tasks()

    task_input = ft.TextField(
        label="Введите задачу",
        expand=True,
        on_submit=add_task
    )

    add_button = ft.IconButton(
        icon=ft.Icons.SEND,
        on_click=add_task
    )

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
            ft.ElevatedButton("Ожидают", on_click=lambda e: set_filter("uncompleted")),
            ft.ElevatedButton("Готово", on_click=lambda e: set_filter("completed")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    page.add(
        ft.Row([task_input, add_button]),
        filter_buttons,
        task_list
    )

    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
