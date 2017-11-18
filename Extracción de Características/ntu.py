import argparse
import csv
import zipfile
import graphHelper
import os
from constants import CSV_DELIMITER
from utils import extractFeatures, printProgress

datapath = '/home/a20122064/'
outpath = '/home/a20122064/'
zipname = 'nturgbd_skeletons.zip'
featuresFile = 'video+skeleton2.csv'
availableVideos = [1]

def getDataStats(filelist, movements):
    stats = {}

    for m in movements:
        stats[m] = 0

    for f in filelist:
        stats[f.split('.')[0].split('A')[1]] += 1

    print(stats)

def getVideosAvailable():
    videos = {}

    for index in availableVideos:
        zipvideo = zipnamevideo(index)
        with zipfile.ZipFile(datapath + zipvideo) as zip:
        # zip = zipfile.ZipFile(datapath + zipvideo)
            files = [file.split('/')[-1].split('_')[0] for file in zip.namelist() if file.split('/')[1] != '']

            for f in files:
                videos[f] = zipvideo

    return videos

def zipnamevideo(index):
    return 'nturgbd_rgb_s{0:03d}.zip'.format(index)

def getFiltered(zip, videosList):
    f = open('NTU Extractor/samples_with_missing_skeletons.txt')
    ignore = [x.strip() for x in f.readlines()]
    files = [file for file in zip.namelist() if file.split('/')[1] != '']
    movements = ['007', '009', '024', '027', '043']
    filtered = [f for f in files if f.split('.')[0].split('A')[1] in movements and f.split('/')[-1].split('.')[0] not in ignore and f.split('/')[-1].split('.')[0] in videosList]
    getDataStats(filtered, movements)

    return filtered

def getVideo(name, videolist):
    rname = name.split('/')[-1].split('.')[0]
    videopath = 'nturgb+d_rgb/{0}_rgb.avi'.format(rname)

    with zipfile.ZipFile(datapath + videolist[rname]) as zip:
        return zip.extract(videopath)

def skeletonCsvFile(zip, f, csvfilename):
    with zip.open(f, 'r') as file, open(csvfilename, 'w', newline='') as csvfile:
        frames = int(file.readline())
        writer = csv.writer(csvfile, delimiter=',')
        process = True
        for i in range(frames):
            nbodys = int(file.readline())
            bodyinfo = file.readline()
            joints = int(file.readline())
            positions = []

            if nbodys == 1:
                process = True
                for j in range(joints):
                    line = file.readline().decode().split(' ')
                    positions.append('{0} {1} {2}'.format(line[0], line[1], line[2]))

                writer.writerow(positions)
            else:
                process = False
                break

        return process

def main():
    with open(outpath + featuresFile, 'w', newline='') as outfile:
        zip = zipfile.ZipFile(datapath + zipname)
        featuresWriter = csv.writer(outfile, delimiter=CSV_DELIMITER)
        videosList = getVideosAvailable()
        filtered =  getFiltered(zip, list(videosList.keys()))
        printProgress(0, len(filtered), prefix = 'Progress:', suffix = '0/{0}'.format(len(filtered)), bar_length = 50)
    
        for index, f in enumerate(filtered):
            videopath = getVideo(f, videosList)
            csvfilename = outpath + f.split('/')[-1].split('.')[0] + '.csv'
            process = skeletonCsvFile(zip, f, csvfilename)

            if process:
                videoFeatures = extractFeatures(csvfilename, videopath)
                print('Total Shape: {}'.format(videoFeatures.shape))
                featuresWriter.writerow(videoFeatures.tolist() + [f.split('.')[0].split('A')[1].split('0')[-1]])

            os.remove(csvfilename)
            os.remove(videopath)
            printProgress(index+1, len(filtered), prefix = 'Progress:', suffix = '{0}/{1}'.format(index+1, len(filtered)), bar_length = 50)

if __name__ == "__main__":
    main()
