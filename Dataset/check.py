import os
import pandas as pd
import cv2

for (_, _, filenames) in os.walk('Data/skeleton'):
  for f in filenames:
    name = f.split('.')[0]

    try:
      data = pd.read_csv('Data/skeleton/' + f, header=None)
    except:
      print(name)
      continue

    cap = cv2.VideoCapture('Data/rgb/' + name + '.avi')
    fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps != data.shape[0]:
      print(name)

