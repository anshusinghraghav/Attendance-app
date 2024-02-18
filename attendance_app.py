import cv2
import os
import cvzone
import numpy as np
import pickle
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-app-1a0c6-default-rtdb.firebaseio.com/",
    'storageBucket':"attendance-app-1a0c6.appspot.com"
})


bucket=storage.bucket()



cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgbackground=cv2.imread("C:/Users/HP/Downloads/my codes/resources/background.png")

# importing modes images into list
foldermodepath="C:/Users/HP/Downloads/my codes/resources/modes"
modepathlist=os.listdir(foldermodepath)
imgmodelist=[]

for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(foldermodepath,path)))

#load the encoding file
print("loading encode file...")
file=open("encodefile.p","rb") 
encodelistknownwithid=pickle.load(file)
file.close()
encodelistknown,studentids=encodelistknownwithid
print("encode file loaded...")
# print(studentids)
# print(len(imgmodelist))    
# print(modepathlist)


modetype=0
counter=0
id=-1
imgstudent=[]

    
while True:

    success,img=cap.read()

    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    facecurrframe=face_recognition.face_locations(imgs)
    encodecurrframe=face_recognition.face_encodings(imgs,facecurrframe)

    imgbackground[162:642,55:695]=img
    imgbackground[44:677,808:1222]=imgmodelist[modetype]

    if facecurrframe:

        for encodeface,faceloc in zip(encodecurrframe,facecurrframe):
            matches=face_recognition.compare_faces(encodelistknown,encodeface)
            facedis=face_recognition.face_distance(encodelistknown,encodeface)
            # print("matches",matches)
            # print("facedis",facedis) 
            
            matchindex=np.argmin(facedis)
            #print("match index",matchindex)

            if matches[matchindex]:
                # print("Face Detected")
                # print(studentids[matchindex])
                y1,x2,y2,x1=faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox=55 +x1,162+y1,x2-x1,y2-y1
                imgbackground=cvzone.cornerRect(imgbackground,bbox,rt=0)
                id=studentids[matchindex]
                # print(id)

                if counter==0:
                    cvzone.putTextRect(imgbackground,"loading...",(275,600))
                    cv2.imshow("Attendance System",imgbackground)
                    cv2.waitKey(1)
                    counter=1
                    modetype=1


        if counter!=0:
            if counter==1:
                # get the data
                studentinfo=db.reference(f'Students/{id}').get()
                print(studentinfo)
                # get the image from storage
                blob=bucket.get_blob(f"C:/Users/HP/Downloads/my codes/images/{id}.jpg")
                array=np.frombuffer(blob.download_as_string(),np.uint8 )
                imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # update attendance
                datetimeobject=datetime.strptime(studentinfo['last_attendance_time'],
                                                '%Y-%m-%d %H:%M:%S')
                secondelapsed=(datetime.now()-datetimeobject).total_seconds()
                print(secondelapsed)

                # time after which next attendance will be marked in sec is 30
                if secondelapsed>30:
                    ref=db.reference(f"Students/{id}")
                    studentinfo["Total_attendance"] +=1
                    ref.child("Total_attendance").set(studentinfo["Total_attendance"])
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modetype=3
                    counter=0
                    imgbackground[44:677,808:1222]=imgmodelist[modetype]
            
            if modetype!=3:


                if 10<=counter<=20:
                    modetype=2 

                imgbackground[44:677,808:1222]=imgmodelist[modetype]


                if counter <=10:
                    cv2.putText(imgbackground,str(studentinfo["Total_attendance"]),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    
                    cv2.putText(imgbackground,str(studentinfo["Major"]),(1006,550),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)  
                    cv2.putText(imgbackground,str(id),(1006,493),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1) 
                    cv2.putText(imgbackground,str(studentinfo["Standing"]),(910,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgbackground,str(studentinfo["Year"]),(1025,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1) 
                    cv2.putText(imgbackground,str(studentinfo["Starting_year"]),(1125,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)  
                    
                    # to shift name in centre of the screen
                    (w,h),_=cv2.getTextSize(studentinfo["Name"],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv2.putText(imgbackground,str(studentinfo["Name"]),(808+offset,445),
                                cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1) 
                        

                    imgbackground[175:175+216,909:909+216] =imgstudent  

                counter+=1

                if counter>=20:
                    counter=0
                    modetype=0
                    studentinfo=[]
                    imgstudent=[]
                    imgbackground[44:677,808:1222]=imgmodelist[modetype]
            

    else:
        modetype=0
        counter=0


    # cv2.imshow("Camera",img)
    cv2.imshow("Attendance System",imgbackground)
    if cv2.waitKey(1)==ord("c"):
        break