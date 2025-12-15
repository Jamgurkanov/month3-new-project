from db import main_db
import flet as ft 


def main(page: ft.Page):
    page.title = 'ToDO List'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list =ft.Column(spacing=30)

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_task():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))
        page.update()


    def create_task_row(task_id, task_text):
        task_filed = ft.TextField(value=task_text, read_only=True, expand=True)

        def enable_edit(_):
            task_filed.read_only = False
            task_filed.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_filed.value)
            task_filed.read_only = True
            task_filed.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id=task_id)
            load_tasks()
            


        delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=delete_task)

        return ft.Row([task_filed, edit_button, save_button, delete_button])
    

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            print(f'Задача {task} completed - id {task_id}')
            task_input.value = None
            page.update()

    task_input = ft.TextField(label='Введите задачу', on_submit=add_task, expand=True)
    task_input_button = ft.IconButton(icon=ft.Icons.SEND, on_click=add_task)

    page.add(ft.Row([task_input, task_input_button]), task_list)
    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)


    