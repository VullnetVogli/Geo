import os
from imageai.Detection.Custom import DetectionModelTrainer
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = 'true'

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()

trainer.setDataDirectory(data_directory=r'D:\Cartelli\dare_precedenza_panoramiche')

metrics = trainer.evaluateModel(model_path= 'D:\Cartelli\dare_precedenza_panoramiche\models\detection_model-ex-001--loss-0020.089.h5', json_path=r"D:\Cartelli\dare_precedenza_panoramiche\json\detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)