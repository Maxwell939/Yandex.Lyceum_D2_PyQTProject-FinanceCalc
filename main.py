import calendar
import sys
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QHeaderView, QMessageBox

from MainWindow import Ui_MainWindow
from toJournalAddGain import Ui_Main_AddGain
from toJournalAddExpense import Ui_Main_AddExpense
from toRegularPaymentsAddIncome import Ui_Reg_AddIncome
from toRegularPaymentsAddSpending import Ui_Reg_AddSpending


def add_row(row, table):
    """Добавление строки в таблицу"""

    r = table.rowCount()
    table.insertRow(r)

    for c, val in enumerate(row):
        item = QTableWidgetItem(val)
        # Выравнивание чисел по правому краю
        if val.isdigit():
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight |
                                  Qt.AlignmentFlag.AlignVCenter)
        table.setItem(r, c, item)

    # Настройка отображения заголовков таблицы
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(True)

def del_row(table):
    """Удаление выбранной строки из таблицы"""

    selected_rows = table.selectedIndexes()
    if selected_rows:
        # Подтверждение удаления
        reply = QMessageBox.question(
            None,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранную запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            table.removeRow(selected_rows[0].row())


class ToJournalAddExpense(QDialog, Ui_Main_AddExpense):
    """Диалоговое окно для добавления расхода в журнал"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Подключаем кнопки принятия и отмены
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_inputs(self):
        return [self.lineEdit.text(),
                self.comboBox.currentText(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text()]

    def validate_inputs(self):
        """Проверка корректности введенных данных"""
        name, category, value, comment = self.get_inputs()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название расхода!")
            return False

        if not value or not value.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
            return False

        return True

    def accept(self):
        """Обработка принятия диалога с валидацией"""
        if self.validate_inputs():
            super().accept()


class ToJournalAddGain(QDialog, Ui_Main_AddGain):
    """Диалоговое окно для добавления дохода в журнал"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Подключаем кнопки принятия и отмены
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_inputs(self):
        return [self.lineEdit.text(),
                self.comboBox.currentText(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text()]

    def validate_inputs(self):
        """Проверка корректности введенных данных"""
        name, category, value, comment = self.get_inputs()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название расхода!")
            return False

        if not value or not value.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
            return False

        return True

    def accept(self):
        """Обработка принятия диалога с валидацией"""
        if self.validate_inputs():
            super().accept()


class ToRegularPaymentsAddIncome(QDialog, Ui_Reg_AddIncome):
    """Диалоговое окно для добавления регулярного дохода"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Устанавливаем период "Месяц" по умолчанию
        self.moth_radbtn.setChecked(True)
        # Подключаем кнопки принятия и отмены
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_inputs(self):
        return [self.lineEdit.text(),
                self.comboBox.currentText(),
                self.lineEdit_2.text(),
                self.buttonGroup.checkedButton().text()]

    def validate_inputs(self):
        """Проверка корректности введенных данных"""
        name, category, value, comment = self.get_inputs()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название расхода!")
            return False

        if not value or not value.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
            return False

        return True

    def accept(self):
        """Обработка принятия диалога с валидацией"""
        if self.validate_inputs():
            super().accept()


class ToRegularPaymentsAddSpending(QDialog, Ui_Reg_AddSpending):
    """Диалоговое окно для добавления регулярного расхода"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Устанавливаем период "Месяц" по умолчанию
        self.moth_radbtn.setChecked(True)
        # Подключаем кнопки принятия и отмены
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_inputs(self):
        return [self.lineEdit.text(),
                self.comboBox.currentText(),
                self.lineEdit_2.text(),
                self.buttonGroup.checkedButton().text()]

    def validate_inputs(self):
        """Проверка корректности введенных данных"""
        name, category, value, comment = self.get_inputs()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название расхода!")
            return False

        if not value or not value.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму!")
            return False

        return True

    def accept(self):
        """Обработка принятия диалога с валидацией"""
        if self.validate_inputs():
            super().accept()


class MainWindow(QMainWindow, Ui_MainWindow):
    """Главное окно приложения для учета финансов"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Подключение сигналов кнопок добавления
        self.add_expense_btn.clicked.connect(self.add_expense)
        self.add_gain_btn.clicked.connect(self.add_gain)
        self.add_spending_btn.clicked.connect(self.add_spending)
        self.add_income_btn.clicked.connect(self.add_income)

        # Подключение сигналов кнопок удаления
        self.del_expense_btn.clicked.connect(self.del_expense)
        self.del_gain_btn.clicked.connect(self.del_gain)
        self.del_spending_btn.clicked.connect(self.del_spending)
        self.del_income_btn.clicked.connect(self.del_income)

        # Подключение кнопок загрузки и сохранения
        self.load_btn.clicked.connect(self.load)
        self.save_btn.clicked.connect(self.save)

        # Загрузка данных при запуске
        self.set_table_headers()
        self.load()

    def set_table_headers(self):
        """Установка заголовков для таблиц"""
        headers_journal = ["Название", "Категория", "Сумма", "Примечание"]
        headers_reg_payments = ["Название", "Категория", "Сумма", "Период"]

        self.gains_table.setHorizontalHeaderLabels(headers_journal)
        self.expenses_table.setHorizontalHeaderLabels(headers_journal)
        self.income_table.setHorizontalHeaderLabels(headers_reg_payments)
        self.spending_table.setHorizontalHeaderLabels(headers_reg_payments)

    def load(self):
        """Загрузка данных из базы данных для выбранного месяца"""
        with sqlite3.connect("db/journalDatabase.db") as conn:
            # Очистка таблиц перед загрузкой
            self.income_table.setRowCount(0)
            self.gains_table.setRowCount(0)
            self.expenses_table.setRowCount(0)
            self.spending_table.setRowCount(0)
            self.total.clear()
            self.reg_total.clear()

            cursor = conn.cursor()
            month, year = self.calendar.monthShown(), self.calendar.yearShown()

            try:
                # Загрузка доходов журнала за выбранный месяц
                result = cursor.execute(
                    """SELECT name, category, value, comment
                        FROM Journal_gains WHERE month = ? and year = ?""",
                    (month, year)).fetchall()
                for row in result:
                    add_row(row, self.gains_table)

                # Загрузка расходов журнала за выбранный месяц
                result = cursor.execute(
                    """SELECT name, category, value, comment
                        FROM Journal_expenses WHERE month = ? and year = ?""",
                    (month, year)).fetchall()
                for row in result:
                    add_row(row, self.expenses_table)

                # Загрузка регулярных доходов (всех)
                result = cursor.execute("""SELECT name, category, value, period
                                            FROM RegPayments_income""").fetchall()
                for row in result:
                    add_row(row, self.income_table)

                # Загрузка регулярных расходов (всех)
                result = cursor.execute("""SELECT name, category, value, period
                                            FROM RegPayments_spending""").fetchall()
                for row in result:
                    add_row(row, self.spending_table)

                # Пересчет итого
                self.calc_total()
                self.calc_reg_payments_total()

            except Exception as e:
                print(f"Ошибка при загрузке данных: {e}")
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные из базы данных")

    def save(self):
        """Сохранение данных в базу данных"""
        with sqlite3.connect("db/journalDatabase.db") as conn:
            cursor = conn.cursor()
            month, year = self.calendar.monthShown(), self.calendar.yearShown()

            try:
                # Сохранение доходов журнала
                cursor.execute("DELETE FROM Journal_gains WHERE month = ? and year = ?", (month, year))
                for r in range(self.gains_table.rowCount()):
                    vals = []
                    for c in range(self.gains_table.columnCount()):
                        item = self.gains_table.item(r, c)
                        vals.append(item.text() if item else "")

                    sql = """INSERT INTO Journal_gains (name, category, value, comment, month, year)
                             VALUES(?, ?, ?, ?, ?, ?)"""
                    cursor.execute(sql, tuple(vals + [str(month), str(year)]))

                # Сохранение расходов журнала
                cursor.execute("DELETE FROM Journal_expenses WHERE month = ? and year = ?", (month, year))
                for r in range(self.expenses_table.rowCount()):
                    vals = []
                    for c in range(self.expenses_table.columnCount()):
                        item = self.expenses_table.item(r, c)
                        vals.append(item.text() if item else "")

                    sql = """INSERT INTO Journal_expenses (name, category, value, comment, month, year)
                             VALUES(?, ?, ?, ?, ?, ?)"""
                    cursor.execute(sql, tuple(vals + [str(month), str(year)]))

                # Сохранение регулярных доходов
                cursor.execute("DELETE FROM RegPayments_income")
                for r in range(self.income_table.rowCount()):
                    vals = []
                    for c in range(self.income_table.columnCount()):
                        item = self.income_table.item(r, c)
                        vals.append(item.text() if item else "")

                    sql = """INSERT INTO RegPayments_income (name, category, value, period)
                             VALUES(?, ?, ?, ?)"""
                    cursor.execute(sql, tuple(vals))

                # Сохранение регулярных расходов
                cursor.execute("DELETE FROM RegPayments_spending")
                for r in range(self.spending_table.rowCount()):
                    vals = []
                    for c in range(self.spending_table.columnCount()):
                        item = self.spending_table.item(r, c)
                        vals.append(item.text() if item else "")

                    sql = """INSERT INTO RegPayments_spending (name, category, value, period)
                             VALUES(?, ?, ?, ?)"""
                    cursor.execute(sql, tuple(vals))

                conn.commit()
                QMessageBox.information(self, "Успех", "Данные успешно сохранены!")

            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить данные в базу данных")

    def calc_total(self):
        """Расчет общего баланса для выбранного месяца"""
        try:
            total = 0
            _, days_num = calendar.monthrange(self.calendar.yearShown(), self.calendar.monthShown())

            # Коэффициенты для пересчета регулярных платежей
            factors = {
                "День": lambda x: x * days_num,
                "Месяц": lambda x: x,
                "Год": lambda x: x / 12
            }

            # Учет расходов журнала
            for r in range(self.expenses_table.rowCount()):
                item = self.expenses_table.item(r, 2)
                if item and item.text().isdigit():
                    total -= int(item.text())

            # Учет доходов журнала
            for r in range(self.gains_table.rowCount()):
                item = self.gains_table.item(r, 2)
                if item and item.text().isdigit():
                    total += int(item.text())

            # Учет регулярных расходов
            for r in range(self.spending_table.rowCount()):
                value_item = self.spending_table.item(r, 2)
                period_item = self.spending_table.item(r, 3)

                if value_item and value_item.text().isdigit() and period_item:
                    value = int(value_item.text())
                    period = period_item.text()
                    if period in factors:
                        total -= factors[period](value)

            # Учет регулярных доходов
            for r in range(self.income_table.rowCount()):
                value_item = self.income_table.item(r, 2)
                period_item = self.income_table.item(r, 3)

                if value_item and value_item.text().isdigit() and period_item:
                    value = int(value_item.text())
                    period = period_item.text()
                    if period in factors:
                        total += factors[period](value)

            # Отображение результата с форматированием
            self.total.setText(f"{total:,.2f} ₽".replace(",", " "))

            # Цвет в зависимости от результата
            if total > 0:
                self.total.setStyleSheet("color: green;")
            elif total < 0:
                self.total.setStyleSheet("color: red;")
            else:
                self.total.setStyleSheet("color: blue;")

        except Exception as e:
            print(f"Ошибка при расчете итогов: {e}")
            self.total.setText("Ошибка расчета")

    def calc_reg_payments_total(self):
        """Расчет итогов только по регулярным платежам за выбранный месяц"""
        try:
            # Получаем количество дней в выбранном месяце
            _, days_num = calendar.monthrange(self.calendar.yearShown(), self.calendar.monthShown())

            # Коэффициенты для пересчета регулярных платежей
            factors = {
                "День": lambda x: x * days_num,
                "Месяц": lambda x: x,
                "Год": lambda x: x / 12
            }
            total_income = 0  # Общие регулярные доходы
            total_spending = 0  # Общие регулярные расходы

            # Расчет регулярных доходов
            for r in range(self.income_table.rowCount()):
                value_item = self.income_table.item(r, 2)
                period_item = self.income_table.item(r, 3)
                if value_item and value_item.text().isdigit() and period_item:
                    value = int(value_item.text())
                    period = period_item.text()
                    if period in factors:
                        total_income += factors[period](value)

            # Расчет регулярных расходов
            for r in range(self.spending_table.rowCount()):
                value_item = self.spending_table.item(r, 2)
                period_item = self.spending_table.item(r, 3)
                if value_item and value_item.text().isdigit() and period_item:
                    value = int(value_item.text())
                    period = period_item.text()
                    if period in factors:
                        total_spending += factors[period](value)

            # Чистый итог
            net_total = total_income - total_spending
            self.reg_total.setText(f"{net_total:,.2f} ₽".replace(",", " "))

            # Цвет в зависимости от результата
            if net_total > 0:
                self.reg_total.setStyleSheet("color: green;")
            elif net_total < 0:
                self.reg_total.setStyleSheet("color: red;")
            else:
                self.reg_total.setStyleSheet("color: blue;")

        except Exception as e:
            print(f"Ошибка при расчете регулярных платежей: {e}")
            self.reg_total.setText("Ошибка расчета")

    def add_spending(self):
        """Добавление регулярного расхода"""
        dialog = ToRegularPaymentsAddSpending(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            add_row(dialog.get_inputs(), self.spending_table)
            self.calc_total()
            self.calc_reg_payments_total()

    def add_income(self):
        """Добавление регулярного дохода"""
        dialog = ToRegularPaymentsAddIncome(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            add_row(dialog.get_inputs(), self.income_table)
            self.calc_total()
            self.calc_reg_payments_total()

    def add_expense(self):
        """Добавление расхода в журнал"""
        dialog = ToJournalAddExpense(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            add_row(dialog.get_inputs(), self.expenses_table)
            self.calc_total()

    def add_gain(self):
        """Добавление дохода в журнал"""
        dialog = ToJournalAddGain(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            add_row(dialog.get_inputs(), self.gains_table)
            self.calc_total()

    def del_expense(self):
        """Удаление расхода из журнала"""
        del_row(self.expenses_table)
        self.calc_total()

    def del_gain(self):
        """Удаление дохода из журнала"""
        del_row(self.gains_table)
        self.calc_total()

    def del_income(self):
        """Удаление регулярного дохода"""
        del_row(self.income_table)
        self.calc_total()

    def del_spending(self):
        """Удаление регулярного расхода"""
        del_row(self.spending_table)
        self.calc_total()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())