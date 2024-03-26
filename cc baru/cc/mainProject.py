import cv2 as cv
import pickle
import time
import numpy as np
import os
import cvzone as cvz
import face_recognition
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage
cred = credentials.Certificate('C:/Users/Candra Naradhipa/Downloads/cc baru/cc/serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
'databaseURL': "https://fv-project-81f32-default-rtdb.firebaseio.com/",
'storageBucket':"fv-project-81f32.appspot.com"
})

cap = cv.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cap.set(cv.CAP_PROP_FPS, 45)

imgBackground = cv.imread('resource/bg.jpg')

folderMode = 'resource/ModesNew'
modePath = os.listdir(folderMode)
imgModeList = []
for path in modePath:
    imgModeList.append(cv.imread(os.path.join(folderMode, path)))
# print(len(imgModeList))

FaceDist = None
match = None

#load encoder
print("loading encoder")
file = open('encodefile.p', 'rb')
knownEncodeID = pickle.load(file)
file.close()
knownEncode, stdID = knownEncodeID
# print(stdID)
print("encoder loaded")

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()
    
    #camera    
    new_width = int(0.7 * img.shape[1])
    new_height = int(0.7 * img.shape[0])
    imgS = cv.resize(img, (new_width, new_height))    
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCF = face_recognition.face_locations(imgS)
    encodeCF = face_recognition.face_encodings(imgS, faceCF)
    
    imgBackground[200:200+imgS.shape[0], 50:50+imgS.shape[1]] = imgS

    #status
    resized_width = int(1.0 *587)
    resized_height = int(1.3 * 174)
    imgModeResized = cv.resize(imgModeList[modeType], (resized_width, resized_height))
    imgBackground[305:305 + imgModeResized.shape[0], 539:539 + imgModeResized.shape[1]] = imgModeResized

        
    for encodeFace, faceLoc in zip(encodeCF, faceCF):
        # print(faceLoc)
        match = face_recognition.compare_faces(knownEncode, encodeFace)
        FaceDist = face_recognition.face_distance(knownEncode, encodeFace)
        # print('Loop iteration executed')
        # print('matches:', match)
        # print('faceDis:', faceDis)

    matchedindex = np.argmin(FaceDist)
    # print("match index : ", matchIndex)
    
    if encodeCF:  # Check if encodeCF is not empty
        matchedIndex = np.argmin(FaceDist)
        
        if match[matchedIndex]:
            # print("Known Face Detected")
            # print(stdID[matchedIndex])
            # time.sleep(1)
            # y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            # imgBackground = cvz.cornerRect(imgBackground, bbox, rt=0)
                        
            id = stdID[matchedIndex]
            # print(id)            
            if counter == 0:
                counter = 1
                modeType = 1
    if counter!= 0:
        if counter == 1:
            stdInfo = db.reference(f'Mahasiswa/{id}').get()
            print(stdInfo)
            
            #update attendance
            datetimeObject = datetime.strptime(stdInfo['last_Attendance_Time'],
                                                "%Y-%m-%d %H:%M:%S")

            secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 30:
                ref = db.reference(f'Mahasiswa/{id}')
                stdInfo['total_attendance'] +=1
                ref.child('total_attendance').set(stdInfo['total_attendance'])
                ref.child('last_Attendance_Time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else :
                modeType = 3
                counter = 0
                imgBackground[305:305 + imgModeResized.shape[0], 539:539 + imgModeResized.shape[1]] = imgModeResized
                
        if modeType != 3:
            
    
            if 10<counter<20:
                modeType = 2
                imgBackground[305:305 + imgModeResized.shape[0], 539:539 + imgModeResized.shape[1]] = imgModeResized

            
            if counter <= 10:
                        
                cv.putText(imgBackground, str(stdInfo['total_attendance']), (861, 125),
                            cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                # (w, h), _ = cv.getTextSize(stdInfo['Nama'], cv.FONT_HERSHEY_COMPLEX, 1, 1)
                # cv.putText(imgBackground, str(stdInfo['Nama']), (922, 445),
                #             cv.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)
                # cv.putText(imgBackground, str(stdInfo['Jurusan']), (835, 550),
                #             cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)# background, info, koordinat, font, ukuran, warna, tebal
                # cv.putText(imgBackground, str(id), (950, 493),
                #             cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            
    counter+=1
    
    if counter > 20:
        counter = 0
        modeType = 0
        stdInfo = []
        
        imgBackground[305:305 + imgModeResized.shape[0], 539:539 + imgModeResized.shape[1]] = imgModeResized


    # cv.imshow("webcam", img)
    cv.imshow("face attendance", imgBackground)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv.destroyAllWindows()
