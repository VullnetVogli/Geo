from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect

from typing import List

import math

class Immagine(QLabel):
    
    # Costruttore
    def __init__(self, img):
        
        self.img = img
        
        self.item = None
        
    # Set && Get
    def setItem(self, item):
        
        if item is not None: self.item = item
        
    def getItem(self):
        
        return self.item
    
    """Metodo per caricare l'immagine"""
    def load(self):

        self.img.setPixmap(QPixmap(self.item.text()))
    
    """Metodo per cropppare l'immagine"""
    def crop(self, x: int, y: int, w: int, h: int):
        
        return QPixmap(self.item.text()).copy(QRect(x, y, w - x, h - y))
        
    
class Crop(Immagine):
    
    def __init__(self, img: Immagine, points: List[int]):
        
        super().__init__(img = img)
        
        self.points = points

    def getPoints(self):
        
        return self.points

    def load(self):
        
        self.img.setPixmap(super().crop(*self.points).scaled(250, 250))
        
        # self.percentage.setText(str(percentage))
        
        # self.labelX.setText(str(box_points[0]))
        
        # self.labelY.setText(str(box_points[1]))
        
        # self.labelWidth.setText(str(box_points[2]))
        
        # self.labelHeight.setText(str(box_points[3]))

                
class Crops():
    
    """Parameters: imgs: lista di Crop"""
    def __init__(self, imgs: List[Crop], gridLayout):
        
        self.index = -1
        
        self.img = imgs
        
        self.gridLayout = gridLayout
     
    """Metodo che inserisce tutti i crop in un gridLayout"""   
    def cambiaCrop(self):
        
        self.clearCrops()

        # Quanti riquadri devo creare per il gridLayout in base agli elementi che ho. Calcolo: Radice (perfetta) di len(oggetti). Quindi 2x2 per 3/4 elemnti, 3x3 per 5 < elemnti < 10, ecc...
        n = math.floor(math.sqrt(len(self.imgs))) + 1 if len(self.imgs) > 2 else len(self.imgs)
        index = 0
        
        for i in range(n):
            
            for j in range(n):
                
                try:
                
                    x, y, x1, y1 = self.imgs[self.index]['box_points']
                    
                    label = QLabel(self)
                    
                    label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                    
                    label.setAlignment(Qt.AlignCenter)
                    
                    label.setMaximumSize(250 / n + 10, 250 / n + 10)
                    
                    img = QPixmap(self.imgs[self.index].getItem().text()).copy(QRect(x, y, x1 - x, y1 - y))
                    
                    label.setPixmap(img)
                    
                    self.gridLayout.addWidget(label, i, j)
                    
                    index += 1
                    
                except IndexError as ex:
                    
                    return 
    
    """
    Metodo che cancella i crop presenti per aggiornarli
    """
    def clearCrops(self):
            
        while self.gridLayout.count():
            
            self.gridLayout.takeAt(0).widget().deleteLater()
        