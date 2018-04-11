import cv2
import numpy as np
import Persona
import time
import urllib
import imutils

cap = cv2.VideoCapture(0)
#cv2.VideoCapture.set.PROP_BUFFERSIZE(cap,3)

#Contadores de entrada y salida
cnt_up   = 0
cnt_down = 0
retval, frame = cap.read()
print retval
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #Create the background substractor
kernelOp = np.ones((3,3),np.uint8) #matrix that  defines the area to use when calculating the value of each pixel.
kernelCl = np.ones((11,11),np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX


personas = []
idp= 1
Maxage = 5
w = cap.get(3) #Obtener ancho del video
h = cap.get(4) #Obtener alto del VideoCapture
frameArea = h*w
Minarea = frameArea/50  #/250


#Lineas de entrada/salida
line_up = int(2*(h/5))
line_down   = int(3*(h/5))
line_down_color = (19, 254, 0)
line_up_color = (0,0,255)

up_limit =   int(1*(h/5))
down_limit = int(4*(h/5))

print "Up red line y:", str(line_up)
print "Down green line y:",str(line_down)
print Minarea

pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))

pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))

pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))
#puntos de las lineas


while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    fgmask = fgbg.apply(frame) #Aplicar el bg substractor al fram, Use the substractor.
    fgmask2 = fgbg.apply(frame)

    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY) #Binarizar la imagen a blancos y negros unicamente.
        #Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regiones blancas.
        mask = cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        #cv2.imshow('Frame',frame)#mostrar frame
        #cv2.imshow('Background Substraction',mask)


    except:
        #if there are no more frames to show...
        print('END')
        print 'UP:',cnt_up
        print 'DOWN:',cnt_down
        break

    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)

        if area > Minarea :
           #realizar tracking#
           M = cv2.moments(cnt)
           cx = int(M['m10']/M['m00']) #sacar el centro de la figura
           cy = int(M['m01']/M['m00'])
           x,y,w,h = cv2.boundingRect(cnt)

           new = True
           for i in personas:
               #print len(personas)
               i.age_one() #age every person one frame
               if (abs(x-i.getX()) <= w and abs(y-i.getY()) <= h): #Si el objeto esta cerca de uno detectado previamente
                   new = False #No es una nueva persona
                   i.updateCoords(cx,cy) #Actualizar coordenadas de la personas
                   if (i.going_UP(line_up) == True):
                       cnt_up += 1;
                       print "ID:",i.getId(),'va hacia arriba a las ',time.strftime("%c")

                   elif(i.going_DOWN(line_down)==True):
                        cnt_down += 1;
                        print "ID:",i.getId(),'va hacia abajo a las ',time.strftime("%c")
                   break

               if(i.getState() == '1'):
                 if(i.getDir() == 'down' and i.getY() > down_limit):
                    i.setDone()
                 elif(i.getDir() == 'up' and i.getY() < up_limit):
                      i.setDone()

               if(i.done == True):
                  #sacar i de la lista persons
                  index = personas.index(i)
                  personas.pop(index)
                  del i     #liberar la memoria de i


           if(new ==True):
              p = Persona.MyPerson(idp,cx,cy,Maxage)
              personas.append(p)
              idp += 1

           #Dibujar circulo, rectangulo y contornos #
           cv2.circle(frame,(cx,cy), 5, (0,0,255), -1) #dibujar circulo
           img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) #dibujar rectangulo
          ## cv2.drawContours(frame, cnt, -1, (0,255,255), 3, 8) #dibujar contornos


# DIBUJAR  #
    for i in personas:
        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
        str_up = 'Salen: '+ str(cnt_up)
        str_down = 'Entran: '+ str(cnt_down)
        frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        #frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        #frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        #cv2.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
        #cv2.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, str_down ,(10,90),font,0.5,(19, 254, 0),1,cv2.LINE_AA)

    #     if len(i.getTracks()) >= 2:
    #        pts = np.array(i.getTracks(), np.int32)
    #        pts = pts.reshape((-1,1,2))
    #        frame = cv2.polylines(frame,[pts],False,i.getRGB())


        # if i.getId() == 9:
        #    print str(i.getX()), ',', str(i.getY())
        #    cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)


    cv2.imshow('Frame',frame)

    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows
