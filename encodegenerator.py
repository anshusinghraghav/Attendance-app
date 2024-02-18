import cv2
import face_recognition
import os
import pickle 


# importing student images 
folderpath="C:/Users/HP/Downloads/my codes/images"
pathlist=os.listdir(folderpath)
print(pathlist)
imglist=[]
studentid=[]

for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
   
    studentid.append(os.path.splitext(path)[0])

# print(path)
# print(os.path.splitext(path)[0])
print(studentid)


def findencodeings(imageslist):
    encodelist=[]

# we loop through all the images and encode every single image
    # steps to encode img
    # 1-change the color(to make sure we r going from BGR to RGB)bcz that is what
    # lib uses so opencv uses bgr,the face recognition libray uses rgb
    # 2-find encodeings
    for img in imageslist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        # putting the encoding in list
        encodelist.append(encode)

    return encodelist    

print("encoding started....")

encodelistknown=findencodeings(imglist)
encodelistknownwithid=[encodelistknown,studentid]
# print(encodelistknown)
print("encoding complete")

file=open("encodefile.p ",'wb')
pickle.dump(encodelistknownwithid,file)
file.close()

print("file saved")




