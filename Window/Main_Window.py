import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap


class Note:
    """ Класс для создания игр и рекордов пользователей по ним """
    def __init__(self, img, Title, game_in_D):
        self.img = img
        self.Title = Title
        self.game_in_D = game_in_D  # Запись в БД
        self.play_btn = QPushButton('Play')

    @staticmethod
    def create_form():
        forma = QLabel()
        forma.setFixedSize(591, 91)
        forma.setStyleSheet('background: black;')
        return forma

    def create_Game_form(self):
        """ Форма для игры"""
        game_form = self.create_form()
        lay_h = QHBoxLayout()

        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(self.img))
        self.icon.setFixedSize(50, 50)

        self.title = QLabel(f"{self.Title}")
        self.title.setFixedSize(111, 41)
        self.title.setStyleSheet("""
        font-family: "Cascadia Momo SemiBold";
        font-size: 20pt;
        color: white;""")

        self.play_btn.setFixedSize(141, 41)
        self.play_btn.setStyleSheet("""
        font-family: "Cascadia Code SemiBold";
        font-size: 10pt;
        color: white;
        background: #46CC00;
        """)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        lay_h.addWidget(self.icon)
        lay_h.addWidget(self.title)
        lay_h.addWidget(self.play_btn)
        game_form.setLayout(lay_h)
        return game_form

    def create_Record_form(self):
        """ Форма для рекордов """
        record_form = self.create_form()
        lay_h2 = QHBoxLayout()

        self.title2 = QLabel(f"{self.Title}")
        self.title2.setFixedSize(111, 41)
        self.title2.setStyleSheet("""
                font-family: "Cascadia Momo SemiBold";
                font-size: 20pt;
                color: white;""")

        lay_h2.addWidget(self.title2)

        # получаем Рекорд пользователя
        database = sqlite3.connect('Users_Gameland.sqlite')
        cur = database.cursor()
        try:
            file = open(r"now_user.txt", 'r', encoding='utf-8')
            infa = file.readline()
            if infa != '':
                infa = infa.split(';')
                record = cur.execute(f"""SELECT {self.game_in_D}
                        FROM users WHERE Password = {infa[1]}""").fetchone()

                print(f"""SELECT {self.game_in_D}
                        FROM users WHERE Password = {infa[1]}""")

                self.record = QLabel(f"{record[0]}")
                self.record.setFixedSize(111, 41)
                self.record.setStyleSheet("""
                font-family: "Cascadia Momo SemiBold";
                font-size: 20pt;
                color: white;""")

                lay_h2.addWidget(self.record)
                file.seek(0)
        except FileNotFoundError:
            print('Проблема с пользовательским файлом!!!!!')
        record_form.setLayout(lay_h2)
        return record_form


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Window\Main_Window.ui', self)

        # Для My profile
        self.full_infa_user()
        self.leave_account_btn.clicked.connect(self.leave_account)

    def full_infa_user(self):
        # заполняет информацию о пользователе (My profile)
        try:
            file = open(r"now_user.txt", 'r', encoding='utf-8')
            infa = file.readline()
            print('INFA', infa)
            if infa != '':
                infa = infa.split(';')
                self.for_name.setText(infa[0])
                self.for_email.setText(infa[2])
                self.for_password.setText(infa[1])
                file.seek(0)
        except Exception as e:
            print('Проблема с пользовательским файлом!!!!!', e)

    def leave_account(self):
        # Спрашиваем у пользователя подтверждение на удаление элементов
        valid = QMessageBox.question(
            self, '', "Do you really want to log out of your account? ",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # Если пользователь ответил утвердительно, выходим из аккаунта.
        if valid == QMessageBox.StandardButton.Yes:
            with open(r"now_user.txt", 'w', encoding='utf-8') as file:
                file.write('')
                self.closen()
                self.close()

    def add_note(self, note):
        """ Добавляет формы в само окно """
        self.games_lay.addWidget(note.create_Game_form())
        self.records_lay.addWidget(note.create_Record_form())

    def closen(self):
        """ Очищает при закрытии"""
        self.games_lay = QVBoxLayout()
        self.records_lay = QVBoxLayout()


