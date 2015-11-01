"""
Statistik
v 0.5.6
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
        #will play snake on the canvas
        pass
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
    else:
        for Data in DataArr:
            L2.append(Data)
            listTwo.insert(END, Data)
            listTwo.see(END)
        summRecalc("L2")

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
    stateR = False
    def change_state():
        if stateR:
            for child in windowFrameRight.winfo_children():
                child.configure(state="disable")
        else:
            for child in windowFrameRight.winfo_children():
                child.configure(state="enable")

    Graph.delete("all")
    BoxPlotWindow = Toplevel()
    BoxPlotWindow.wm_title("Graph Box Plot")
    TopFrame = Frame(BoxPlotWindow)
    TwoSetsVar = IntVar()
    TwoSets = Checkbutton(TopFrame, text="Double Box Plot?", variable=TwoSetsVar)

    sidesFrame = Frame(BoxPlotWindow)

    windowFrameLeft = Frame(sidesFrame)
    FL_dataList = Listbox(windowFrameLeft, height=5, width=20)
    for item in L1:
        FL_dataList.insert(END, item)
    FL_ColorChooseVar = StringVar()
    FL_ColorChooseVar.set("Red")
    FL_colorChooser = OptionMenu(windowFrameLeft, FL_ColorChooseVar, "Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Grey", "Black")
    windowFrameRight = Frame(sidesFrame)
    FR_dataList = Listbox(windowFrameLeft, height=5, width=20)
    for item in L2:
        FR_dataList.insert(END, item)
    FR_dataList.config(state="disable")
    FR_ColorChooseVar = StringVar()
    FR_ColorChooseVar.set("Blue")
    FR_colorChooser = OptionMenu(windowFrameLeft, FR_ColorChooseVar, "Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Grey", "Black")
    lowerFrame = Frame(BoxPlotWindow)

    TopFrame.pack()
    TwoSets.pack()
    sidesFrame.pack()
    windowFrameLeft.pack(side=LEFT)
    FL_dataList.pack()
    FL_colorChooser.pack()
    windowFrameRight.pack(side=RIGHT)
    FR_dataList.pack()
    FR_colorChooser.pack()
    lowerFrame.pack()

    TwoSetsVar.trace("w", change_state)
    tempButton = Button(BoxPlotWindow, text="Graph",
    command=lambda: BoxPlot(Graph, L1, data2=L2, color="red", color2="blue")).pack()

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
graphmenu.add_command(label="Scatter Plot")
graphmenu.add_command(label="Box Plot", command=DrawBoxPlotWindow)
graphmenu.add_command(label="Histogram")
graphmenu.add_command(label="Stacked Bar Chart")
graphmenu.add_separator()
graphmenu.add_command(label="Clear Graph", command=lambda: Graph.delete("all"))
graphmenu.add_command(label="Edit Graph")
menubar.add_cascade(label="Graph", menu=graphmenu)

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

#test1 = BoxPlot(Graph, [33,44,56,72,13,45,99,81,23,33,47,16,8], data2=[23,44,51,32,65,88,94,23,45,61,54,90,32], color="green", color2="red")
#test2 = BoxPlot(Graph, [33,44,56,72,13,45,99,81,23,33,47,16,8], data2=[33,44,56,72,13,45,99,81,23,33,47,16,8], color="green", color2="red")
window.mainloop()
