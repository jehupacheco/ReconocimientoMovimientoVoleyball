import csv
# import os
import numpy as np
from read import ReadData
from features import Features
from hog import HogFeatureExtractor
from constants import *

root = '../Data/0512164529'

infilename = root + '/0512164529.csv'
outfilename = root + '/features.csv'

data = [[] for i in range(JOINT_NUM)]
outfile = open(outfilename, 'w', newline='')
writer = csv.writer(outfile, delimiter=CSV_DELIMITER)

reader = ReadData(infilename, hasHeader=True)

skeletonFeatures = Features()
while reader.readData(data):
    skeletonFeatures.extractFeatures(data)

skeletonFeatures.endExtraction()

(angles, velocities, frames) = skeletonFeatures.getFeatures()

# print(frames)

imageFeatures = HogFeatureExtractor(root, frames)
imageFeatures.extractFeatures()
(depth, rgb) = imageFeatures.getFeatures()

writer.writerow(np.concatenate((angles, velocities)))
outfile.close()

# os.system('libreoffice --calc {0} &'.format(outfilename))
# writer.writerow(np.concatenate((angles, velocities, depth, rgb)))
