import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO
 
if __name__ == '__main__':
    model = YOLO('/home/ljr/Project/yolov10/ultralytics/cfg/models/v10/yolov10s.yaml') # 地址改成自己的
    model.train(data='/home/ljr/Project/UI.yaml',
                cache=False,
                imgsz=640,
                epochs=100,
                single_cls=False,  # 是否是单类别检测
                batch=8,
                close_mosaic=10,
                workers=0,
                device='0',
                optimizer='SGD',
                amp=True,
                project='runs/train',
                name='exp',
                )
