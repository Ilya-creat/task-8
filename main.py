import random
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog


class Dialog(QDialog):
    def __init__(self, tableWidget):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.tableWidget.setRowCount(tableWidget.rowCount())
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setColumnWidth(4, 550)
        for i in range(tableWidget.rowCount()):
            for j in range(tableWidget.columnCount()):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(tableWidget.item(i, j).text())))
                self.tableWidget.resizeRowsToContents()
        self.pushButton.clicked.connect(lambda: self.new_row(tableWidget))

    def new_row(self, tableWidget):
        def new_row(self, tableWidget):
            try:
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                cur.execute("""
                            INSERT INTO coffee VALUES (NULL, 'New coffee', '', '', '', -1, -1)
                            """)
                con.commit()
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                ans = cur.execute("""
                SELECT * FROM coffee
                """).fetchall()
                self.tableWidget.setRowCount(len(ans))
                self.tableWidget.resizeColumnsToContents()
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(ans[i][j])))
                        self.tableWidget.resizeRowsToContents()
            except Exception as e:
                print(e)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        ans = cur.execute("""
        SELECT * FROM coffee
        """).fetchall()
        self.tableWidget.setRowCount(len(ans))
        self.tableWidget.resizeColumnsToContents()
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(ans[i][j])))
                self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnWidth(4, 550)
        self.pushButton.clicked.connect(self.dialog)

    def dialog(self):
        try:
            dialog = Dialog(self.tableWidget)
            ans = dialog.exec()
            if ans == QDialog.Accepted:
                self.tableWidget.setRowCount(dialog.tableWidget.rowCount())
                self.tableWidget.resizeColumnsToContents()
                for i in range(dialog.tableWidget.rowCount()):
                    for j in range(dialog.tableWidget.columnCount()):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(dialog.tableWidget.item(i, j).text())))
                for i in range(self.tableWidget.rowCount()):
                    con = sqlite3.connect('coffee.sqlite')
                    cur = con.cursor()
                    cur.execute("""
                    UPDATE coffee SET name = ?, stand = ?, type = ?, about = ?, price = ?, v = ? WHERE id = ?
                    """, (self.tableWidget.item(i, 1).text(), self.tableWidget.item(i, 2).text(),
                          self.tableWidget.item(i, 3).text(), self.tableWidget.item(i, 4).text(),
                          self.tableWidget.item(i, 5).text(), self.tableWidget.item(i, 6).text(),
                          self.tableWidget.item(i, 0).text()))
                    con.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
