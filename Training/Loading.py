from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi

from pyqtspinner.spinner import WaitingSpinner
import sys

class Loading(QFrame):
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        self.setFrameShape(QFrame.Panel)
        
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        
        testo = QLabel('Caricamento...')
        testo.setFont(font)
        layout.addWidget(testo, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        load = QLabel()
        load.setObjectName('labelLoading')
        
        l = QVBoxLayout()
        self.loading = WaitingSpinner(load, radius = 20, color = (255, 255, 255))
        l.addWidget(load)
        layout.addLayout(l)
        
        self.setLayout(layout)
        
    def start(self):
        
        self.loading.start()
        
        self.show()
        
    def stop(self):
        
        self.loading.stop()
        
        self.hide()


if __name__ == "__main__":
    
    import sys
    app = QApplication(sys.argv)
    home = Loading()
    home.start()
    sys.exit(app.exec_())