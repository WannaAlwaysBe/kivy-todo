from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
import datetime
from datetime import date
from dbManager import DatabaseManager

Window.size = (350, 600)


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):

    title = StringProperty()
    description = StringProperty()
    status = BooleanProperty()


class ToDoApp(MDApp):

    def build(self):
        global screen_manager
        global data_manager
        data_manager = DatabaseManager()
        data_manager.create_table()
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("AddTodo.kv"))
        return screen_manager

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        current_date = f"{days[wd]}, {day} {month} {year}"
        screen_manager.get_screen("main").date.text = current_date

        data = data_manager.get_todo(current_date)

        for e in data:
            screen_manager.get_screen("main").todo_list.add_widget(
                TodoCard(title=e[0], description=e[1], status = e[3]))

    def on_complete(self, checkbox, value, description, title):
        data_manager.update_todo(
            title.text,
            description.text,
            screen_manager.get_screen("main").date.text,
            value
        )

    def add_todo(self, title, description):
        if title != "" and description != "":
            screen_manager.current = "main"
            screen_manager.transition.direction = "right"
            if data_manager.add_todo(title, description,
                             screen_manager.get_screen("main").date.text):
                screen_manager.get_screen("main").todo_list.add_widget(TodoCard(
                    title = title,
                    description = description,
                    status = False
                ))
            screen_manager.get_screen("add_todo").description.text = ""
            screen_manager.get_screen("add_todo").title.text = ""
        elif title == "":
            Snackbar(
                text="Title is missing!",
                snackbar_x = "10dp",
                snackbar_y = "10dp",
                size_hint_y = .08,
                size_hint_x = (Window.width - (dp(10) * 2)) / Window.width,
                bg_color = (1, 170/255, 23/255, 1),
                font_size = "18sp"
            ).open()
        elif description == "":
            Snackbar(
                text="Description is missing!",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_y=.08,
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                bg_color=(1, 170/255, 23/255, 1),
                font_size="18sp"
            ).open()


if __name__ == "__main__":
    ToDoApp().run()
