import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap


class BreakRecord(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Break_record\break_record.ui', self)
        self.for_cup.setPixmap(QPixmap(r'Break_record\cup_win.png'))
        self.pushButton.clicked.connect(self.close)

# app = QApplication(sys.argv)
# win = BreakRecord()
# win.show()
# sys.exit(app.exec())