import csv
from constants import *

class ReadData:
    def __init__(self, filename, hasHeader=False):
        self.file = open(filename, newline='')
        self.reader = csv.reader(self.file, delimiter=CSV_DELIMITER)

        if hasHeader:
            next(self.reader)

    def readData(self, data):
        try:
            row = next(self.reader)
            self.fillData(data, row)
            return True
        except Exception as e:
            self.file.close()
            return False

    def fillData(self, data, row):
        for i in range(JOINT_NUM):
            data[i] = [float(x) for x in row[i].lstrip().split(' ')]