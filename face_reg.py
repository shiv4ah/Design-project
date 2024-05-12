import cv2
import sys
import os


from sample_data import student

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
train=True
video_capture = cv2.VideoCapture(0)
name="train"
if os.path.exists(name):
    h=0
else:
    os.mkdir(name)

s1=student
print(s1.name)
name1="train\\"+s1.name
if os.path.exists(name1):
    j=0
else:
    os.mkdir(name1)
k=0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
######
    if (frame is None):
            print("Can't open image file")
    face_cascade = cv2.CascadeClassifier(cascPath)
    faces = face_cascade.detectMultiScale(frame, 1.1, 3, minSize=(100, 100))
    if (faces is None):
            print('Failed to detect face')

    if (True):
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                #lastimg = cv2.resize(frame, (32, 32))
            #cv2.imshow('img', frame)

    facecnt = len(faces)
    print("Detected faces: %d" % facecnt)
    i = 0
    height, width = frame.shape[:2]

    for (x, y, w, h) in faces:
            r = max(w, h) / 2
            centerx = x + w / 2
            centery = y + h / 2
            nx = int(centerx - r)
            ny = int(centery - r)
            nr = int(r * 2)

            faceimg = frame[ny:ny+nr, nx:nx+nr]
            lastimg = cv2.resize(faceimg, (100, 100))
            i += 1
            k+=1
            if ((k<20)&(k>=5)):
                str=name1+'\\%d.jpg'%k
                cv2.imwrite(str, lastimg)




    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

