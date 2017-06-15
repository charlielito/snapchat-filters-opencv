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
def poner_sombrero():
        global SPRITES
        SPRITES[0] = (1 - SPRITES[0]) #not actual value

def poner_bigote():
        global SPRITES
        SPRITES[1] = (1 - SPRITES[1]) #not actual value

def poner_moscas():
        global SPRITES
        SPRITES[2] = (1 - SPRITES[2]) #not actual value

def poner_gafas():
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

#Returns the rectangles
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

#ajusta el sprite dado, al ancho de la cabeza y la posicion de la cabeza
#en caso de que se que salga de la imagen, recorta el sprite
def ajustar_sprite_cabeza(sprite, ancho_cabeza, y_pos_cabeza):
        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
        factor = 1.0*ancho_cabeza/w_sprite
        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor) #ajusta al ancho de la cabeza
        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
        y_orig =  y_pos_cabeza-h_sprite #ajusta la posicion del sprite
        if (y_orig < 0): #chequea que no se salga de la imagen
                sprite = sprite[abs(y_orig)::,:,:] #en caso que se salga, la recorta
                y_orig = 0 #el sprite va en la parte superior de la imagen
        return (sprite, y_orig)

#Loop pricipal donde se manejan los accesorios y funciones openCV
def cvloop(run_event):
        global panelA
        global SPRITES
        
        # Filtro Haar
        faceCascade = cv2.CascadeClassifier("./filters/haarcascade_frontalface_default.xml")
        
        carpeta = "./sprites/flyes/"
        moscas = [f for f in listdir(carpeta) if isfile(join(carpeta, f))] #imagenes de moscas
        i = 0
        video_capture = cv2.VideoCapture(0) #leemos de la WebCam
        (x,y,w,h) = (0,0,10,10)
        while run_event.is_set(): #mientras el Hilo deba esta activo
                ret, image = video_capture.read()

                caras = detectar_caras(image,faceCascade,1.3)
                if (len(caras) != 0 ): #si hay caras en la foto
                        #toma el tamano de la primera cara que encuentra
                        (x,y,w,h) = (caras[0,0],caras[0,1],caras[0,2],caras[0,3]) 
                #condicion de sombrero
                if SPRITES[0]:
                        sprite = cv2.imread("./sprites/hat.png",-1)

                        (sprite, y_final) = ajustar_sprite_cabeza(sprite, w, y)
                        
                        image = draw_sprite(image,sprite,x, y_final)
                #bigote
                if SPRITES[1]:
                        sprite = cv2.imread("./sprites/mustache.png",-1)

                        ypos = y + 2*h/3 #empiricamente el bigote esta a un 2/3 de la cara (desde el pelo)
                        xpos = x + w/4 #empiricamente el ancho del bigote es la mitad
                        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
                        factor = 1.0*(w/2)/w_sprite
                        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)
                        
                        image = draw_sprite(image,sprite,xpos,ypos)
                #moscas
                if SPRITES[2]:
                        #para hacer la "animacion" de las moscas, va leyendo imagenes distintas cada loop
                        #y asi da la impresion de movimiento
                        sprite = cv2.imread(carpeta+moscas[i],-1)

                        (sprite, y_final) = ajustar_sprite_cabeza(sprite, w, y)

                        image = draw_sprite(image,sprite,x,y_final)
                        i+=1
                        i = 0 if i >= len(moscas) else i #cuando termine de leer todas las imagenes en la carpeta, reinicia

                #gafas
                if SPRITES[3]:
                        sprite = cv2.imread("./sprites/glasses.png",-1)

                        ypos = y + h/3 #empiricamente los ojos estan a un 1/3 de la cara (desde el pelo)
                        xpos = x #ancho de las gafas igual a la cara
                        (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
                        factor = 1.0*w/w_sprite
                        sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)
                        
                        image = draw_sprite(image,sprite,xpos,ypos)
                
                # OpenCV representa imagenes en orden BGR; pero PIL en RGB, hay que cambiar orden
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # convierte a formato PIL
                image = Image.fromarray(image)
                # Luego a formato ImageTk (para visualizarlo en GUI)
                image = ImageTk.PhotoImage(image)
                #Actualizamos panel del GUI con la imagen a mostrar
                panelA.configure(image=image)
                panelA.image = image

#Inicializamos el panel de GUI
root = Tk()

##Creamos 3 botones y les asignamos distintas funciones 
btn1 = Button(root, text="Hat", command=poner_sombrero)
btn1.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn2 = Button(root, text="Mustache", command=poner_bigote)
btn2.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn3 = Button(root, text="Flyes", command=poner_moscas)
btn3.pack(side="top", fill="both", expand="no", padx="10", pady="10")

btn4 = Button(root, text="Glasses", command=poner_gafas)
btn4.pack(side="top", fill="both", expand="no", padx="10", pady="10")
# Creamos panel donde va a estar la imagen de la WebCam y el resto
panelA = Label(root)
panelA.pack( padx=10, pady=10)

# Variable para controlar que "sprite" o accesorio queremos poner en la cara
SPRITES = [0,0,0,0] #sombrero, bigote, moscas, gafas -> 1 significa mostrar accesorio, 0 lo contrario


# Crea hilo para manejar la parte de la camara y openCV
run_event = threading.Event() #maneja evento para decirle al hilo cuando acabar
run_event.set()
subprocess = Thread(target=cvloop, args=(run_event,)) #crea el hiilo
subprocess.start() #inicia el hilo

# Funcion para manejar que todo se cierre bien, es decir, el hilo principal acabe sin errores
def cerrar_ventana():
        global root, run_event, subprocess
        print "Closing thread opencv..."
        run_event.clear()
        subprocess.join()
        root.destroy()
        print "All closed! Chao"
        
# Activa la funcion cuando se cierra la ventana de la GUI
root.protocol("WM_DELETE_WINDOW", cerrar_ventana)
root.mainloop() #crea el loop que maneja la perte visual


