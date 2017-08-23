# Snapchat-like filters with Python OpenCV/dlib and TKinter
Basic desktop application to play around with Snapchat-alike filters like hat, moustache and glasses automatic in-face superposition in real time.

![alt text][s1] ![alt text][s11]


It uses [Haar features](https://en.wikipedia.org/wiki/Haar-like_features) and the [Viola–Jones object detection framework
](https://en.wikipedia.org/wiki/Viola%E2%80%93Jones_object_detection_framework) implemented in OpenCV to detect mainly faces positions and inside the faces, eyes and mouth position. It uses then this information to add different accessories to the faces (hat, moustache, etc).

The files containing the Haar Filters descriptions were taken from http://alereimondo.no-ip.org/OpenCV/34 and ftp://mozart.dis.ulpgc.es/pub/Software/HaarClassifiers/FaceFeaturesDetectors.zip.

The Dlib implementation of this app uses a [Histogram of Oriented Gradients (HOG)](https://en.wikipedia.org/wiki/Histogram_of_oriented_gradients) feature combined with a linear classifier, an image pyramid, and sliding window detection scheme to detect faces. Then it finds the 68 facial landmarks using an Ensemble of Regression Trees described in the paper [One Millisecond Face Alignment with an Ensemble of Regression Trees](https://pdfs.semanticscholar.org/d78b/6a5b0dcaa81b1faea5fb0000045a62513567.pdf).


## Requirements
* OpenCV 3.0+ with python bindings
* Python 2.7
     * pillow
     * numpy
     * tkinter
* Python bindings of dlib.


#### Easy install
Build `OpenCV` or install the light version with `sudo apt-get install libopencv-dev python-opencv`. For Windows users it is always easier to just download the binaries of OpenCV and execute them, see [this web page](http://docs.opencv.org/trunk/d5/de5/tutorial_py_setup_in_windows.html). For `TKinter` in Linux just execute: `apt-get install python-tk` (python binaries in windows usually have Tkinter already installed).

For python dependences just execute:

```
pip install -r requirements.txt
```

***Dlib installation***: For Windows Users it can be very hard to compile dlib with python bindings, just follow this simple [instruction on how to install dlib in windows the easy way](https://github.com/charlielito/install-dlib-python-windows).

For Linux Users make sure you have the prerequisites:
```
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```
Finally just `pip install it` with: `pip install dlib`


### How it works
#### HaarClassifiers
The algorithm give us the rectangles where faces might be as it can be seen in the next picture. After that, specialized HaarClassifiers are used to find mouths, noses, and eyes inside the image recognized as a face. With that information it is relatively easy to put the different "gadgets" in superposition with the image. We just use the alpha channel (transparency) of the "accessories" to merge the images.

![alt text][s4]

To recreate this in real time with your WebCam just execute

```
python facial_features.py
```


#### Dlib face and landmarks detection
HarrCascades technique is very old, so detection is often not so good when the faces are slightly bent for example. It is not possible to estimate the inclination of the head for example. Detection of face characteristics (eyes, nose, mouth, eyebrows, etc) is also not robust with HaarClassifiers. Here comes into play more recent techniques implemented in the dlib library. If you compare the to detection schemes the dlib is more accurate and stable. As described, we can also get the main facial landmarks which are used to detect the face characteristics and to estimate the tilt angle of the face. That can be seen in the next picture.

![alt text][s5]

The 68 facial landmarks are numbered in the following form. With tha points we calculate the inclination so the "accessories" are also bent. Wth the points of the mouth can be detected when the mouth is open and then display some trick, like a rainbow coming out.

![alt text][s6]

To recreate this in real time with your WebCam just execute

```
python facial_landmarks.py
```

## Running the code with opencv or dlib
In Windows just double click de file `main.py` or execute in the console the following to run the HaarCascade version app (opencv)

```
python main.py
```

To use the dlib version with more interesting features run
```
python main_dlib.py
```


## Comparison between OpenCv HaarCascade Classifiers and Dlib algorithms
Here can be compared the performance in real time of the two techniques. As seen the opencv with HaarCascade  implementation is not so "stable" (i.e the hat moves a lot although the face is still). Also with the dlib version more fun things can be made and the accessories inclines with us.

### OpenCV
![alt text][s3]
### Dlib
![alt text][s2]


[s1]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/opencv.gif "S"
[s11]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/dlib.gif "S"

[s2]: https://raw.githubusercontent.com/charlielito/mydata/master/dlibvideo.gif "S"

[s3]: https://raw.githubusercontent.com/charlielito/mydata/master/opencvvideo.gif "S"

[s4]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/features.png "S"
[s5]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/landmarks.png "S"

[s6]: https://raw.githubusercontent.com/charlielito/snapchat-filters-opencv/master/imgs/facial_landmarks_68markup.jpg "S"
