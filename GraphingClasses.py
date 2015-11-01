import SummaryCalcs
import math

class ScatterPlot:
    def __init__(self, master, data, master_size=[640, 640], color="black", bufferZone=[20, 20]):
        self.parent= master
        self.parent_size = master_size
        self.color = color
        self.bufferZone = bufferZone
        self.data = data
class BoxPlot:
    def __init__(self, master, data, data2=[], master_size=[640, 640], color="black", color2="black", bufferZone=[20, 20]):
        self.parent = master
        self.master_size = master_size
        self.color = color
        self.color2 = color2
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
        # min & max
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
class Histogram:
    def __init__(self, master, data, master_size=[640, 640], color="black", bufferZone=[20, 20]):
        self.parent= master
        self.parent_size = master_size
        self.color = color
        self.bufferZone = bufferZone
        self.data = data

class StackedBar:
    def __init__(self, master, data, master_size=[640, 640], color="black", bufferZone=[20, 20]):
        self.parent= master
        self.parent_size = master_size
        self.color = color
        self.bufferZone = bufferZone
        self.data = data
