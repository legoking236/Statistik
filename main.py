"""
Statistik
v 0.5.18
(c) 2015 Alex Probst
"""

from Tkinter import *
from SummaryCalcs import *
from GraphingClasses import *
from DrawClass import Draw
import snake

window = Tk()
window.wm_title("Statistik")
window.configure(bg="gray")

L1 = []
L2 = []

DataSummSeld = "L1"
GraphDrawn = [False, None, None]

def SetDataSumm(self, self2, self3):
    global DataSummSeld
    Seld = DataListChooseVar.get()
    DataSummSeld = Seld
    summRecalc(DataSummSeld)
def summRecalc(listIdent):
    global DataSummSeld
    if listIdent == DataSummSeld:
        if listIdent == "L1":
            passData = L1
        else:
            passData = L2

        DataMax.configure(text="Max: " + str(maximum(passData)))
        DataMin.configure(text="Min: " + str(minimum(passData)))
        DataSx.configure(text=u"\u03C3" + ": " + str(stadard(passData)))
        DataXb.configure(text="x" + u"\u0305" + ": " + str(mean(passData)))
        DataMed.configure(text="Med: " + str(median(passData)))
        DataMode.configure(text="Mode: " + str(mode(passData)))
        DataQ1.configure(text="Q" + u"\u2081" + ": " + str(quar1(passData)))
        DataQ2.configure(text="Q" + u"\u2083" + ": " + str(quar3(passData)))
        DataIQR.configure(text="IQR: " + str(calIQR(passData)))
        DataRange.configure(text="Range: " + str(calRange(passData)))
    else:
        pass
def AddData():
    EntData = DataEntry.get()
    if EntData == "snake":
        DataEntry.delete(0, END)
        snake.snake(Graph)
        return 0
    elif EntData.lower() == "chuck norris":
        EntData = "42"
    DataArr = EntData.split(',')
    for x in range(0, len(DataArr)):
        DataArr[x] = float(DataArr[x])
    List = ListChooseVar.get()

    if List == "L1":
        for Data in DataArr:
            L1.append(Data)
            listOne.insert(END, Data)
            listOne.see(END)
        summRecalc("L1")
        if GraphDrawn[2] == "L1":
            GraphDrawn[1].reDraw(L1)
        elif GraphDrawn[2] == "BOTH":
            GraphDrawn[1].reDraw(L1, L2)
    else:
        for Data in DataArr:
            L2.append(Data)
            listTwo.insert(END, Data)
            listTwo.see(END)
        summRecalc("L2")
        if GraphDrawn[2] == "L2":
            GraphDrawn[1].reDraw(L2)
        elif GraphDrawn[2] == "BOTH":
            GraphDrawn[1].reDraw(L1, L2)

    DataEntry.delete(0, END)
def DelList(listIdent):
    if listIdent == "L1":
        try:
            selection = listOne.curselection()
            i = 0
            for x in range(0, len(selection)):
                L1.pop(selection[x-i])
                listOne.delete(selection[x-i])
                i+=1
            listOne.activate(listOne.nearest(selection[-1]-i))
            summRecalc("L1")
            if GraphDrawn[2] == "L1":
                GraphDrawn[1].reDraw(L1)
            elif GraphDrawn[2] == "BOTH":
                GraphDrawn[1].reDraw(L1, L2)
        except:
            pass
    else:
        try:
            selection = listTwo.curselection()
            i = 0
            for x in range(0, len(selection)):
                L2.pop(selection[x-i])
                listTwo.delete(selection[x-i])
                i+=1
            listTwo.activate(listTwo.nearest(selection[-1]-i))
            summRecalc("L2")
            if GraphDrawn[2] == "L2":
                GraphDrawn[1].reDraw(L2)
            elif GraphDrawn[2] == "BOTH":
                GraphDrawn[1].reDraw(L1, L2)
        except:
            pass
def AddDataOnPress(self):
    AddData()
def DelL2(self):
    DelList("L2")
def DelL1(self):
    DelList("L1")
def swichList(self):
    if DataSummSeld == "L1":
        ListChooseVar.set("L2")
    else:
        ListChooseVar.set("L1")
def ClrList1():
    L1 = []
    listOne.delete(0, END)
    summRecalc("L1")
def ClrList2():
    L2 = []
    listTwo.delete(0, END)
    summRecalc("L2")
