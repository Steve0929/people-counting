<img src="https://img.shields.io/badge/on-development-red.svg">

# people-counting
Track and count people walking using computer vision


### Requirements
* Python 2.7
* OpenCV 2.4.8


### Tech
* [OpenCV] - Open Source Computer Vision Library.
* [numpy] - Package for scientific computing with Python.
 
### Installation and usage
```sh
$ pip install opencv 
$ pip install numpy
$ python hellow.py
```
Passing '0' to cv2.VideoCapture will use the default camera of your computer, however you may pass the path of a video file saved on your computer or a RTSP (Real Time Streaming Protocol) URL.

```sh
cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("video.avi")
cap = cv2.VideoCapture("rtsp://YourRTSPUrl")
```
[OpenCV]: <https://opencv.org/>
[numpy]: <http://www.numpy.org/>
