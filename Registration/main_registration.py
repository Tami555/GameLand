import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from string import digits

class Registration(QMainWindow):
    """Класс для регистрации"""
    """ Родительский класс, от него идет выбор -> регистрация или вход"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(625, 778)
        self.move(400, 0)
        uic.loadUi(r'Registration\Main_sign_up.ui', self)

        # подключаемся к БД
        self.database = sqlite3.connect('Users_Gameland.sqlite')
        self.cur = self.database.cursor()

        # подключение методов к кнопкам: входа и регистрации
        self.btn_sign_up.clicked.connect(self.sign_up)
        self.btn_login_up.clicked.connect(self.log_in)

    def clids_window(self, l, s):
        # создание окон входа и регистрации (дети)
        self.login = l
        self.sign_up = s

    def sign_up(self):
        # показываем окно регистрации(SignUp)
        self.sign_up.show()

    def log_in(self):
        # показываем окно входа (Login())
        self.login.show()

    # ДЛЯ ДРУГИХ 2-Х ОКОН (РЕГИСТРИЦИИ И ВХОДА)
    # функции для использования в обоих следующих окнах (зарегистрироваться\войти)
    def create_answer_return(self):
        # создание стрелочки возврата на родительскую страницу
        self.arrow_return.setIcon(QIcon(r'Registration\arrow_return_img.png'))
        self.arrow_return.clicked.connect(self.close)

    @staticmethod
    def check_full_poles(pole, answer):
        # для проверки наличия данных в полях (заполнение полей ввода)
        if pole == '':
            answer.setStyleSheet("color: red;")
            answer.setText('the field must be filled in')
            return False
        answer.setStyleSheet("color: green;")
        answer.setText('good')
        return True

    def create_now_user(self, data):
        # Для записи на компьютер текущего пользователя. (Без повторной регистрации)
        file = open('now_user.txt', 'w', encoding='utf-8')
        file.write(';'.join(map(str, data)))


class Login(Registration):
    """ Дочерний класс, Входа"""
    def __init__(self, parents):
        super().__init__()
        uic.loadUi(r'Registration\Log_in.ui', self)

        self.parents = parents  # родитель
        self.create_answer_return()  # для кнопки возврата
        self.btn_login_up_go.clicked.connect(self.go_login)  # кнопка для окончательного входа

        # получение имя и пароля пользователя
        self.user_name = ''
        self.user_password = ''

    def go_login(self):
        """ Получаем данные из ввода и обращаемся к БД """
        self.user_password = self.line_password.text()
        self.user_name = self.line_name.text()

        n = self.check_full_poles(self.user_name, self.answer_message_1)
        p = self.check_full_poles(self.user_password, self.answer_message_2)
        if p and n:
            self.connection_database(self.user_password, self.user_name)

    def connection_database(self, password, name):
        """ Метод для обращения к БД для получения данных о существующем пользователе (по имени и паролю)"""

        result = self.cur.execute("""
                            SELECT * FROM users
                             WHERE Password = ? AND Name = ?""", (password, name)).fetchone()

        if result is None:
            self.answer_message_2.setStyleSheet("color: red;")
            self.answer_message_2.setText('The username or password is incorrect!!!')

        else:
            print(f'Есть такой Пользователь, это же {result[0]}')
            QTimer.singleShot(1000, self.close)  # закрываем текущее окно
            self.parents.close()  # закрываем родителя
            self.create_now_user(result)

    def closeEvent(self, event):
        """ Перед закрытием окна очищаем ввод"""
        self.line_password.setText('')
        self.answer_message_2.setText('')
        self.line_name.setText('')
        self.answer_message_1.setText('')


class SignUP(Registration):
    def __init__(self, parents):
        super().__init__()
        uic.loadUi(r'Registration\Sign_up.ui', self)
        self.parents = parents
        self.create_answer_return()  # для кнопки возврата

        self.btn_sign_up_go.clicked.connect(self.go_sign)  # кнопка для окончательной регистрации
        self.user_name = ''
        self.user_password = ''
        self.user_email = ''

    def go_sign(self):
        """ Получаем данные из ввода и обращаемся к БД"""
        self.user_name = self.line_name.text()
        self.user_password = self.line_password.text()
        self.user_email = self.line_email.text()

        #  Проверяем наличие данных в полях
        n = self.check_full_poles(self.user_name, self.answer_message_1)
        p = self.check_full_poles(self.user_password, self.answer_message_2)
        e = self.check_full_poles(self.user_email, self.answer_message_3)
        if n and p and e:
            self.connection_database(self.user_password)

    def connection_database(self, password):
        """ Обращение к БД для создания новой записи о пользователе"""
        if any([x not in digits for x in self.user_password]):
            self.answer_message_2.setStyleSheet("color: red;")
            self.answer_message_2.setText('The password must consist of numbers only!!!!')

        else:
            result = self.cur.execute("""
                                        SELECT * FROM users WHERE Password = ?""", (password,)).fetchone()
            if result is None:
                self.cur.execute("""
                        INSERT INTO users(Name, Password, Email)
                        VALUES(?, ?, ?)""", (self.user_name, self.user_password, self.user_email))
                self.create_now_user((self.user_name, self.user_password, self.user_email, '0'))
                QTimer.singleShot(1000, self.close)  # закрываем текущее окно
                self.parents.close()  # закрываем родителя

            else:
                self.answer_message_2.setStyleSheet("color: red;")
                self.answer_message_2.setText('This password is busy, come up with another one')
            self.database.commit()

    def closeEvent(self, event):
        # перед закрытием окна очищаем ввод
        self.line_password.setText('')
        self.answer_message_2.setText('')
        self.line_name.setText('')
        self.answer_message_1.setText('')
        self.line_email.setText('')
        self.answer_message_3.setText('')

# login = Login()
# sign_up = SignUP()
# win = Registration()
# win.clids_window(login, sign_up)
# win.show()
# sys.exit(app.exec())
