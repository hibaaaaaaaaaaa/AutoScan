from PySide6.QtWidgets import QApplication,QMainWindow
from PySide6.QtGui import QPixmap,QIcon
from home import Home
import sys


class Connexion(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.central_widget = Home(self)
        self.setFixedSize(1200, 600)
        self.setWindowIcon(QIcon(QPixmap("packages/icons/icon_logo.svg")))
        self.setframe(self.central_widget)
        self.setStyleSheet("background: rgba(1, 1, 1, 1);")

        
    def setframe(self, fen):
        self.setCentralWidget(fen)
        
    def set_win_title(self,title):
        self.setWindowTitle(title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Connexion()
    window.show()
    sys.exit(app.exec())

