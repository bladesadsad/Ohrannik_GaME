import sqlite3
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QWidget
import sys

class BasementUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Управление пропусками')
        self.setGeometry(500, 500, 500, 500)
        self.name_label = QLabel('Фамилия:')
        self.name_input = QLineEdit()
        self.surname_label = QLabel('Имя:')
        self.surname_input = QLineEdit()
        self.patronymic_label = QLabel('Отчество:')
        self.patronymic_input = QLineEdit()
        self.birthdate_label = QLabel('Дата рождения:')
        self.birthdate_input = QLineEdit()
        self.passnumber_label = QLabel('Номер пропуска:')
        self.passnumber_input = QLineEdit()
        self.check_button = QPushButton('Пройти на работу')
        self.check_button.clicked.connect(self.check_basement)
        self.check_result = QLabel('')

        self.check_button1 = QPushButton('Выйти с работы')
        self.check_button1.clicked.connect(self.check_basement_to_left)
        self.create_pass_button = QPushButton('Выдать временной пропуск')
        self.create_pass_button.clicked.connect(self.create_temporary_pass)
        self.ex = QPushButton('Выйти по пропуску')
        self.ex.clicked.connect(self.exit_with_pass)
        self.parking_car = QPushButton('Взять талон для сотрудников')
        self.parking_car.clicked.connect(self.parking_working)
        self.parking_car1 = QPushButton('Взять талон для гостей')
        self.parking_car1.clicked.connect(self.parking_guest)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)
        self.layout.addWidget(self.patronymic_label)
        self.layout.addWidget(self.patronymic_input)
        self.layout.addWidget(self.birthdate_label)
        self.layout.addWidget(self.birthdate_input)
        self.layout.addWidget(self.passnumber_label)
        self.layout.addWidget(self.passnumber_input)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.check_result)
        self.layout.addWidget(self.create_pass_button)
        self.layout.addWidget(self.ex)
        self.layout.addWidget(self.check_button1)
        self.layout.addWidget(self.parking_car)
        self.layout.addWidget(self.parking_car1)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def check_basement(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        passnumber = self.passnumber_input.text()
        if surname and name and patronymic and birthdate and passnumber:
            db_connection = sqlite3.connect('basement.db')
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT * FROM basement WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                (surname, name, patronymic, birthdate,passnumber))
            basement = cursor.fetchone()
            if basement:
                self.check_result.setText('Сотрудник прошёл на работу.')
                time = datetime.datetime.now()
                cursor.execute(
                    "UPDATE basement SET time_in = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                    (time, surname, name, patronymic, birthdate, passnumber))
                db_connection.commit()
            else:
                self.check_result.setText('Сотрудник не смог пройти валидацию')
            db_connection.close()
        else:
            self.check_result.setText('Заполните все поля')

    def check_basement_to_left(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        passnumber = self.passnumber_input.text()
        if surname and name and patronymic and birthdate and passnumber:
            db_connection = sqlite3.connect('basement.db')
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT * FROM basement WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                (surname, name, patronymic, birthdate,passnumber))
            basement = cursor.fetchone()
            if basement:
                self.check_result.setText('Сотрудник вышел с работы.')
                time_out = datetime.datetime.now()
                cursor.execute(
                    "UPDATE basement SET time_out = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                    (time_out, surname, name, patronymic, birthdate,passnumber))
                db_connection.commit()
            else:
                self.check_result.setText('Сотрудник не смог пройти валидацию')
            db_connection.close()
        else:
            self.check_result.setText('Заполните все поля')

    def exit_with_pass(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        birthdate = self.birthdate_input.text()
        patronymic = self.patronymic_input.text()
        db_connection = sqlite3.connect('visitors.db')
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM visitors WHERE surname = ? AND name = ? AND birthdate = ? and patronymic = ? ",(surname, name, birthdate,patronymic))
        visitor = cursor.fetchone()
        if visitor:
            self.check_result.setText('Выход по пропуску зарегистрирован')
            cursor.execute("DELETE FROM visitors WHERE id = ?", (visitor[0],))
            db_connection.commit()
        else:
            self.check_result.setText(
                'Посетитель не найден в базе данных или пропуск не действителен. Обратитесь к старшему охраннику')
        db_connection.close()

    def create_temporary_pass(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        if surname and name and patronymic and birthdate:
            db_connection = sqlite3.connect('visitors.db ')
            cursor = db_connection.cursor()
            entry_time = datetime.datetime.now()
            valid_hours, ok = QInputDialog.getInt(self, 'Выдача временного пропуска', 'Введите количество минут для пропуска:')
            if ok:
                expiration_time = entry_time + datetime.timedelta(minutes=valid_hours)
                cursor.execute("INSERT INTO visitors (surname, name, patronymic, birthdate) VALUES (?, ?, ?, ?)", (surname, name, patronymic, birthdate))
                visitor_id = cursor.lastrowid
                cursor.execute("INSERT INTO guest_passes (visitor_id, entry_time, valid_hours, expiration_time) VALUES (?, ?, ?, ?)", (visitor_id, entry_time, valid_hours, expiration_time))
                db_connection.commit()
                self.check_result.setText('Посетителю выдан временной пропуск до ' + str(expiration_time))
            else:
                self.check_result.setText('Отменено')
        else:
            self.check_result.setText('Введите фамилию, имя, отчество и дату рождения посетителя')

    working_passes = 0
    guest_passes = 0

    def parking_working(self):
        name = self.name_input.text()
        number = self.passnumber_input.text()
        surname = self.surname_input.text()
        patronymic = self.patronymic_input.text()
        if name and number and patronymic and surname:
            if self.working_passes < 5:
                self.working_passes += 1
                self.check_result.setText('Парковочный талон для сотрудника выдан')
            elif self.guest_passes < 5:
                self.guest_passes += 1
                self.check_result.setText('Парковочный талон для посетителя выдан')
            else:
                self.check_result.setText('Извините, лимит парковочных талонов исчерпан')
        else:
            self.check_result.setText('Введите фамилию, имя, отчество и номер пропуска')

    def parking_guest(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        patronymic = self.patronymic_input.text()
        if name and surname and patronymic:
            if self.guest_passes < 5:
                self.guest_passes +=1
                self.check_result.setText('Парковочный талон для сотрудника выдан')
            else:
                self.check_result.setText('Извините, лимит парковочных талонов исчерпан')
        else:
            self.check_result.setText('Введите фамилию, имя и отчество')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    basement_ui = BasementUI()
    basement_ui.show()
    sys.exit(app.exec())