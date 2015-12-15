"""
Statistik
v 0.5.18
(c) 2015 Alex Probst
"""

import SummaryCalcs
import math

class ScatterPlot:
    def __init__(self, master, data, data2, master_size=[640, 640], color="red", axisColor="black", bufferZone=[20, 20], LSRL=True):
        self.parent = master
        self.master_size = master_size
        self.color = color
        self.axisColor = axisColor
        self.bufferZone = bufferZone
        self.dataX = []
        for item in data:
            self.dataX.append(item)
        self.dataY = []
        for item in data2:
            self.dataY.append(item)
        if len(self.dataX) > len(self.dataY):
            diff = len(self.dataX) - len(self.dataY)
            for i in range(0, diff):
                self.dataY.append(0)
        elif len(self.dataX) < len(self.dataY):
            diff = len(self.dataY) - len(self.dataX)
            for i in range(0, diff):
                self.dataX.append(0)
        self.scaleX = self.calcScale('x')
        self.scaleY = self.calcScale('y')
        self.LSRL = LSRL
        self.drawPlot()
        if self.LSRL:
            self.LineOfBestFit()
    def calcScale(self, scale):
        if scale == 'x':
            Xrange = SummaryCalcs.maximum(self.dataX)
            if Xrange == 0:
                return 1
            return (self.master_size[0]-self.bufferZone[0]*2)/Xrange
        else:
            Yrange = SummaryCalcs.maximum(self.dataY)
            if Yrange == 0:
                return 1
            return (self.master_size[1]-self.bufferZone[1]*2)/Yrange
    def drawPlot(self):
        #draw axis
        self.parent.create_line(self.bufferZone[0], self.master_size[1]-(self.bufferZone[1]), self.master_size[0]-(self.bufferZone[0]), self.master_size[1]-(self.bufferZone[1]), fill=self.axisColor)
        self.parent.create_line(self.bufferZone[0], self.master_size[1]-(self.bufferZone[1]), self.bufferZone[0], self.bufferZone[1])

        for i in range(0, len(self.dataX)):
            Xcord = (self.bufferZone[0]) + (self.dataX[i] * self.scaleX)
            Ycord = (self.master_size[1] - self.bufferZone[1]) - (self.dataY[i] * self.scaleY)
            self.parent.create_rectangle(int(Xcord)-2, int(Ycord)-2, int(Xcord)+2, int(Ycord)+2, outline=self.color, fill=self.color)
    def reDraw(self, newData, newData2):
        self.dataX = []
        for item in newData:
            self.dataX.append(item)
        self.dataY = []
        for item in newData2:
            self.dataY.append(item)
        self.scaleX = self.calcScale('x')
        self.scaleY = self.calcScale('y')
        if len(self.dataX) > len(self.dataY):
            diff = len(self.dataX) - len(self.dataY)
            for i in range(0, diff):
                self.dataY.append(0)
        elif len(self.dataX) < len(self.dataY):
            diff = len(self.dataY) - len(self.dataX)
            for i in range(0, diff):
                self.dataX.append(0)
        self.parent.delete("all")
        self.drawPlot()
        if self.LSRL:
            self.LineOfBestFit()
    def LineOfBestFit(self):
        xBar = SummaryCalcs.mean(self.dataX)
        yBar = SummaryCalcs.mean(self.dataY)
        bigEQtop = 0
        bigEQbottom = 0
        for i in range(0, len(self.dataX)):
            xEQ = self.dataX[i] - xBar
            bigEQtop += (xEQ * (self.dataY[i] - yBar))
            bigEQbottom += (xEQ * xEQ)
        self.LBslope = bigEQtop / bigEQbottom
        self.Bval = yBar - (self.LBslope * xBar)

        print "y = " + str(round(self.LBslope,3)) + "x+" + str(round(self.Bval,3))
        self.drawLB()
    def drawLB(self):
        xSize = (self.master_size[0] - (self.bufferZone[0]*2))
        Ystart = (self.master_size[1] - self.bufferZone[1]) - (self.Bval * self.scaleY)
        Xstart = self.bufferZone[0]

        Yend = (self.master_size[1] - self.bufferZone[1]) - (self.LBslope * (xSize/self.scaleX) + self.Bval)
        Xend = xSize

        self.parent.create_line(Xstart, Ystart, Xend, Yend, fill="blue")
