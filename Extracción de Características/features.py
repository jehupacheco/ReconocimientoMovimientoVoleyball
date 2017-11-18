import math
import numpy as np
import graphHelper
from functools import reduce
from constants import *
from bagfeatures import bagOfFeatures

class Features:
    def __init__(self):
        # self.file = open(filename, 'w', newline='')
        # self.writer = csv.writer(self.file, delimiter=CSV_DELIMITER)
        # Angle features variables
        self.articulations = graphHelper.arts(CONEXION_GRAPH)
        self.angles = np.array([])
        # Velocity feature variables
        self.pastPositions = [[0.0, 0.0, 0.0] for i in VELOCITY_JOINTS]
        # self.velocities = [[0.0, 0.0, 0.0] for i in VELOCITY_JOINTS]
        self.velocities = [0.0 for i in VELOCITY_JOINTS]
        self.currentFrame = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.endExtraction()

    def extractFeatures(self, data):
        self.angles = np.concatenate((self.angles, np.array(self.getArticulationsAngles(data))))
        # print('Data: {0} Pos: {1}'.format(len(data), len(self.pastPositions)))
        self.getVelocities(data)

    def getArticulationsAngles(self, data):
        return [self.getAngleInArticulation(data, art) for art in self.articulations]

    def getAngleInArticulation(self, data, articulation):
        points = [np.array(data[p]) for p in articulation]
        ab = points[1] - points[0]
        bc = points[2] - points[1]
        cosineAngle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
        angle = np.arccos(cosineAngle)

        return np.degrees(angle)

    def getVelocities(self, data):
        if self.currentFrame > 0:
            difference = [[data[VELOCITY_JOINTS[i]][j] - self.pastPositions[i][j] for j in range(3)] for i in range(len(VELOCITY_JOINTS))]
            velocities = [np.linalg.norm(np.array([x/FRAME_TIME for x in d])) for d in difference]
            self.velocities = [self.velocities[i] + velocities[i] for i in range(len(velocities))]

        self.currentFrame += 1
        self.pastPositions = [data[i] for i in VELOCITY_JOINTS]

    def endExtraction(self):
        self.averageVelocities = np.array([v/(self.currentFrame-1) for v in self.velocities])

    def getFeatures(self):
        shape = self.angles.shape
        return (
            bagOfFeatures(len(self.articulations),self.angles.reshape((shape[0], 1))),
            self.averageVelocities,
            self.currentFrame
        )
