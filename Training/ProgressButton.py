from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFrame, QPushButton, QProgressBar


class ProgressButton(QProgressBar):
    
    def __init__(self, parent):
        
        super().__init__(parent = parent)

        self.btn = QPushButton(parent = parent)
        
        self.setFixedSize(250, 250)

class Home(QFrame):
    
    def __init__(self):
        
        super().__init__()
        
        self.btn = ProgressButton(parent = self)




if __name__ == "__main__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    home = Home()
    home.show()
    sys.exit(app.exec_())