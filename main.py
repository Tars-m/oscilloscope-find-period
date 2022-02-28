import numpy as np
import math
import random
import cv2 as cv
font = cv.FONT_HERSHEY_SIMPLEX
def nothing(x):
    pass

altezza = 512
lunghezza = 700

img = np.zeros((altezza,lunghezza,3), np.uint8)
cv.namedWindow('oscilloscope')
cv.createTrackbar("trig1", "oscilloscope", 1,100, nothing)
cv.createTrackbar("trig2", "oscilloscope", 1,100, nothing)
cv.createTrackbar("rumore","oscilloscope",0,50,nothing)
cv.createTrackbar("periodo","oscilloscope",100,1000,nothing)
trig1=0
trig2=0

def findmax(signal, num):
    maxval = signal[0]
    for i in range(num):
       if(signal[i]>maxval):
           maxval=signal[i]
    return maxval

def findmin(signal, num):
    minval = signal[0]
    for i in range(num):
       if(signal[i]<minval):
           minval=signal[i]
    return minval
def error():
    print("Scelta sbagliata o numero di campioni troppo limitato, riprova..")

def findperiod(signal, num, trig1, trig2):
    #trova il campione di inizio periodo di indice n1
    flag1=False
    n1=0 #commento solo così
    n2=0
    for i in range(10,num):
        if((-signal[i]<=trig1)&(-signal[i+1]>trig1)):
            n1=i
            flag1 = True
            break
    if not flag1:
        error()
        return

    flag1 = False
    flag2 = False

    for i in range(n1,num):
        if((-signal[i] <= trig2)&(-signal[i+1]>trig2)):
            flag1= True
        if(flag1&(-signal[i]<=trig1)&(-signal[i+1]>trig1)):
            flag2 = True
            n2=i
            break
    if not flag2:
        error()
        return
    return [n1,n2]

def signalCreate(periodo_settato,signal):
    signal.clear()
    for k in range(lunghezza):
            signal.append(200*math.sin(math.radians((periodo_settato/100)*k)))

def disegnaOnda(signal):
    signalNew=[]
    while (1):
        img[:] = 0
        signalNew.clear()
        moltiplicatore = cv.getTrackbarPos("periodo", "oscilloscope")
        cv.line(img, (0, int(altezza / 2)), (lunghezza, int(altezza / 2)), (20, 20, 20), 2, cv.LINE_AA)
        trig1 = (altezza / 2) - cv.getTrackbarPos("trig1", "oscilloscope")
        trig1 = int(trig1)
        cv.line(img, (0, trig1), (lunghezza, trig1), (255, 0, 0), 1, cv.LINE_AA)
        trig2 = (altezza / 2) + cv.getTrackbarPos("trig2", "oscilloscope")
        trig2 = int(trig2)
        cv.line(img, (0, trig2), (lunghezza, trig2), (0, 255, 0), 1, cv.LINE_AA)
        noise=cv.getTrackbarPos("rumore","oscilloscope")
        signalCreate(moltiplicatore, signal)
        for w in range(lunghezza):
            if (w % 2 == int(random.randint(0,1))):
                signalNew.append(signal[w] + random.randint(-noise, noise))
            else:
                signalNew.append(signal[w])
        for f in range(lunghezza-1):
            a=int((altezza/2)+signalNew[f])
            img[a,f]=[0,0,255]
        n1n2 = findperiod(signalNew, lunghezza - 1, cv.getTrackbarPos("trig1", "oscilloscope"),
                          -cv.getTrackbarPos("trig2", "oscilloscope"), )

        if n1n2 is not None:
            cv.line(img, (n1n2[0], 0), (n1n2[0], 512), (255, 100, 100),1, cv.LINE_AA)
            cv.line(img, (n1n2[1], 0), (n1n2[1], 512), (255, 100, 100), 1, cv.LINE_AA)
            periodo_ricavato=str((n1n2[1]-n1n2[0]))
            cv.putText(img, periodo_ricavato, (0, 300), font, 1, (255, 255, 255), 2, cv.LINE_AA)

        k = cv.waitKey(30) & 0xFF
        if k == 27:
            break
            cv2.destroyAllWindows()
        cv.imshow("oscilloscope", img)


if __name__ == '__main__':
    signal=[]
    disegnaOnda(signal)

