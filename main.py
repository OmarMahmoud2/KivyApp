from kivy.app import App
from kivy.lang import Builder
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS User (id integer primary key autoincrement, username varchar(30) unique, password varchar(50))")

Builder.load_file('design.kv')


class LoginScreen(Screen):

    def login(self, uname, pword):
        cur.execute(f"SELECT username, password FROM User WHERE username == ? AND password == ?", (uname.text,pword.text))
        data = cur.fetchall()
        print(data)
        if data != []:
            self.manager.current = 'main_window'
            self.ids.login_error.text = ""
        else:
            self.ids.login_error.text = 'Wrong Username Or Password, Try again'

    def sign_up(self):
        self.manager.current = 'sign_up_screen'


class MainWindow(Screen):

    def logout(self):
        self.manager.current = 'login_screen'
        print('logout')

    def help(self, feel):
        if str(feel).lower() == 'happy':
            self.ids.answer.text = 'This time will pass, so cherish this moment'
        elif str(feel).lower() == 'sad':
            self.ids.answer.text = 'This time will pass, so thankful for what you have, also sadness toughen us up'
        elif str(feel).lower() == 'loved':
            self.ids.answer.text = 'This is a beautiful and unique thing to feel, appreciate the people who love you'
        elif str(feel).lower() == 'depressed':
            self.ids.answer.text = 'This time will pass, think of other people who suffered and made it to the other side'
        else:
            self.ids.answer.text = 'This is new to me'

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):

    def sign_up(self, uname, pword):
        print(uname.text, pword.text)
        cur.execute("INSERT INTO User (username, password) VALUES (?,?)", (uname.text, pword.text))
        conn.commit()
        self.manager.current = 'sign_up_success'

class SignUpSuccess(Screen):

    def sign_in(self):
        self.manager.current = 'login_screen'

class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()