# Requirements:
# pip install tk
# pip install pillow

from Tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import threading
from threading import Thread
from os import listdir
from os.path import isfile, join

### Function to set wich sprite must be drawn
def put_hat():
        global SPRITES
        SPRITES[0] = (1 - SPRITES[0]) #not actual value

def put_mustache():
        global SPRITES
        SPRITES[1] = (1 - SPRITES[1]) #not actual value

def puy_flies():
        global SPRITES
        SPRITES[2] = (1 - SPRITES[2]) #not actual value

def put_glasses():
        global SPRITES
        SPRITES[3] = (1 - SPRITES[3]) #not actual value

#Draws sprite over a image
#It uses the alpha chanel to see which pixels need to be reeplaced
# Input: image, sprite: numpy arrays
#
def draw_sprite(frame, sprite, x_offset, y_offset):
        (M,N) = (sprite.shape[0], sprite.shape[1])
        #for each RGB chanel
        for c in range(3):
                #chanel 4 is alpha: 255 is not transpartne, 0 is transparent background
                frame[y_offset:y_offset+M, x_offset:x_offset+N, c] =  \
                sprite[:,:,c] * (sprite[:,:,3]/255.0) +  frame[y_offset:y_offset+M, x_offset:x_offset+N, c] * (1.0 - sprite[:,:,3]/255.0)
        return frame

# Returns the rectangles
def detectar_caras(img,faceCascade,scaleFact):
    #Img es una imagen a color
    #faceCascade es un clasificador tipo cascada cv2.CascadeClassifier
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=scaleFact,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

# Returns the rectangles
# Img is a rgb image
# path_filter is the path to the haar .xml file
# the other inputs are the filter parameters
def apply_Haar_filter(img, path_filter,scaleFact = 1.1, minNeigh = 5, minSizeW = 30):
    haar_cascade = cv2.CascadeClassifier(path_filter)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    feature = haar_cascade .detectMultiScale(
        gray,
        scaleFactor=scaleFact,
        minNeighbors=minNeigh,
        minSize=(minSize, minSize),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return features


#Adjust the given sprite to the head's width and position
#in case of the sprite not fitting the screen in the top, the sprite should be trimed
def adjust_sprite2head(sprite, head_width, head_ypos):
        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
        factor = 1.0*head_width/w_sprite
        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor) # adjust to have the same width as head
        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
        y_orig =  head_ypos-h_sprite # adjust the position of sprite to end where the head begins
        if (y_orig < 0): #check if the head is not to close to the top of the image and the sprite would not fit in the screen
                sprite = sprite[abs(y_orig)::,:,:] #in that case, we cut the sprite
                y_orig = 0 #the sprite then begins at the top of the image
        return (sprite, y_orig)

#Loop pricipal donde se manejan los accesorios y funciones openCV
def cvloop(run_event):
        global panelA
        global SPRITES


        faceCascade = cv2.CascadeClassifier("./filters/haarcascade_frontalface_default.xml")

        dir_ = "./sprites/flyes/"
        flies = [f for f in listdir(dir_) if isfile(join(dir_, f))] #image of flies to make the "animation"
        i = 0
        video_capture = cv2.VideoCapture(0) #read from webcam
        (x,y,w,h) = (0,0,10,10)
        while run_event.is_set(): #while the thread is active we loop
                ret, image = video_capture.read()

                faces = detectar_caras(image,faceCascade,1.3)
                if (len(faces) != 0 ): #if there are faces
                        #take first face found
                        (x,y,w,h) = (faces[0,0],faces[0,1],faces[0,2],faces[0,3])
                #hat condition
                if SPRITES[0]:
                        sprite = cv2.imread("./sprites/hat.png",-1)

                        (sprite, y_final) = adjust_sprite2head(sprite, w, y)

                        image = draw_sprite(image,sprite,x, y_final)
                #mustache condition
                if SPRITES[1]:
                        sprite = cv2.imread("./sprites/mustache.png",-1)

                        ypos = y + 2*h/3 #empiricamente el bigote esta a un 2/3 de la cara (desde el pelo)
                        xpos = x + w/4 #empiricamente el ancho del bigote es la mitad
                        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
                        factor = 1.0*(w/2)/w_sprite
                        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)

                        image = draw_sprite(image,sprite,xpos,ypos)
                #flies condition
                if SPRITES[2]:
                        #to make the "animation" we read each time a different image of that folder
                        # the images are placed in the correct order to give the animation impresion
                        sprite = cv2.imread(dir_+flies[i],-1)

                        (sprite, y_final) = adjust_sprite2head(sprite, w, y)

                        image = draw_sprite(image,sprite,x,y_final)
                        i+=1
                        i = 0 if i >= len(flies) else i #when done with all images of that folder, begin again

                #glasses condition
                if SPRITES[3]:
                        sprite = cv2.imread("./sprites/glasses.png",-1)

                        ypos = y + h/3 #empiricamente los ojos estan a un 1/3 de la cara (desde el pelo)
                        xpos = x #ancho de las gafas igual a la cara
                        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
                        factor = 1.0*w/w_sprite
                        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)

                        image = draw_sprite(image,sprite,xpos,ypos)

                # OpenCV represents image as BGR; PIL but RGB, we need to change the chanel order
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # conerts to PIL format
                image = Image.fromarray(image)
                # Converts to a TK format to visualize it in the GUI
                image = ImageTk.PhotoImage(image)
                # Actualize the image in the panel to show it
                panelA.configure(image=image)
                panelA.image = image

# Initialize GUI object
root = Tk()

##Create 3 buttons and assign their corresponding function to active sprites
btn1 = Button(root, text="Hat", command=put_hat)
btn1.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn2 = Button(root, text="Mustache", command=put_mustache)
btn2.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn3 = Button(root, text="Flies", command=put_flies)
btn3.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn4 = Button(root, text="Glasses", command=put_glasses)
btn4.pack(side="top", fill="both", expand="no", padx="10", pady="10")

# Create the panel where webcam image will be shown
panelA = Label(root)
panelA.pack( padx=10, pady=10)

# Variable to control which sprite you want to visualize
SPRITES = [0,0,0,0] #hat, mustache, flies, glasses -> 1 is visible, 0 is not visible


# Creates a thread where the magic ocurs
run_event = threading.Event()
run_event.set()
action = Thread(target=cvloop, args=(run_event,))
action.start()

# Function to close all properly, aka threads and GUI
def terminate():
        global root, run_event, subprocess
        print "Closing thread opencv..."
        run_event.clear()
        action.join()
        root.destroy()
        print "All closed! Chao"

# When the GUI is closed it actives the terminate function
root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop() #creates loop of GUI
