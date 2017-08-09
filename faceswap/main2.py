# import the necessary packages
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog, cv2, time, threading, dlib, tkMessageBox, os
from threading import Thread
from utils import face_swap_cropedimage
import numpy as np

DATA = [None, None] #First element will be the image reference and the second the face rectangle in that image

# boundbox is an array in the form: x,y,w,h
def is_in_boundbox(x,y,boundbox):
    if (x < boundbox[0] or x > boundbox[0] + boundbox[2]):
        return False
    if (y < boundbox[1] or y > boundbox[1] + boundbox[3]):
        return False
    return True

#Principal Loop where openCV (magic) ocurs
def cvloop(run_event):
    global panelA, DATA

    print("[INFO] loading facial landmark predictor...")
    model = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model)

    video_capture = cv2.VideoCapture(0) #read from webcam

    panelA = Label()
    panelA.pack(side="left", padx=10, pady=10)

    while run_event.is_set(): #while the thread is active we loop
        ret, image = video_capture.read()

        img_ref = DATA[0]
        face_ref_rect = DATA[1]

        if face_ref_rect != None:
            swapped = face_swap_cropedimage(img_ref, face_ref_rect, image, detector, predictor)
            if swapped is not None:
                image = swapped

        # OpenCV represents image as BGR; PIL but RGB, we need to change the chanel order
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # converts to PIL format
        image = Image.fromarray(image)
        # Converts to a TK format to visualize it in the GUI
        image = ImageTk.PhotoImage(image)
        # Actualize the image in the panel to show it
        panelA.configure(image=image)
        panelA.image = image

    video_capture.release()


def select_image():
    # grab a reference to the image panels
    global panelB

    # open a file chooser dialog and allow the user to select an input
    # image
    path = tkFileDialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0:
    	# load the image from disk, convert it to grayscale, and detect
    	# edges in it
        image = cv2.imread(path)

        if image is None:
            tkMessageBox.showerror("Error", "Not a valid image file")
        assert image is not None, "Not a valid image file"

        DATA[0] = np.copy(image);
        DATA[1] = None

        # Face Detector
        detector = dlib.get_frontal_face_detector()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)
        bound_boxes = []
        for face in faces: #if there are faces
            (x,y,w,h) = (face.left(), face.top(), face.width(), face.height())
            bound_boxes.append([x,y,w,h])
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # convert the images to PIL format...
        image = Image.fromarray(image)

        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)

        # if the panels are None, initialize them
        if panelB is None:
        	# while the second panel will store the edge map
        	panelB = Label(image=image)
        	panelB.image = image
        	panelB.pack(side="right", padx=10, pady=10)

        # otherwise, update the image panels
        else:
        	# update the pannels
        	panelB.configure(image=image)
        	panelB.image = image

        def printcoord(event,bound_boxes, rect_boxes):
            global DATA
            any_face = False
            for i, bound in enumerate(bound_boxes):
                if is_in_boundbox(event.x,event.y, bound):
                    DATA[1] = rect_boxes[i]
                    any_face = True
            if not any_face: #clicked outside faces then not more swapping
                DATA[1] = None

        #mouseclick event
        panelB.bind("<Button 1>",lambda event: printcoord(event, bound_boxes, faces))


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Face Swapping App")
this_dir = os.path.dirname(os.path.realpath(__file__))
# Adds a custom logo
imgicon = PhotoImage(file=os.path.join(this_dir,'icon.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)

# Create the panel where webcam image will be shown
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


# Creates a thread where the magic ocurs
run_event = threading.Event()
run_event.set()
action = Thread(target=cvloop, args=(run_event,))
action.setDaemon(True)
action.start()


# Function to close all properly, aka threads and GUI
def terminate():
        global root, run_event, action
        print "Closing thread opencv..."
        run_event.clear()
        time.sleep(1)
        #action.join() #strangely in Linux this thread does not terminate properly, so .join never finishes
        root.destroy()
        print "All closed! Chao"

# When the GUI is closed it actives the terminate function
root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop() #creates loop of GUI
