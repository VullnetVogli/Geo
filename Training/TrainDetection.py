from imageai.Detection.Custom import DetectionModelTrainer
import os

from PyQt5.QtCore import QThread

from Exceptions import *

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = 'true'

class Train(QThread):
    
    def __init__(self):
        
        super(Train, self).__init__()
        
        self.trainer = DetectionModelTrainer()
        
        self.trainer.setModelTypeAsYOLOv3()
                
    def setDataDirectory(self, path: str):
        
        self.trainer.setDataDirectory(data_directory = path)
        
    def setTrainConfig(self, oggetti, batch_size = 2, num_experiments = 1, train_from_pretrained_model = ''):
            
        self.trainer.setTrainConfig(object_names_array = oggetti, batch_size = batch_size, num_experiments = num_experiments, train_from_pretrained_model = train_from_pretrained_model)
        
    def start(self):
        
        super().start()
            
    def run(self):
        
        self.trainer.trainModel()
        
    def getLog(self):
        
        return self.trainer.getLog()

