from imageai.Detection.Custom import CustomObjectDetection
from pathlib import Path
import os

from datetime import datetime

from colorama import init
from termcolor import colored

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfile

'''

Autore: Vogli Vullnet
Consegna: Automatizzazione processo di detection ImageAI

Note versioni e oggetti utilizzati:
- colorama             0.4.3
- h5py                 2.10.0
- imageai              2.1.5
- Keras                2.1.6
- numpy                1.19.0
- opencv-python        4.2.0.34
- PyQt5                5.15.0
- termcolor            1.1.0
ciao
'''

def file_immagine_valido(file_immagine: Path):

    for estensione in estensioni_supportate:

        if file_immagine.name.lower().endswith(estensione):

            return True
 
    return False

def crea_percorsi(cartella: Path):

    if not cartella.exists():

        cartella.mkdir()

def crea_file_di_testo(path: Path, nome_immagine: str):
    
    # Ritorniamo la path del file.txt sulla cartella path_salvataggi
    return Path(os.path.join(path, nome_immagine.split('.')[0] + '.txt'))

def scrivi_su_file_di_testo(file_testo: Path, detections: list):

    try:

        with open(file_testo, 'w+') as f:

            informazioni = datetime.today()

            f.write('Scansione in data: %s, alle ore: %s\n\n' % (str(informazioni.strftime('%y-%m-%d')), str(informazioni.today().strftime('%H.%M.%S'))))

            if len(detections) == 0:

                f.write('Nessun oggetto rilevato!')

            else:

                for detection in detections:
                    
                    f.write("-> %10s %10s %50s\n" % (detection['name'], detection['percentage_probability'], detection['box_points']))

                f.write('\n\n\n')

        print(colored('Dati salvati! :)', 'green'))

    except Exception as e:

        print(colored(e, 'red'))

def calcola_immagine(immagine: Path, output_path: str):

    return detector.detectObjectsFromImage(input_image = str(immagine.absolute()), output_image_path = os.path.join(output_path, immagine.name), minimum_percentage_probability = PERCENTUALE_MINIMA)

def esplora_cartelle(path: Path):

    # Scorro le cartelle nella path
    for file_immagine in path.iterdir():

        # Se viene trovata una cartella utilizzo la ricorsività per esplorare quest'ultima.
        if file_immagine.is_dir():
            
            esplora_cartelle(file_immagine)

        # Altrimenti se trovo un file che rispetti le estensioni dettate dalla API ImageAI eseguo tutti i calcoli.
        elif file_immagine_valido(file_immagine):
            
            output_path_file = Path(str(file_immagine.parent).replace(str(path_iniziale), str(path_salvataggi)))

            # Path cartella 'Risultati'
            crea_percorsi(output_path_file)        
            
            # I calcoli vengono effettuati in un blocco try -> expect dato che qualche file potrebbe avere permessi non accessibili senza essere amministratore.
            try:

                print(colored('Lavorando sulla immagine -> "%s" -> ' % (file_immagine.absolute()), 'green'), end = '')

                # Creo il file nome_foto.txt in base alla cartella path_salvataggi in cui scriverò le informazioni ricavate dalla detection.
                scrivi_su_file_di_testo(crea_file_di_testo(output_path_file, file_immagine.name), calcola_immagine(immagine = file_immagine, output_path = str(output_path_file)))
                
            except Exception as e:
            
                print(colored(e), 'red')

        # Altrimenti il file è di un'altra estensione non adatta.
        else:

            print(colored('Il file_immagine %s non è valido! Proseguo...' % (file_immagine.absolute()), 'red'))

# Prese dalla documentazione
estensioni_supportate = ('.jpg', '.png', '.tif', '.webp', '.ppm', '.pgm')

PERCENTUALE_MINIMA = 90

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"]= "true"

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("D:\Programmazione\Python\Stage_MachineLearning\Segnali\models\detection_model-ex-046--loss-0004.598.h5")
detector.setJsonPath("D:\Programmazione\Python\Stage_MachineLearning\Segnali\json\detection_config.json")
detector.loadModel()

#path_iniziale = Path(r'D:\Programmazione\Python\Stage_MachineLearning\Test\Immagini\FOTO_PANORAMICHE\119')
path_iniziale = Path(askdirectory())

#path_salvataggi = Path(r'D:\Programmazione\Python\Stage_MachineLearning\Test\Risultati')
path_salvataggi = Path(askdirectory())

path_salvataggi = Path(os.path.join(path_salvataggi, datetime.today().strftime('Esecuzione_%H.%M.%S_%y-%m-%d')))

path_salvataggi.mkdir()

esplora_cartelle(path_iniziale)

print(colored('\nTutte le informazioni riguardanti queste operazioni sono state salvate nella cartella: "%s".\n' % (path_salvataggi), 'yellow'))

os.startfile(path_salvataggi)