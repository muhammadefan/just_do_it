import face_recognition
import cv2
import os
import numpy as np
import csv
from datetime import datetime

# path to dataset
path = 'E:/PROJECT/py/att_recognition/data/'

images = []
att_name = []
data_train = os.listdir(path)

# read multiple images
for img in data_train:
  data = cv2.imread(path+img)
  images.append(data)
  # save image class name
  att_name.append(os.path.splitext(img)[0])

# encode the data
def data_encoding(images):
  encoded_list=[]
  for i in images:
    # convert images to RGB
    img_cvt = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    # encode the images, then save
    encoded = face_recognition.face_encodings(i)[0]
    encoded_list.append(encoded)
  return encoded_list

# if the csv file already created, skip below code
if not os.path.exists('attendant-record.csv'):
	with open('attendant-record.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(['name','date'])

# record attendant name and arrival time
def attendance_record(name):
	with open('attendant-record.csv', 'r+') as f:
		r_line = f.readlines()
		att_list = []
		for r in r_line:
			attribute = r.split(',')
			att_list.append(attribute[0])

		if name not in att_list:
			now = datetime.now()
			time = now.strftime('%H:%M:%S')
			f.writelines(f'{name},{time}\n')

# execute the function
encoded_list = data_encoding(images)

# launch webcam
cap = cv2.VideoCapture(0)
while True:
  s, img = cap.read()
  img_process = cv2.resize(img, (0,0), None, 0.25, 0.25)
  img_process = cv2.cvtColor(img_process, cv2.COLOR_BGR2RGB)

  img_floc = face_recognition.face_locations(img_process)
  img_encoded = face_recognition.face_encodings(img_process, img_floc)

  for floc,enc in zip(img_floc, img_encoded):
    match = face_recognition.compare_faces(encoded_list, enc)
    face_dis = face_recognition.face_distance(encoded_list, enc)
    match_idx = np.argmin(face_dis)

    if match[match_idx]:
      name = att_name[match_idx]
      print(name)
      # coordinate of bounding box
      y1,x2,y2,x1 = floc
      y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
      # create bounding box
      cv2.rectangle(img, (x1,y1), (x2,y2), (255,255,0), 2)
      cv2.rectangle(img, (x1,y2-35), (x2,y2), (255,255,0), cv2.FILLED)
      cv2.putText(img, name, (x1,y2-7), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
      # store data into csv file
      attendance_record(name)

  # to open the window (camera capture)
  cv2.imshow('real-time detection', img)
  # to close the window
  if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
    cap.release()
    break