def DrawBoxPlotWindow():
    Graph.delete("all")
    BoxPlotWindow = Toplevel()
    BoxPlotWindow.wm_title("Graph Box Plot")
    listUsed = "L1"
    def drawBox():
        GraphDrawn[1] = BoxPlot(Graph, L1, data2=L2, color="red", color2="blue")
        GraphDrawn[0] = True
        if len(L1) > 0 and len(L2) > 0:
            GraphDrawn[2] = "BOTH"
        else:
            GraphDrawn[2] = listUsed
    #FUCK THIS SHIT, FUCK IT ALL TO HELL, I WILL DO IT LATER
    #UNTIL THEN I'M GOING TO WATCH 7 EPISODES OF MAD MEN AND
    #SULK IN SELF PITY, FUCK YOU PYTHON

    tempButton = Button(BoxPlotWindow, text="Graph",
    command=drawBox).pack()
def DrawHistogramWindow():
    Graph.delete("all")
    HistogramWindow = Toplevel()
    HistogramWindow.wm_title("Graph Historgram")
    def drawHist():
        GraphDrawn[1] = Histogram(Graph, L1, color="red")
        GraphDrawn[0] = True
        GraphDrawn[2] = "L1"


    #Look at DrawBoxPlotWindow for why there is no interface

    tempButton = Button(HistogramWindow, text="Graph",
    command=drawHist).pack()

def DrawScatterPlotWindow():
    Graph.delete("all")
    ScatterPlotWindow = Toplevel()
    ScatterPlotWindow.wm_title("Graph Scatter Plot")
    def drawScatter():
        GraphDrawn[1] = ScatterPlot(Graph, L1, L2, color="red")
        GraphDrawn[0] = True
        GraphDrawn[2] = "BOTH"


    #Look at DrawBoxPlotWindow for why there is no interface

    tempButton = Button(ScatterPlotWindow, text="Graph",
    command=drawScatter).pack()

WindowLeft = Frame(window)
WindowRight = Frame(window, width=300 , height=655, bg="white")

Graph = Canvas(WindowLeft, width=640, height=640)
drawing = Draw(Graph)

TRframe = Frame(WindowRight)
labelFrame = Frame(TRframe)
ListOneTitle = Label(labelFrame, text="L1", width=20)
ListTwoTitle = Label(labelFrame, text="L2", width=20)
listFrame = Frame(TRframe)
listOne = Listbox(listFrame, height=25, selectmode=EXTENDED)
listTwo = Listbox(listFrame, height=25, selectmode=EXTENDED)

DataControls = Frame(WindowRight)
DataEntry = Entry(DataControls)
ListChooseVar = StringVar(window)
ListChooseVar.set("L1")
DataOpts = OptionMenu(DataControls, ListChooseVar, "L1", "L2")
DataAdd = Button(DataControls, text="Add", command=AddData)

DataSumm = LabelFrame(WindowRight, text="Data Summary:", width=295, height=170)
DataListChooseVar = StringVar(window)
DataListChooseVar.set("L1")
ListChoose = OptionMenu(DataSumm, DataListChooseVar, "L1", "L2")
DataFrame = Frame(DataSumm)
DataCol1 = Frame(DataFrame, width=147, height=150)
DataCol2 = Frame(DataFrame, width=147, height=150)
DataMax = Label(DataCol1, text="Max: N/A")
DataMin = Label(DataCol1, text="Min: N/A")
DataSx = Label(DataCol1, text=u"\u03C3" + ": N/A")
DataXb = Label(DataCol1, text="x" + u"\u0305" + ": N/A")
DataMed = Label(DataCol2, text="Med: N/A")
DataMode = Label(DataCol1, text="Mode: N/A")
DataQ1 = Label(DataCol2, text="Q" + u"\u2081" + ": N/A")
DataQ2 = Label(DataCol2, text="Q" + u"\u2083" + ": N/A")
DataIQR = Label(DataCol2, text="IQR: N/A")
DataRange = Label(DataCol2, text="Range: N/A")

WindowLeft.pack(side=LEFT, padx=5, pady=5)
WindowRight.pack(side=RIGHT, anchor=N)
WindowRight.pack_propagate(0)

Graph.pack()

TRframe.pack(anchor=N)
labelFrame.pack()
ListTwoTitle.pack(side=RIGHT)
ListOneTitle.pack(side=RIGHT)
listFrame.pack()
listTwo.pack(side=RIGHT)
listOne.pack(side=RIGHT)
listTwo.bind("<BackSpace>", DelL2)
listOne.bind("<BackSpace>", DelL1)

