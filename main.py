import random
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
