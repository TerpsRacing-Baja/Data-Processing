import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Time interval between sampling in milliseconds 

class rpmData:
    '''
        Will be adding other functionality hopefully
    '''
    def __init__(self) -> None:
        # Time interval between sampling in milliseconds 
        self.dt = 20
        # Input data file path to be read from
        self.inputFile = "fall2023RPM/rpm_manual_only_voltage.csv"
        # Dataframe for easy access
        self.dataframe = pd.read_csv("fall2023RPM/rpm_manual_only_voltage.csv")
    '''
        @param
        @return None
    '''
    def getCleanedRPM(self, outputFile: str) -> None:
        # Initializes variables
        if (os.path.exists(outputFile)):
            raise FileExistsError("outputFile path exists: choose a different path or delete such file")
        input = open(self.inputFile, "r")
        data = list(csv.reader(input, delimiter=","))
        input.close()
        output = open(outputFile, "w")
        outputWriter = csv.writer(output)

        # Writes column names 
        outputWriter.writerow(data[0])

        # Writes every row that satifies some condition; here, it is if Voltage has some value
        for d in data[1:]:
            if (d[1] != ''):
                outputWriter.writerow(d)
        
        output.close()

    # getCleanedRPM("fall2023RPM/rpm_manual_cleaned.csv", "fall2023RPM/rpm_manual_only_voltage.csv")
    # Even cleaner RPM file is in fall2023RPM/rpm_manual_only_voltage.csv

    '''
        @return float the average RPM
    '''
    def getAverageRPM(self, row1: int, row2: int) -> float:
        state = False # False if voltage is 0.5, True if 0.0
        switches = 0
        for voltage in self.dataframe.iloc[row1:row2, 1]:
            if (voltage == 0):
                if (not state):
                    switches += 1
                state = True
            else:
                state = False
        # (rotations / dt ms) * (ms / 0.001 s) * (60 s / 1 min)
        return switches / (self.dt * (row2 - row1)) * (1000 * 60)
    '''
        @param windowSize the range of rows to calculate moving average RPM 
        @return list(float) of RPM averages
    '''
    def getAverageRPMList(self, windowSize: int) -> tuple:
        totalRows = self.dataframe.shape[0]
        if (windowSize > totalRows):
            raise Exception("windowSize cannot be greater than number of rows")
        # Returns a list of ordered pairs: (window-median time, average RPM)
        # To separate average RPM from time?
        return ([self.dataframe.iloc[int(index + windowSize / 2), 0]    for index in range(0, totalRows - windowSize)],
                [self.getAverageRPM(index, index + windowSize) for index in range(0, totalRows - windowSize)])
    '''
        The idea is that from the average RPM step function, we can assign each 
        line segment a RPM value, a mid-point value, and a weight value for 
        interpolation. Smaller segments have less weight and vice versa. 
    '''
    def getWeightedPointsFromStepFunction(x: list(float), y: list(float)) -> tuple:
        totalPoints = len(x)
        pointsCounter = 0.0
        currentXValue = x[0]
        currentYValue = y[0]
        xValues = []
        yValues = [currentYValue]
        weights = []
        for dx, dy in zip(x, y):
            if (dy != currentYValue):
                #####
                currentYValue = dy
                yValues.append(currentYValue)
                weights.append(pointsCounter / totalPoints)
                pointsCounter = 0.0
            else:
                pointsCounter += 1

# x, y = rpmData().getAverageRPMList(10)
# plt.plot(x, y)
# x, y = rpmData().getAverageRPMList(50)
# plt.plot(x, y)
# x, y = rpmData().getAverageRPMList(100)
# plt.plot(x, y)
'''
The following currently returns a list whose first value is 
(500 samples / 2) * 20 ms => 5 seconds forwards from the dataset
'''
x, y = rpmData().getAverageRPMList(500)
plt.plot(x, y)
plt.show()