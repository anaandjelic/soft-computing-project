Enemy detection and aimbot for CS:GO
-------------
This project incorporates a version of [Ultralitic's YOLOv5s](https://github.com/ultralytics/yolov5) model for character detection and classification. It was trained on a custom dataset containing around 1000 labeled and unlabeled images. Images were processed mainly on [roboflow](https://roboflow.com/) with the help of [Scutti](https://github.com/TrevorSatori/Scutti) to collect data and [labelImg](https://github.com/heartexlabs/labelImg) to label the data.

Requirements
-------------
requirements.txt was generated from Anaconda environment.
Install the dependencies by running the following command:
```python
pip install -r requirements.txt
```
Enable CUDA to achieve higher FPS (increased from 2FPS to 20FPS on 640 image size).

How to run
-------------
aimbot.py takes two arguments: opponent and image size. Opponent can be terrorist or counter-terrorist, while image size can be 320, 640 or 1280.
Here's an example of how to run the script:
```python
python aimbot.py terrorist 640
```
