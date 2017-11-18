import os
import csv
import numpy as np
from constants import CSV_DELIMITER, CONEXION_GRAPH, VELOCITY_JOINTS
import graphHelper
from utils import transform, extractFeatures
# import numpy as np

# def getHeaders():
#     articulations = graphHelper.arts(CONEXION_GRAPH)
#     artHeaders = ['Angle {0}-{1}-{2}'.format(JOINTS[art[0]], JOINTS[art[1]], JOINTS[art[2]]) for art in articulations]
#     velHeaders = ['Velocity {0}'.format(JOINTS[j]) for j in VELOCITY_JOINTS]
#     return artHeaders + velHeaders + ['Class']


rootFolder = '/home/a20122064/data/TesisData'
featuresFile = '/features-real.csv'

with open(rootFolder + featuresFile, 'w', newline='') as outfile:
    for (_, _, filenames) in os.walk(rootFolder + '/skeleton'):
        writer = csv.writer(outfile, delimiter=CSV_DELIMITER)
        # writer.writerow(getHeaders())

        for f in filenames:
            print('... {0}'.format(f))
            videoFeatures = extractFeatures(rootFolder + '/skeleton/' + f, '')
            classname = f.split('A')[0].split('0')[-1]
            # classname = f.split('.')[0].split('A')[-1].split('0')[-1]

        writer.writerow(videoFeatures.tolist() + [int(classname)])

os.system('libreoffice --calc {0} &'.format(rootFolder + featuresFile))

# rootFolder = '/media/alulab/Datos/Data/'
# descriptionFile = 'activityLabel.txt'
# classesFile = 'classes.csv'

# classes = []

# with open(rootFolder + descriptionFile, 'r', newline='') as file, open(rootFolder + featuresFile, 'w', newline='') as outfile:
#     reader = csv.reader(file, delimiter=CSV_DELIMITER)
#     writer = csv.writer(outfile, delimiter=CSV_DELIMITER)
#     writer.writerow(getHeaders())

#     for row in reader:
#         infile = '{0}{1}/{2}.txt'.format(rootFolder, row[0], row[0])
#         outfile = '{0}{1}/{2}.csv'.format(rootFolder, row[0], row[0])
#         transform(infile, outfile)

#         print('... {0}{1}/{2}.csv'.format(rootFolder, row[0], row[0]))
#         videoFeatures = extractFeatures('{0}{1}/{2}.csv'.format(rootFolder, row[0], row[0]))

#         index = 0

#         if row[1] in classes:
#             index = classes.index(row[1])
#         else:
#             index = len(classes)
#             classes.append(row[1])

#         writer.writerow(videoFeatures.tolist() + [index])

# with open(rootFolder + classesFile, 'w') as f:
#     for fclass in classes:
#         print(fclass, file=f)

# os.system('libreoffice --calc {0} &'.format(rootFolder + featuresFile))
