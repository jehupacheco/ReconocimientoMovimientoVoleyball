import cv2
import imageio
import imutils
import numpy as np
import csv
from bagfeatures import bagOfFeatures
from constants import CSV_DELIMITER

# HOG descriptor
winSize = (16,16)
blockSize = (8,8)
blockStride = (4,4)
cellSize = (8,8)
nbins = 9
derivAperture = 1
winSigma = -1.
histogramNormType = 0
L2HysThreshold = 0.2
gammaCorrection = 1
nlevels = 64
signedGradients = True

class HogFeatureExtractor:
    def __init__(self, videofilename):
        self.hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, signedGradients)
        self.rgbFeatures = []
        self.videofilename = videofilename

    def extractFeatures(self):
        video = imageio.get_reader(self.videofilename, 'ffmpeg')
        for i, image in enumerate(video):
            crop = image[:,660:1260]
            resized = imutils.resize(crop, width=min(64, crop.shape[1]))
            rgbHog = self.hog.compute(resized)
            self.rgbFeatures.append(rgbHog.flatten())

    def getFeatures(self):
        features = np.matrix(self.rgbFeatures)
        shape = features.shape
        return bagOfFeatures(shape[1], features.reshape((shape[0]*shape[1], 1)))
