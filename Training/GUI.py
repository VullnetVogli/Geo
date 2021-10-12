from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QColor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFrame, QListWidgetItem

from TrainDetection import Train

from Utils import *

import logging, os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = 'true'

class Home(QFrame):

    # Costruttore
    def __init__(self):
        
        super(Home, self).__init__()
        
        loadUi("guis//home.ui", self)
        
        self.running = False
        
        self.trainer = Train()
        
        self.__inizilizzaBottoni()
    
    # Inizializzazioni
    def __inizilizzaBottoni(self):
        
        self.btnStart.clicked.connect(self.start)
        
        self.btnCartellaModelli.clicked.connect(self.__apriCartellaModelli)
     
        self.epoche.valueChanged.connect(lambda: self.boxProgress.setTitle(f'0 di {self.epoche.value()}'))
     
        self.btnDataPath.clicked.connect(lambda: self.__selezionaModello())
        
        self.btnModelPath.clicked.connect(lambda: self.__selezionaCartella())
        
        self.btnAggiungi.clicked.connect(lambda: self.__aggiungi())
        
        self.btnRimuovi.clicked.connect(lambda: self.__rimuovi())
    
    def __inizializzaProgressBar(self):
    
        self.progressBarEpoche.reset()
        
        self.progressBarEpoche.setRange(0, self.epoche.value() + 3)
    
        self.progressBarEpoche.setValue(0)

    # Metodi
    def start(self):
        
        # if self.textDataDirectory.text() == '':
            
        #     creaAvviso(parent = self, messaggio = 'Selezionare la cartella prima!', icona = QMessageBox.Critical, func = lambda: None)
    
        # elif not self.listObjs.count():
            
        #     creaAvviso(parent = self, messaggio = 'Inserisci gli elementi prima!', icona = QMessageBox.Information, func = lambda: None)
    
        # else:
    
        self.__run()
        
    def __run(self):
        
        elementi = [self.listObjs.item(i).text() for i in range(self.listObjs.count())]
        
        self.trainer.setDataDirectory(self.textDataDirectory.text())
        
        self.trainer.setTrainConfig(oggetti = elementi, batch_size = self.batchSize.value(), num_experiments = self.epoche.value(), train_from_pretrained_model = self.textPretrainedModel.text())
        
        self.__inizializzaProgressBar()
        
        self.trainer.setObjs({'batch': {
                                        'label': self.labelBatch,
                                        'progressBar': self.progressBarBatch,
                                        'total': self.batchTotali
                                        },
                              'loss': {
                                        'total': self.labelLoss,
                                        'layer1': self.labelLossLayer1,
                                        'layer2': self.labelLossLayer2,
                                        'layer3': self.labelLossLayer3
                                      },
                              'epoca': {
                                  'label': self.labelEpoca,
                                  'progressBar': self.progressBarEpoche,
                                  'total': self.epocheTotali
                              }})
        
        self.trainer.start()
        
    def __apriCartellaModelli(self):
        
        try:
            
            os.startfile(os.path.join(self.textDataDirectory.text(), 'models'))
            
        except FileNotFoundError:
            
            creaAvviso(parent = self, messaggio = 'Seleziona una cartella prima!', icona = QMessageBox.Information, func = lambda: None)
        
    def __aggiungi(self):
        
        testo = chiediEtichetta(parent = self)
        
        if testo:
        
            a = QListWidgetItem(testo)
            
            a.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            
            self.listObjs.addItem(a)

    def __rimuovi(self):
        
        if self.listObjs.count():
            
            self.listObjs.takeItem(self.listObjs.currentRow())
    
    def __selezionaModello(self):
        
        self.__openFileNameDialog(caption = 'Seleziona modello', files = "H5 Files (*.h5)", textField = self.textPretrainedModel)
    
    def __selezionaCartella(self):
        
        self.__openFolder(caption = 'Seleziona la cartella con le immagini', textField = self.textDataDirectory)
        
        self.trainer.setDataDirectory(path = self.textDataDirectory.text())
    
    # File/Folder Dialogs
    def __openFolder(self, caption, textField):
        
        fileName = QFileDialog.getExistingDirectory(self, caption = caption, directory = textField.text())
        
        if fileName:
            
            textField.setText(fileName)

    def __openFileNameDialog(self, caption, files, textField):
        
        fileName, _ = QFileDialog.getOpenFileName(self, caption = caption, directory = textField.text(), filter = files)
        
        if fileName:
            
            textField.setText(fileName)
            
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