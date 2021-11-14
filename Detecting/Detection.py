from imageai.Detection.Custom import CustomObjectDetection

import os

class FileNotValidException(Exception):
    
    def __init__(self, path):
        
        self.path = path
        
    def __str__(self):
        
        return f'"{self.path}" not valid'

class ModelNotValidException(FileNotValidException):
    
    def __init__(self, path):
        
        super().__init__(path)

class JSONNotValidException(FileNotValidException):
    
    def __init__(self, path):
        
        super().__init__(path)

class Detector():

    os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

    PERCENTUALE_MINIMA = 50

    def __init__(self):
        
        self.detector = CustomObjectDetection()
        
        self.detector.setModelTypeAsYOLOv3()

    def setModelPath(self, modelPath):
        
        self.detector.setModelPath(modelPath)
        
    def setJsonPath(self, jsonPath):
        
        self.detector.setJsonPath(jsonPath)
     
    def getModelPath(self):
        
        return self.detector.getModelPath()
    
    def getJsonPath(self):
        
        return self.detector.getJsonPath()
        
    def loadModel(self):
             
        try:
        
            self.detector.loadModel()
            
        except (FileNotFoundError, KeyError) as e:
            
            raise JSONNotValidException(self.detector.getJsonPath()) from None
            
        except ValueError as e:
            
            raise ModelNotValidException(self.detector.getModelPath()) from None
        
    def same_model(self, model):
        
        return self.detector.getModelPath() == model
                
    def detect(self, image: str, output_image: str):
        
        return self.detector.detectObjectsFromImage(input_image = image, output_image_path = output_image, minimum_percentage_probability = self.PERCENTUALE_MINIMA)
    