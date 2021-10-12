from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon


def creaAvviso(parent, messaggio: str, icona: QIcon, func):
    
    msg = QMessageBox(parent = parent)
            
    msg.setIcon(icona)
    
    msg.setText(messaggio)
    
    msg.buttonClicked.connect(func)

    msg.exec_()

def chiediEtichetta(parent):
    
    testo, okPremuto = QInputDialog.getText(parent, 'Input', 'Che elemento vuoi aggiungere?')
        
    return testo.strip() if okPremuto else None
    