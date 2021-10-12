import json
import os

from datetime import datetime

class JLogs():
    
    def __init__(self):
        
        self.logs = {}
    
    def salva(self, detections: list, file: str, output: str) -> None:
        
        try:
            
            son = {'path': os.path.dirname(os.path.dirname(file)), 
                   'run': os.path.basename(os.path.dirname(file)),
                   'filename': os.path.basename(file),
                   'objects': []}
            
            [son['objects'].append(detection) for detection in detections]
            
            # Assegnamo al json con tutti i log dei cartelli quest'ultimo analizzato
            self.logs[file] = son
            
            with open(output, 'w') as f:
                
                json.dump(son, f, indent = 4)
                
        except Exception as e:

            print(e)

    def salvaLog(self, output: str, nomeModello: str, percentuale: int):
        
        self.logs['nomeModello'] = nomeModello
        
        self.logs['percentuale'] = percentuale
        
        self.logs['timestamp'] = datetime.timestamp(datetime.now())
        
        with open(output, 'w') as f:

            json.dump(self.logs, f, indent = 4)
        