class BoxPlot:
    def __init__(self, master, data, data2=[], master_size=[640, 640], color="black", color2="black", axisColor="black", bufferZone=[20, 20]):
        self.parent = master
        self.master_size = master_size
        self.color = color
        self.color2 = color2
        self.axisColor = axisColor
        self.bufferZone = bufferZone
        self.bufferZone2 = [bufferZone[0], bufferZone[1]+70]
        self.data = data
        if len(data2) > 0:
            self.data2 = data2
            self.doubleBox = True
            self.min2 = SummaryCalcs.minimum(self.data2)
            self.q12 = SummaryCalcs.quar1(self.data2)
            self.mean2 = SummaryCalcs.mean(self.data2)
            self.q32 = SummaryCalcs.quar3(self.data2)
            self.max2 = SummaryCalcs.maximum(self.data2)
        else:
            self.doubleBox = False
        self.min = SummaryCalcs.minimum(self.data)
        self.q1 = SummaryCalcs.quar1(self.data)
        self.mean = SummaryCalcs.mean(self.data)
        self.q3 = SummaryCalcs.quar3(self.data)
        self.max = SummaryCalcs.maximum(self.data)
        self.scale = self.calcScale()
        if self.doubleBox:
            if self.min - self.min2 > 0:
                self.lower = 1
            else:
                self.lower = 2
            if self.max - self.max2 > 0:
                self.higher = 1
            else:
                self.higher = 2

        self.draw_plot()
    def draw_plot(self):
        if self.doubleBox:
            if self.lower == 1:
                Min2Offset = int(self.min - self.min2) * self.scale
                Min1Offset = 0
            else:
                Min1Offset = int(self.min2 - self.min) * self.scale
                Min2Offset = 0
            if self.higher == 1:
                Max2Offset = int(self.max - self.max2) * self.scale
                Max1Offset = 0
            else:
                Max1Offset = int(self.max2 - self.max) * self.scale
                Max2Offset = 0
        else:
            Min1Offset = 0
            Max1Offset = 0
        #draw axis
        self.parent.create_line(self.bufferZone[0]-5, self.master_size[1]-(self.bufferZone[1]-5), self.master_size[0]-(self.bufferZone[0]-5), self.master_size[1]-(self.bufferZone[1]-5), fill=self.axisColor)
        self.parent.create_line(self.bufferZone[0]-5, self.master_size[1]-(self.bufferZone[1]-5), self.bufferZone[0]-5, self.bufferZone[1]-5)
        # min & max
        self.parent.create_line(self.bufferZone[0] + Min1Offset, self.master_size[1] - (self.bufferZone[1]+50), self.bufferZone[0]+Min1Offset, self.master_size[1] - self.bufferZone[1], fill=self.color)
        self.parent.create_line(self.master_size[0] - (self.bufferZone[0] + Max1Offset), self.master_size[1] - (self.bufferZone[1]+50), self.master_size[0] - (self.bufferZone[0] + Max1Offset), self.master_size[1] - self.bufferZone[1], fill=self.color)
        #lines to box
        self.parent.create_line(self.bufferZone[0] + Min1Offset, self.master_size[1] - (self.bufferZone[1]+25), (self.bufferZone[0] + Min1Offset)+(self.scale * (self.q1 - self.min)), self.master_size[1] - (self.bufferZone[1]+25), fill=self.color)
        self.parent.create_line(self.master_size[0] - (self.bufferZone[0] + Max1Offset), self.master_size[1] - (self.bufferZone[1]+25),
        (self.master_size[0] - (self.bufferZone[0]+Max1Offset))-(self.scale * (self.max - self.q3)), self.master_size[1] - (self.bufferZone[1]+25), fill=self.color)
        #box
        self.parent.create_rectangle((self.bufferZone[0]+Min1Offset)+(self.scale * (self.q1 - self.min)),
        self.master_size[1] - (self.bufferZone[1]+50),
        (self.master_size[0] - (self.bufferZone[0] + Max1Offset))-(self.scale * (self.max - self.q3)),
        self.master_size[1] - self.bufferZone[1], outline=self.color)
        #mean
        self.parent.create_line((self.bufferZone[0] + Min1Offset)+(self.scale * (self.mean-self.min)), self.master_size[1] - (self.bufferZone[1]+50),
        (self.bufferZone[0]+Min1Offset)+(self.scale * (self.mean-self.min)), self.master_size[1] - self.bufferZone[1], fill=self.color)

        if self.doubleBox:
            # min2 & max2
            self.parent.create_line(self.bufferZone2[0] + Min2Offset, self.master_size[1] - (self.bufferZone2[1]+50), self.bufferZone2[0] + Min2Offset, self.master_size[1] - self.bufferZone2[1], fill=self.color2)
            self.parent.create_line(self.master_size[0] - (self.bufferZone2[0] + Max2Offset), self.master_size[1] - (self.bufferZone2[1]+50), self.master_size[0] - (self.bufferZone2[0] + Max2Offset), self.master_size[1] - self.bufferZone2[1], fill=self.color2)
            #lines to box
            self.parent.create_line(self.bufferZone2[0] + Min2Offset, self.master_size[1] - (self.bufferZone2[1]+25), (self.bufferZone2[0] + Min2Offset)+(self.scale * (self.q12 - self.min2)), self.master_size[1] - (self.bufferZone2[1]+25), fill=self.color2)
            self.parent.create_line(self.master_size[0] - (self.bufferZone2[0] + Max2Offset), self.master_size[1] - (self.bufferZone2[1]+25),
            (self.master_size[0] - (self.bufferZone2[0] + Max2Offset))-(self.scale * (self.max2 - self.q32)), self.master_size[1] - (self.bufferZone2[1]+25), fill=self.color2)
            #box
            self.parent.create_rectangle((self.bufferZone2[0] + Min2Offset)+(self.scale * (self.q12 - self.min2)),
            self.master_size[1] - (self.bufferZone2[1]+50),
            (self.master_size[0] - (self.bufferZone2[0] + Max2Offset))-(self.scale * (self.max2 - self.q32)),
            self.master_size[1] - self.bufferZone2[1], outline=self.color2)
            #mean2
            self.parent.create_line((self.bufferZone2[0] + Min2Offset)+(self.scale * (self.mean2-self.min2)), self.master_size[1] - (self.bufferZone2[1]+50),
            (self.bufferZone2[0] + Min2Offset)+(self.scale * (self.mean2-self.min2)), self.master_size[1] - self.bufferZone2[1], fill=self.color2)
    def change_scale(self, newScale):
        self.scale = newScale
        self.draw_plot()
    def calcScale(self):
        draw_width = self.master_size[0] - self.bufferZone[0]*2
        if self.doubleBox:
            Data1Dist = self.max - self.min
            Data2Dist = self.max2 - self.min2

            Data1Scale = int(draw_width/Data1Dist)
            Data2Scale = int(draw_width/Data2Dist)

            if Data1Scale < Data2Scale:
                return Data1Scale
            else:
                return Data2Scale
        else:
            numDist = self.max - self.min
            return int(draw_width/numDist)
    def reDraw(self, newData, newData2=[]):
        self.data = newData
        if len(newData2) > 0:
            self.data2 = newData2
            self.doubleBox = True
            self.min2 = SummaryCalcs.minimum(self.data2)
            self.q12 = SummaryCalcs.quar1(self.data2)
            self.mean2 = SummaryCalcs.mean(self.data2)
            self.q32 = SummaryCalcs.quar3(self.data2)
            self.max2 = SummaryCalcs.maximum(self.data2)
        else:
            self.doubleBox = False
        self.min = SummaryCalcs.minimum(self.data)
        self.q1 = SummaryCalcs.quar1(self.data)
        self.mean = SummaryCalcs.mean(self.data)
        self.q3 = SummaryCalcs.quar3(self.data)
        self.max = SummaryCalcs.maximum(self.data)
        self.scale = self.calcScale()
        if self.doubleBox:
            if self.min - self.min2 > 0:
                self.lower = 1
            else:
                self.lower = 2
            if self.max - self.max2 > 0:
                self.higher = 1
            else:
                self.higher = 2
        self.parent.delete("all")
        self.draw_plot()
