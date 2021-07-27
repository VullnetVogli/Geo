from imageai.Detection.Custom import DetectionModelTrainer
import os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "lel"


a = ['F026-096 DOPPIO SENSO DI CIRCOLAZIONE', 'F079A120 SOSTA CONSENTITA A PARTICOLARI CATEGORIE', 'F036-106 DARE PRECEDENZA', 'F076-120 PARCHEGGIO', 'F047-116 SENSO VIETATO', 'F080B122 DIREZIONE OBBLIGATORIA A SINISTRA', 'F037-107 FERMARSI E DARE PRECEDENZA',
   'F291-133 SEGNALE NOME STRADA APPLICATO IN ANGOLO', 'F074-120 DIVIETO DI SOSTA', 'F080C122 DIREZIONE OBBLIGATORIA A DESTRA', 'F082B122 PASSAGGIO OBBLIGATORIO A DESTRA', 'F084-122 ROTATORIA', 'F309-135 STRADA SENZA USCITA', 'F348-135 SENSO UNICO PARALLELO', 'F303-135 ATTRAVERSAMENTO PEDONALE']

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory=r"D:\Programmazione\Python\Stage_MachineLearning\Segnali")
trainer.setTrainConfig(object_names_array=a, batch_size=4, num_experiments=100, train_from_pretrained_model='D:\Programmazione\Python\Stage_MachineLearning\Segnali\models\detection_model-ex-046--loss-0004.598.h5')
trainer.trainModel()
