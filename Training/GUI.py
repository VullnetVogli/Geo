from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFrame, QListWidgetItem

from TrainDetection import Train

from Utils import *
from Loading import Loading

import os

from Exceptions import *

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = 'true'
    
class Home(QFrame):

    # Costruttore
    def __init__(self):
        
        super().__init__()
        
        loadUi("guis//home.ui", self)

        self.running = False
        
        self.trainer = Train()

        self.loading = Loading()
        
        self.trainer.getLog().batch.connect(self._updateBatch)
        
        self.trainer.getLog().epoch.connect(self._updateEpoca)
        
        self.trainer.getLog().on_start.connect(self.__modificaStatoBottoni)
        
        self.trainer.getLog().info.connect(self._updateInfos)
        
        self.trainer.getLog().on_stop.connect(lambda: creaAvviso(parent = self, messaggio = 'Training terminato!', icona = QMessageBox.Information, func = lambda: None))

        self.__inizilizzaBottoni()
    
    # Inizializzazioni
    def __inizilizzaBottoni(self):
        
        self.btnStart.clicked.connect(self.start)
        
        self.btnCartellaModelli.clicked.connect(self.__apriCartellaModelli)
     
        self.epoche.valueChanged.connect(lambda: self.epocheTotali.setText(f'di {self.epoche.value()}') if not self.running else None)
     
        self.btnDataPath.clicked.connect(lambda: self.__selezionaModello())
        
        self.btnModelPath.clicked.connect(lambda: self.__selezionaCartella())
        
        self.btnAggiungi.clicked.connect(lambda: self.__aggiungi())
        
        self.btnRimuovi.clicked.connect(lambda: self.__rimuovi())
    
    def __modificaStatoBottoni(self, abilitato = True):
        
        for child in self.children():
            
            child.setEnabled(abilitato)
            
        # Se il menu è disattivato (quindi vogliamo riabilitarlo) vuol dire che la gif deve smettere di girare
        if abilitato:
            
            self.loading.stop()
        
    # Metodi
    def start(self):
        
        self.__modificaStatoBottoni(abilitato = False)
            
        if self.textDataDirectory.text() == '':
            
            creaAvviso(parent = self, messaggio = 'Selezionare la cartella prima!', icona = QMessageBox.Critical, func = lambda: None)
    
        elif not self.listObjs.count():
            
            creaAvviso(parent = self, messaggio = 'Inserisci gli elementi prima!', icona = QMessageBox.Information, func = lambda: None)
    
        else:
        
            self.progressBarEpoche.setRange(0, self.epoche.value())
            
            self.progressBarEpoche.setValue(0)
            
            self.progressBarBatch.setRange(0, self.batchSize.value())
            
            self.progressBarBatch.setValue(0)
            
            self.labelLoss.setText('...')
            
            self.labelLossLayer1.setText('...')
            
            self.labelLossLayer2.setText('...')
            
            self.labelLossLayer3.setText('...')
            
            self.loading.start()
            
            self.__run()
        
    def __run(self):
        
        elementi = [self.listObjs.item(i).text() for i in range(self.listObjs.count())]
        
        try:
            
            self.trainer.setDataDirectory(self.textDataDirectory.text())
            
            self.trainer.setTrainConfig(oggetti = elementi, batch_size = self.batchSize.value(), num_experiments = self.epoche.value() - 3, train_from_pretrained_model = self.textPretrainedModel.text())

            self.trainer.start()
            
        except EtichetteNonValideException as e:
            
            self.loading.stop()
            
            creaAvviso(parent = self, messaggio = e.testo, icona = QMessageBox.Information, func = lambda: None)
            
        
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
    
    def _updateInfos(self, logs):
        
        self.epocheTotali.setText('di ' + str(logs['epochs']))
        
        self.progressBarEpoche.setRange(0, logs['epochs'])
        
        self.batchTotali.setText('di ' + str(logs['steps']))
        
        self.progressBarBatch.setRange(0, logs['steps'])
    
    def _updateEpoca(self, logs):
        
        self.labelEpoca.setText(str(logs['epoch']))
        
        self.progressBarEpoche.setValue(logs['epoch'])
        
    def _updateBatch(self, logs):
        
        logs['batch'] += 1
        
        self.labelBatch.setText(str(logs['batch']))
    
        self.progressBarBatch.setValue(logs['batch'])
        
        self.labelLoss.setText(str(logs['loss']))
        
        self.labelLossLayer1.setText(str(logs['yolo_layer_1_loss']))
        
        self.labelLossLayer2.setText(str(logs['yolo_layer_2_loss']))
        
        self.labelLossLayer3.setText(str(logs['yolo_layer_3_loss']))
    
    # File/Folder Dialogs
    def __openFolder(self, caption, textField):
        
        fileName = QFileDialog.getExistingDirectory(self, caption = caption, directory = textField.text())
        
        if fileName:
            
            textField.setText(fileName)

    def __openFileNameDialog(self, caption, files, textField):
        
        fileName, _ = QFileDialog.getOpenFileName(self, caption = caption, directory = textField.text(), filter = files)
        
        if fileName:
            
            textField.setText(fileName)
            
    def closeEvent(self, event):
        
        self.loading.stop()
        
        self.loading.destroy()
            
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
    # app.setPalette(palette)

    home = Home()
    home.show()
    sys.exit(app.exec_())