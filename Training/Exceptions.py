
class EtichetteNonValideException(Exception):
    
    testo = 'Le etichette inserite non coincidono con quelle nel JSON!'
        
    def __str__(self):
        
        return self.testo
    
class CartellaAnnotationsNonValidaException(Exception):
    
    testo = 'La cartella "annotations" non è valida!'
        
    def __str__(self):
        
        return self.testo

class CartellaImagesNonValidaException(Exception):
    
    testo = 'La cartella "images" non è valida!'
        
    def __str__(self):
        
        return self.testo