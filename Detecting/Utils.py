from Detection import JSONNotValidException

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

import json
from json.decoder import JSONDecodeError

import os

def toJSON(file: str):
    
    if os.path.isdir(file):
    
        return os.path.join(file, os.path.basename(file) + '.json')
    
    file = file.split('.')
    
    file[-1] = '.json'
    
    return ''.join(file)

def toXLSX(file: str):
    
    if os.path.isdir(file):
    
        return os.path.join(file, os.path.basename(file) + '.xlsx')
    
    file = file.split('.')
    
    file[-1] = '.xlsx'
    
    return ''.join(file)

def creaAvviso(parent, messaggio: str, icona: QIcon, func):
    
    msg = QMessageBox(parent = parent)
            
    msg.setIcon(icona)
    
    msg.setText(messaggio)
    
    msg.buttonClicked.connect(func)

    msg.exec_()
    
def leggiJSON(path: str):
    
    with open(f'{path}/{os.path.basename(path)}.json', 'r') as f:
        
        try:
                
            return json.loads(f.read())
        
        except JSONDecodeError:
            
            raise JSONNotValidException(path = '') from None

def salvaSons(sons: dict, output: str):

    with open(output, 'w') as f:

        json.dump(sons, f, indent = 4)
        
def salvaSon(son: dict, output: str):

    with open(output, 'w') as f:

        json.dump(son, f, indent = 4)
    
def fileValido(file: str):
    
    return any(file.lower().endswith(estensione) for estensione in ('.jpg', '.png', '.tif', '.webp', '.ppm', '.pgm'))