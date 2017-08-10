# Snapchat-alike filters with Python OpenCV and TKinter
Basic desktop application to play around with Snapchat-alike filters like hat, moustache and glasses automatic in-face superposition.

![alt text][s1]

It uses [Haar features](https://en.wikipedia.org/wiki/Haar-like_features) and the [Viola–Jones object detection framework
](https://en.wikipedia.org/wiki/Viola%E2%80%93Jones_object_detection_framework) implemented in OpenCV to detect mainly faces positions and inside the faces, eyes and mouth position. It uses then this information to add different accesories to the faces (hat, moustache, etc).

The files containing the Haar Filters descriptions were taken from http://alereimondo.no-ip.org/OpenCV/34 and ftp://mozart.dis.ulpgc.es/pub/Software/HaarClassifiers/FaceFeaturesDetectors.zip.

## Requirements
* OpenCV 3.0+ with python bindings
* Python 2.7
     * pillow
     * tkinter

#### Easy install
Build `OpenCV` or install the light version with `pip install python-opencv`. For Windows users it is always easier to just download the binaries of OpenCV and execute them, see [this web page](http://docs.opencv.org/trunk/d5/de5/tutorial_py_setup_in_windows.html). For `TKinter` in Linux just execute: `apt-get install python-tk` (python binaries in windows usually have Tkinter already installed).
For python dependences just execute
```
pip install -r requirements.txt
```


## Running the code
In Windows just double click de file `main.py` or execute in the console the following:

```
python main.py
```

[s1]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/example.png "S"