DataControls.pack()
DataEntry.pack(side=LEFT)
DataEntry.bind("<Return>", AddDataOnPress)
DataEntry.bind("<Alt_L>", swichList)
DataEntry.bind("<Alt_R>", swichList)
DataOpts.pack(side=LEFT)
DataAdd.pack(side=LEFT)

DataSumm.pack()
DataSumm.pack_propagate(0)
ListChoose.pack()
ListChoose.config(width=35)
DataListChooseVar.trace("w", SetDataSumm)
DataFrame.pack()

DataCol1.pack(side=LEFT)
DataCol1.pack_propagate(0)
DataCol2.pack(side=RIGHT)
DataCol2.pack_propagate(0)
DataMax.pack()
DataMin.pack()
DataSx.pack()
DataXb.pack()
DataMed.pack()
DataMode.pack()
DataQ1.pack()
DataQ2.pack()
DataIQR.pack()
DataRange.pack()

menubar = Menu(window)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open")
filemenu.add_command(label="Save")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear L1", command=ClrList1)
editmenu.add_command(label="Clear L2", command=ClrList2)
menubar.add_cascade(label="Edit", menu=editmenu)

graphmenu = Menu(menubar, tearoff=0)
graphmenu.add_command(label="Scatter Plot", command=DrawScatterPlotWindow)
graphmenu.add_command(label="Box Plot", command=DrawBoxPlotWindow)
graphmenu.add_command(label="Histogram", command=DrawHistogramWindow)
graphmenu.add_command(label="Stacked Bar Chart")
graphmenu.add_separator()
graphmenu.add_command(label="Clear Graph", command=lambda: Graph.delete("all"))
graphmenu.add_command(label="Edit Graph")
menubar.add_cascade(label="Graph", menu=graphmenu)

samplemenu = Menu(menubar, tearoff=0)
samplemenu.add_command(label="Simple Random Sample")
samplemenu.add_command(label="Stratified Random Sample")
samplemenu.add_separator()
samplemenu.add_command(label="Random Number(s)")
menubar.add_cascade(label="Sample", menu=samplemenu)

drawmenu = Menu(menubar, tearoff=0)
drawmenu.add_command(label="Pencil", command=drawing.pencil_tool)
drawmenu.add_command(label="Line", command=drawing.line_tool)
drawmenu.add_command(label="Rectangle", command=drawing.rectangle_tool)
drawmenu.add_command(label="Oval", command=drawing.oval_tool)
drawmenu.add_command(label="Text", command=drawing.text_tool)
drawmenu.add_separator()
drawmenu.add_command(label="Move", command=drawing.move_tool)
drawmenu.add_command(label="Erase", command=drawing.erase_tool)
drawmenu.add_command(label="Clear", command=lambda: Graph.delete("all"))
drawmenu.add_separator()
colormenu = Menu(drawmenu, tearoff=0)
colormenu.add_command(label="Red", command=lambda: drawing.changeColorVar("red"))
colormenu.add_command(label="Blue", command=lambda: drawing.changeColorVar("blue"))
colormenu.add_command(label="Green", command=lambda: drawing.changeColorVar("green"))
colormenu.add_command(label="Yellow", command=lambda: drawing.changeColorVar("yellow"))
colormenu.add_command(label="Pink", command=lambda: drawing.changeColorVar("pink"))
colormenu.add_command(label="Purple", command=lambda: drawing.changeColorVar("purple"))
colormenu.add_command(label="Grey", command=lambda: drawing.changeColorVar("grey"))
colormenu.add_command(label="Black", command=lambda: drawing.changeColorVar("Black"))
drawmenu.add_cascade(label="Color...", menu=colormenu)
drawmenu.add_command(label="ToolBox", command=drawing.tool_box)
menubar.add_cascade(label="Draw", menu=drawmenu)

calcmenu = Menu(menubar, tearoff=0)
calcmenu.add_command(label="Z-score")
calcmenu.add_command(label="Linear Regression Line")
menubar.add_cascade(label="Calculate", menu=calcmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Documentation")
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

#histTest = Histogram(Graph, [31,22,15,11,12,34,22,15,67,28,92,15,181,172,152,134,114])
#14.2,16.4,11.9,15.2,18.5,22.1,19.4,25.1,23.4,18.1,22.6,17.2
#215,325,185,332,406,522,412,614,544,421,445,408

window.mainloop()
