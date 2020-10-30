import cv2
import numpy as np
import math

origen = cv2.VideoCapture('CarsDrivingUnderBridge.mp4')
ret, cam = origen.read()
ret2, cam2 = origen.read()
kernel = np.ones((5,5), np.uint8)
nCarros = 0
contador = 0
while(origen.isOpened()):   
    if ret == False or ret2 == False:
        break
    imgGris = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)
    imgGris2 = cv2.cvtColor(cam2, cv2.COLOR_BGR2GRAY)
    imgBlurred1 = cv2.GaussianBlur(imgGris, (5, 5), 0)
    imgBlurred2 = cv2.GaussianBlur(imgGris2, (5, 5), 0)
    alto, ancho, algo = cam.shape
    imgDif = cv2.absdiff(imgBlurred1, imgBlurred2)
    # Threshold por defecto de opencv
    ret, imgTh = cv2.threshold(imgDif,30,255,cv2.THRESH_BINARY)

    # Erosiona y dilatar los objetos
    imgE = cv2.erode(cv2.dilate(imgTh, kernel, iterations=3), kernel, iterations=2)

    contours, hierarchy = cv2.findContours(imgE, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blackImg = np.zeros((np.size(imgTh,0),np.size(imgTh,1)), np.uint8)
    cv2.drawContours(blackImg, contours, -1, (255,255,255), -1)
    #cv2.imshow('Contornos', blackImg)

    # Ahora que tenemos los contornos hay que buscar los posibles autos
    hull = []
    for j in range(len(contours)):
        hull.append(cv2.convexHull(contours[j], False))

    fondo1 = np.zeros((np.size(imgTh,0),np.size(imgTh,1)), np.uint8)
    for k in range(len(contours)):
        cv2.drawContours(fondo1, contours, k, (0,255,0), 1,8, hierarchy)
        cv2.drawContours(fondo1, hull, k, (255,255,255), 1, 8)
    cv2.imshow('ContornosYMas', imgE)
    #cv2.imshow('Figuras', imgE)

    for l in range(len(hull)):
        x,y,w,h = cv2.boundingRect(hull[l])
        perimetro = cv2.arcLength(hull[l],True)
        area = cv2.contourArea(hull[l])
        rAspecto = float(w)/h
        tamDiagonal = math.sqrt(w*w + h*h)
        areaRect = w*h
        if perimetro > 100 and area > 1000 and rAspecto > 0.2 and rAspecto < 4.0 and w > 30 and h > 30 and tamDiagonal > 60 and area/areaRect > 0.5:   
        #if perimetro > 80 and area > 300 and rAspecto > 0.2 and rAspecto < 4.0 and w > 20 and h > 20 and tamDiagonal > 30 and area/areaRect > 0.5:   
            if y > alto*5/8 and y < alto*5/8 + 15:
                nCarros += 1
                #print (nCarros)
            cv2.rectangle(cam, (x,y), (x+w,y+h), (0,255,0),3)
    cv2.line(cam, (int(0), int(alto*5/8)),(int(ancho), int(alto*5/8)), (0,0,255), 2)
    cv2.imshow('Original', cam)

    cam = cam2
    if ((origen.get(cv2.CAP_PROP_POS_FRAMES) + 1) < origen.get(cv2.CAP_PROP_FRAME_COUNT)): 
        r, cam2 = origen.read()

    # contador += 1
    # if contador == 600:
    #     fCarros = open('carros.txt', 'a')
    #     fCarros.write('\n'+str(nCarros))
    #     fCarros.close()
    #     contador = 0
    #     nCarros = 0
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# Deben ser 52 carros en el carril de la derecha para los carros debajo del puente


print (nCarros)
origen.release()
cv2.destroyAllWindows()