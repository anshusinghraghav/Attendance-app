import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import face_recognition
import os
import pickle 


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-app-1a0c6-default-rtdb.firebaseio.com/",
    'storageBucket':"attendance-app-1a0c6.appspot.com"
})

folderpath="C:/Users/HP/Downloads/my codes/images"
pathlist=os.listdir(folderpath)
print(pathlist)
imglist=[]
studentid=[]

for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
   
    studentid.append(os.path.splitext(path)[0])

    filename=f'{folderpath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)


