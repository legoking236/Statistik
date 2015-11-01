from Tkinter import *
from os import *
class Draw:
    def __init__(self, parent):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.identifier = None
        self.Master = parent
        self.ColorChooseVar = StringVar(parent)
        self.ColorChooseVar.set("Black")
        self.Toolbox_open = False
    def pencil_tool(self):
        #tool_name.config(text="Pencil: ")
        self.Master.unbind('<ButtonRelease-1>')
        self.Master.config(cursor="pencil")
        self.Master.bind('<Button-1>', self.obj_start)
        self.Master.bind('<B1-Motion>', self.draw)
    def line_tool(self):
        #tool_name.config(text="Line: ")
        self.Master.config(cursor="crosshair")
        self.Master.bind('<Button-1>', self.obj_start)
        self.Master.bind('<B1-Motion>', self.line_prev)
        self.Master.bind('<ButtonRelease-1>', self.line_end)
    def rectangle_tool(self):
        #tool_name.config(text="Rectangle: ")
        self.Master.config(cursor="crosshair")
        self.Master.bind('<Button-1>', self.obj_start)
        self.Master.bind('<B1-Motion>', self.rect_prev)
        self.Master.bind('<ButtonRelease-1>', self.rect_end)
    def oval_tool(self):
        #tool_name.config(text="Oval: ")
        self.Master.config(cursor="crosshair")
        self.Master.bind('<Button-1>', self.obj_start)
        self.Master.bind('<B1-Motion>', self.oval_prev)
        self.Master.bind('<ButtonRelease-1>', self.oval_end)
    def text_tool(self):
        #tool_name.config(text="Text: ")
        self.Master.unbind('<ButtonRelease-1>')
        self.Master.unbind('<B1-Motion>')
        self.Master.config(cursor="xterm")
        self.Master.bind('<Button-1>', self.text_draw)
    def erase_tool(self):
        #tool_name.config(text="Erase: ")
        self.Master.unbind('<B1-Motion>')
        self.Master.config(cursor="X_cursor")
        self.Master.bind('<Button-1>', self.erase_start)
        self.Master.bind('<ButtonRelease-1>', self.erase_end)
    def move_tool(self):
        #tool_name.config(text="Move: ")
        self.Master.unbind('<ButtonRelease-1>')
        self.Master.config(cursor="fleur")
        self.Master.bind('<Button-1>', self.move_start)
        self.Master.bind('<B1-Motion>', self.move_prev)
    def move_start(self, event):
        self.identifier = self.Master.find_closest(event.x, event.y)
        obj_cords = self.Master.coords(self.identifier)
        self.x0 = event.x
        self.y0 = event.y
    def move_prev(self, event):
        self.Master.move(self.identifier, -1*(self.x0-event.x), -1*(self.y0-event.y))
        self.x0 = event.x
        self.y0 = event.y
    def erase_start(self, event):
        self.identifier = self.Master.find_closest(event.x, event.y, halo=100)
    def erase_end(self, event):
        self.Master.delete(self.identifier)
    def obj_start(self, event):
        self.x0 = event.x
        self.y0 = event.y
    def line_prev(self, event):
        self.Master.delete('prev_line')
        self.Master.create_line(self.x0, self.y0, event.x, event.y, tag='prev_line', fill=self.ColorChooseVar.get())
    def line_end(self, event):
        self.Master.delete('prev_line')
        self.Master.create_line(self.x0, self.y0, event.x, event.y, fill=self.ColorChooseVar.get())
    def draw(self, event):
        self.Master.create_line(self.x0, self.y0, event.x, event.y, fill=self.ColorChooseVar.get())
        self.x0 = event.x
        self.y0 = event.y
    def rect_prev(self, event):
        self.Master.delete('prev_rect')
        self.Master.create_rectangle(self.x0, self.y0, event.x, event.y, tag='prev_rect', outline=self.ColorChooseVar.get())
    def rect_end(self, event):
        self.Master.delete('prev_rect')
        self.Master.create_rectangle(self.x0, self.y0, event.x, event.y, outline=self.ColorChooseVar.get())
    def oval_prev(self, event):
        self.Master.delete('prev_oval')
        self.Master.create_oval(self.x0, self.y0, event.x, event.y, tag='prev_oval', outline=self.ColorChooseVar.get())
    def oval_end(self, event):
        self.Master.delete('prev_oval')
        self.Master.create_oval(self.x0, self.y0, event.x, event.y, outline=self.ColorChooseVar.get())
    def text_draw(self, event):
        x = event.x
        y = event.y
        def ret_insert(event):
            text_to_insert = text.get()
            text_prompt.destroy()
            self.Master.create_text(x, y, text=text_to_insert, fill=self.ColorChooseVar.get())
        def insert():
            text_to_insert = text.get()
            text_prompt.destroy()
            self.Master.create_text(x, y, text=text_to_insert, fill=self.ColorChooseVar.get())
        text_prompt = Toplevel()
        text_prompt.title("Text:")
        text = Entry(text_prompt, width=20)
        btn_insert = Button(text_prompt, text="Insert", command=insert)
        text.pack()
        text.focus()
        text.bind('<Return>', ret_insert)
        btn_insert.pack()
    def changeColorVar(self, color):
        self.ColorChooseVar.set(color)
    def tool_box(self):
        if self.Toolbox_open == True:
            global toolBoxWindow
            toolBoxWindow.lift()
            return None
        def closeBox():
            self.Toolbox_open = False
            toolBoxWindow.destroy()
        toolBoxWindow = Toplevel()
        toolBoxWindow.wm_title("")
        tool_box = Frame(toolBoxWindow, relief=RAISED)
        tool_label = Label(tool_box, text="Toolbox:")
        button_box = Frame(tool_box)
        btn_pencil = Button(button_box, text=u"\u270E", command=self.pencil_tool)
        btn_line = Button(button_box, text=u"\u2571", command=self.line_tool)
        btn_rectangle = Button(button_box, text=u"\u25AD", command=self.rectangle_tool)
        btn_oval = Button(button_box, text=u"\u25EF", command=self.oval_tool)
        btn_text = Button(button_box, text=u"\uFF34", command=self.text_tool)
        btn_delete = Button(button_box, text=u"\u232B", command=self.erase_tool)
        btn_move = Button(button_box, text=u"\u2194", command=self.move_tool)
        ChooseFrame = Frame(tool_box)
        chooseColor = OptionMenu(ChooseFrame, self.ColorChooseVar, "Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Grey", "Black")

        tool_box.pack(side=LEFT, anchor=N, padx=2)
        tool_label.pack()
        button_box.pack()
        btn_pencil.grid(row=0, column=0)
        btn_line.grid(row=0, column=1)
        btn_rectangle.grid(row=1, column=0)
        btn_oval.grid(row=1, column=1)
        btn_text.grid(row=2, column=0)
        btn_delete.grid(row=2, column=1)
        btn_move.grid(row=3, column=0)
        ChooseFrame.pack()
        chooseColor.pack()
        self.Toolbox_open = True
        toolBoxWindow.protocol('WM_DELETE_WINDOW', closeBox)