class Histogram:
    def __init__(self, master, data, master_size=[640, 640], color="red", axisColor="black", bufferZone=[20, 20]):
        self.parent= master
        self.master_size = master_size
        self.color = color
        self.axisColor = axisColor
        self.bufferZone = bufferZone
        self.data = data
        self.FindBinWidth()
        self.dataCounted = self.countData()
        self.scaleX = self.calcScale('x')
        self.scaleY = self.calcScale('y')
        self.drawGraph()
    def FindBinWidth(self):
        dataMin = int(SummaryCalcs.minimum(self.data))
        dataMax = int(SummaryCalcs.maximum(self.data))
        dataRange = dataMax - dataMin
        binWidth = 1
        if dataRange <= 10:
            maxBins = 3
            binInc = 1
        else:
            maxBins = 10
            binInc = 5
        numToDiv = int(dataRange/binWidth)
        while numToDiv > maxBins:
            binWidth += binInc
            numToDiv = int(dataRange/binWidth)
        self.binWidth = binWidth
        #generate bin array
        binArray = []
        binVal = 0
        while (len(binArray) == 0) or (binArray[-1] <= dataMax):
            if len(binArray) == 0:
                if binVal <= dataMin < binVal+binWidth:
                    binArray.append(binVal)
                    binVal += binWidth
                else:
                    binVal += binWidth
            else:
                binArray.append(binVal)
                binVal += binWidth
        self.binArray = binArray
    def countData(self):
        countedData = []
        index = 0
        for binNum in self.binArray:
            binNumCount = 0
            for num in self.data:
                if ((index == len(self.binArray)-1) and (binNum < num)) or (binNum <= num < self.binArray[index+1]):
                    binNumCount += 1
                else:
                    continue
            countedData.append(binNumCount)
            index += 1
        return countedData
    def calcScale(self, axis):
        if axis == 'x':
            masterSizeXwoBuffer = self.master_size[0] - self.bufferZone[0]*2
            scaleX = masterSizeXwoBuffer / len(self.binArray)
            return scaleX
        else:
            masterSizeYwoBuffer = self.master_size[1] - self.bufferZone[1]*2
            scaleY = masterSizeYwoBuffer / SummaryCalcs.maximum(self.dataCounted)
            return scaleY
    def drawGraph(self):
        #draw bars
        index = 0
        while index < len(self.dataCounted)-1:
            if self.dataCounted[index] == 0:
                index+=1
            else:
                self.parent.create_rectangle((self.bufferZone[0]+self.scaleX*index), (self.master_size[1]-self.bufferZone[1])-(self.scaleY*self.dataCounted[index]), (self.bufferZone[0]+self.scaleX*(index+1)), self.master_size[1]-self.bufferZone[1], outline=self.color)
                index+=1
        #draw axis
        self.parent.create_line(self.bufferZone[0], self.master_size[1]-self.bufferZone[1], self.master_size[0]-self.bufferZone[0], self.master_size[1]-self.bufferZone[1], fill=self.axisColor)
        self.parent.create_line(self.bufferZone[0], self.master_size[1]-self.bufferZone[1], self.bufferZone[0], self.bufferZone[1])
        #draw scale marks on Y
        pixlesCoveredY = 0
        while pixlesCoveredY < self.master_size[1]-self.bufferZone[1]*2:
            self.parent.create_line(self.bufferZone[0], (self.master_size[1] - self.bufferZone[1]) - pixlesCoveredY, self.bufferZone[0]-5, (self.master_size[1] - self.bufferZone[1]) - pixlesCoveredY, fill=self.axisColor)
            pixlesCoveredY += self.scaleY
        #draw scale marks on X
        pixlesCoveredX = 0
        while pixlesCoveredX < self.master_size[0]-self.bufferZone[0]*2:
            self.parent.create_line(self.bufferZone[0] + pixlesCoveredX, self.master_size[1]-self.bufferZone[1], self.bufferZone[0] + pixlesCoveredX, self.master_size[1]-(self.bufferZone[1]-5), fill=self.axisColor)
            pixlesCoveredX += self.scaleX
    def reDraw(self, newData):
        self.data = newData
        self.binWidth = self.FindBinWidth()
        self.dataCounted = self.countData()
        self.scaleX = self.calcScale('x')
        self.scaleY = self.calcScale('y')
        self.parent.delete("all")
        self.drawGraph()

class StackedBar:
    def __init__(self, master, data, master_size=[640, 640], color="black", bufferZone=[20, 20]):
        self.parent= master
        self.parent_size = master_size
        self.color = color
        self.bufferZone = bufferZone
        self.data = data
