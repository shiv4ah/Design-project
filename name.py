import smtplib

import imagehash
from PIL import Image
import cv2
import os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from sample_data import student


def image_matching(a,b):
    i1 = Image.open(a)
    i2 = Image.open(b)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
    # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    xx= (dif / 255.0 * 100) / ncomponents
    return xx


def match_templates(in_image):
    name=[]
    values=[]
    entries = os.listdir('train/')
    folder_lenght= len(entries)
    i=0
    for x in entries:
        val=100
        directory=x
        name.append(x)
        x1="train/"+x

        arr = os.listdir(x1)
        for x2 in arr:
             path=x1+"/"+str(x2)
             find=image_matching(path,in_image)
             hash0 = imagehash.average_hash(Image.open(path))
             hash1 = imagehash.average_hash(Image.open(in_image))
             cc1=hash0 - hash1
             print(cc1)
             find=cc1
             if(find<val):
                 val=find
        values.append(val)
    values_lenght= len(values)
    pos=0
    pos_val=100
    for x in range(0, values_lenght):
        if values[x]<pos_val:
            pos=x
            pos_val=values[x]

    if(pos_val<20):
        print(pos,pos_val,name[pos])
        return name[pos]
    else:
        return "unknown"


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
train=True
video_capture = cv2.VideoCapture(0)
name="testing"
if os.path.exists(name):
    h=0
else:
    os.mkdir(name)
e_mail=0
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
    facecnt = len(faces)
    #print("Detected faces: %d" % facecnt)
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
            font = cv2.FONT_HERSHEY_SIMPLEX

            str1=name+'\\tt.jpg'
            # kk=kk+1

            lastimg = cv2.resize(faceimg, (100, 100))

            cv2.imwrite(str1, lastimg)
            ar=match_templates(str1)
            print(ar)

            if ar=="unknown":
                e_mail=e_mail+1
            else:
                e_mail=0

            #print e_mail

            if e_mail>=30:

                msg = MIMEMultipart()
                s=student
                to_mail=s.email

                password = "egjuabqhwvktwdqf"
                msg['From'] = "serverkey2018@gmail.com"
                msg['To'] = to_mail
                msg['Subject'] = "Unknown Face Detected"
                file = str1
                fp = open(file, 'rb')
                img = MIMEImage(fp.read())
                fp.close()
                msg.attach(img)
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                server.login(msg['From'], password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()



            cv2.putText(faceimg, (ar), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0),2,cv2.LINE_AA)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

