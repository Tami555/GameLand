import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from Registration.main_registration import Registration, Login, SignUP
from Window.Main_Window import MainWindow, Note
#Игры
from Sapper_game.sapper_game import SapperGame


class Started(QMainWindow):
    """ Основной класс (самы важный) в нем объединяется и регистрация и игры и само окно"""
    def __init__(self):
        super().__init__()
        uic.loadUi('Started.ui', self)
        self.setFixedSize(625, 778)
        self.move(400, 0)
        self.btn_started.clicked.connect(self.starting)
        self.window = MainWindow()

    def read_file(self):
        with open('now_user.txt', 'r', encoding='utf-8') as file:
            line_data = file.readline()
            file.seek(0)
            return line_data

    def show_window(self):
        self.window = MainWindow()
        self.window.full_infa_user()
        add_lst_games(self.window)
        self.window.show()

    def starting(self):
        self.file = self.read_file()
        if self.file == '':
            self.registration = Registration()
            self.login = Login(self.registration)
            self.sign_up = SignUP(self.registration)
            self.registration.clids_window(self.login, self.sign_up)
            # почему не отображается после завершения регистрации ????
            # registration.destroyed.connect(self.show_window)
            self.registration.show()
        else:
            self.show_window()


def add_lst_games(win):
    """ Для добавления существующих игр в окно """
    #Сапер
    note = Note(r'Sapper_game\icon.png', 'Sapper', 'Sapper_record')
    note.play_btn.clicked.connect(SapperGame)
    win.add_note(note)

app = QApplication(sys.argv)
start = Started()
start.show()
sys.exit(app.exec())
