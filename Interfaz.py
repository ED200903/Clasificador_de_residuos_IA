import cv2
from ultralytics import YOLO
from tkinter import *
from PIL import Image, ImageTk
import imutils
import numpy as np
import math
import serial
from time import sleep


#Inicializamos el puerto de serie a 9600 baud
ser = serial.Serial('COM7', 9600)

sleep(5)

def mover_servos(angulo1, angulo2):
    comando = f"{angulo1},{angulo2}\n"  # Formato del comando
    ser.write(comando.encode())  # Enviar el comando al Arduino

#show Images
def images(img, imgtxt):
    img = img
    imgtxt = imgtxt

    #Img detect
    img = np.array(img, dtype="uint8")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = Image.fromarray(img)

    img_ = ImageTk.PhotoImage(image=img)
    lblimg.configure(image=img_)
    lblimg.image = img_

    imgtxt = np.array(imgtxt, dtype="uint8")
    imgtxt = cv2.cvtColor(imgtxt, cv2.COLOR_RGB2BGR)
    imgtxt = Image.fromarray(imgtxt)

    imgtxt_ = ImageTk.PhotoImage(image=imgtxt)
    lblimgtxt.configure(image=imgtxt_)
    lblimgtxt.image = imgtxt_

#Scanning function
def Scanning():
    global lblimg, lblimgtxt

    #Interfaz
    lblimg = Label(pantalla)
    lblimg.place(x=50, y=260)
    lblimgtxt = Label(pantalla)
    lblimgtxt.place(x=995, y=310)

    #Read VideoCapture
    if cap is not None:
        ret, frame = cap.read()
        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret == True:

            results = model(frame, stream=True, verbose=False)
            for res in results:
                #Box
                boxes = res.boxes
                for box in boxes:
                    #Boonding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    #Error
                    if x1 < 0: x1 = 0
                    if y1 < 0: y1 = 0
                    if x2 < 0: x2 = 0
                    if y2 < 0: y2 = 0

                    #Clase
                    cls = int(box.cls[0])

                    #Confidence
                    conf = math.ceil(box.conf[0])

                    if conf > 0.5: #CARTON
                        if cls == 0:
                            #Draw Rectangle
                            cv2.rectangle(frame_show, (x1,y1), (x2,y2), (111, 78, 55), 2)

                            #Text
                            text = f'{clsName[cls]} {int(conf)*100}%'
                            sizetext = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                            dim = sizetext[0]
                            baseline = sizetext[1]
                            #Rectangle
                            cv2.rectangle(frame_show, (x1, y1 - dim[1] - baseline), (x1 + dim[0], y1 + baseline), (111, 78, 55), cv2.FILLED)
                            cv2.putText(frame_show, text, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                            #Image
                            images(img_Carton, img_cartontxt)

                            mover_servos(0, 70)


                    if conf > 0.5: #LATAS
                        if cls == 1:
                            #Draw Rectangle
                            cv2.rectangle(frame_show, (x1,y1), (x2,y2), (255, 0, 0), 2)

                            #Text
                            text = f'{clsName[cls]} {int(conf)*100}%'
                            sizetext = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                            dim = sizetext[0]
                            baseline = sizetext[1]
                            #Rectangle
                            cv2.rectangle(frame_show, (x1, y1 - dim[1] - baseline), (x1 + dim[0], y1 + baseline), (255, 0, 0), cv2.FILLED)
                            cv2.putText(frame_show, text, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                            # Image
                            images(img_Latas, img_latastxt)

                            mover_servos(0 , 0)
                            

                    if conf > 0.5: #PLASTIC
                        if cls == 2:
                            #Draw Rectangle
                            cv2.rectangle(frame_show, (x1,y1), (x2,y2), (0, 0, 255), 2)

                            #Text
                            text = f'{clsName[cls]} {int(conf)*100}%'
                            sizetext = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                            dim = sizetext[0]
                            baseline = sizetext[1]
                            #Rectangle
                            cv2.rectangle(frame_show, (x1, y1 - dim[1] - baseline), (x1 + dim[0], y1 + baseline), (0, 0, 255), cv2.FILLED)
                            cv2.putText(frame_show, text, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                            #Images
                            images(img_Plastic, img_plastictxt)

                            mover_servos(50, 0)


                    if conf > 0.5: #Glass
                        if cls == 3:
                            #Draw Rectangle
                            cv2.rectangle(frame_show, (x1,y1), (x2,y2), (0, 128, 0), 2)

                            #Text
                            text = f'{clsName[cls]} {int(conf)*100}%'
                            sizetext = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                            dim = sizetext[0]
                            baseline = sizetext[1]
                            #Rectangle
                            cv2.rectangle(frame_show, (x1, y1 - dim[1] - baseline), (x1 + dim[0], y1 + baseline), (0, 128, 0), cv2.FILLED)
                            cv2.putText(frame_show, text, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                            # Image
                            images(img_Glass, img_vidriotxt)

                            mover_servos(0, 0)
            #Resize
            frame_show = imutils.resize(frame_show, width=640)

            #Convertir Video
            im = Image.fromarray(frame_show)
            img = ImageTk.PhotoImage(image=im)

            #Mostrar
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Scanning)
        else:
            cap.release()


#main
def ventana_principal():
    global model, clsName, img_Carton, img_Latas, img_Plastic, img_Glass, lblVideo
    global img_cartontxt, img_latastxt, img_plastictxt, img_vidriotxt, cap, pantalla

    #Ventana principal
    pantalla = Tk()
    pantalla.title("Reciclaje AI")
    pantalla.geometry("1280x720")

    #Background
    ImagenF = PhotoImage(file="E:\DATASCIENCE\Proyecto\Images\Background1.png")
    background = Label(image=ImagenF)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    #Model
    model = YOLO('E:/DATASCIENCE/Proyecto/models/best.pt')

    #Clases
    clsName = ['Carton','Aluminio','Plastico','Vidrio']

    #Img
    img_Carton = cv2.imread('E:\DATASCIENCE\Proyecto\Images\carton.png')
    img_Latas = cv2.imread('E:/DATASCIENCE/Proyecto/Images/aluminio.png')
    img_Plastic = cv2.imread('E:\DATASCIENCE\Proyecto\Images\plastico.png')
    img_Glass = cv2.imread('E:/DATASCIENCE/Proyecto/Images/vidrio.png')
    img_cartontxt = cv2.imread('E:\DATASCIENCE\Proyecto\Images\setUp_cartontxt.png')
    img_latastxt = cv2.imread('E:\DATASCIENCE\Proyecto\Images\setUp_metaltxt.png')
    img_plastictxt = cv2.imread('E:\DATASCIENCE\Proyecto\Images\setUp_plasticotxt.png')
    img_vidriotxt = cv2.imread('E:\DATASCIENCE\Proyecto\Images\setUp_vidriotxt.png')

    #label video
    lblVideo = Label(pantalla)
    lblVideo.place(x=319,y=118)

    #Cam
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    #Scanning
    Scanning()

    #Loop
    pantalla.mainloop()

if __name__ == '__main__':
    ventana_principal()