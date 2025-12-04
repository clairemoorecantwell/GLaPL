import tkinter as tk
from tkinter import END, Entry, Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter import scrolledtext as scrolledtext
import GLaPLUtilities as util

class Console:
    self = None
    def __init__(self, root, frame):
        self = self
        self.frame = frame
        self.root = root

    def ConsoleFrame(self):
        
        # self.root.resize_widgets = (self.root.register(util.resize_widgets),'%P','%P','%P')

        # CONSOLE FRAME
        sticky = 'NSEW'
        maxColumn = 3
        maxRow = 1
        column = 3
        gridRow = 0
        width = 680
        consoleContainerFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.frame, maxColumn=maxColumn, columnSpan=3, 
                                                    maxRow=maxRow, column=column, row=gridRow, sticky=sticky, pady = 5, height=680))

        sticky = 'NW'
        maxColumn = 1
        maxRow = 1
        column = 0
        gridRow = 0
        height = 80
        consoleFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=consoleContainerFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=column, row=gridRow, sticky=sticky, width=width, height=height))

        self.consoleNotebook = ttk.Notebook(consoleFrame)
        self.consoleNotebook.pack(fill='both', expand=True)
        self.consoleNotebook.pressed_index = None

        sticky = 'NW'
        maxColumn = 8
        maxRow = 1
        column = 1
        gridRow = 0
        sizex = 630
        sizey = 280
        width = 630
        height = 280
    
        #Creating child frames
        self.progressFrame = tk.Frame(master=self.consoleNotebook)
        self.progressFrame.pack(fill='both', expand=True)

        self.historyFrame = tk.Frame(master=self.consoleNotebook)
        self.historyFrame.pack(fill='both', expand=True)

        #Adding notebook tabs
        self.consoleNotebook.add(self.progressFrame, text='Progress')
        self.consoleNotebook.add(self.historyFrame, text='History')

        #Creating canvases
        self.progressCanvas = tk.Canvas(self.progressFrame, width=width, height=height)
        self.progressScroll = tk.Scrollbar(self.progressFrame, command=self.progressCanvas.yview)
        self.progressCanvas.config(yscrollcommand=self.progressScroll.set, scrollregion=(0,0,width, 300))
        self.progressCanvas.pack(side='left', fill='both', expand=True)
        self.progressScroll.pack(side='right', fill='y')

        self.historyCanvas = tk.Canvas(self.historyFrame, width=width, height=height)
        self.historyScroll = tk.Scrollbar(self.historyFrame, command=self.historyCanvas.yview)
        self.historyCanvas.config(yscrollcommand=self.historyScroll.set, scrollregion=(0,0,width, 300))
        self.historyCanvas.pack(side='left', fill='both', expand=True)
        self.historyScroll.pack(side='right', fill='y')

        #Creating frames that live inside the canvas
        self.progressFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.progressCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.progressFrame.bind('<Enter>', lambda event, canvas=self.progressCanvas: util.onMouseWheel(canvas, event=event))
        self.progressCanvas.create_window(10, 10, anchor='nw', window=self.progressFrame, tags='progress_frame')
        #self.progressCanvas.bind("<Configure>", lambda *event, canvas=self.progressCanvas: util.resize_widgets(event = event, canvas= canvas, tag = 'progress_frame', width=event, height=event.height))

        self.historyFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.historyCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.historyFrame.bind('<Enter>', lambda event, canvas=self.historyCanvas: util.onMouseWheel(canvas, event=event))
        self.historyCanvas.create_window(0, 0, anchor='nw', window=self.historyFrame, tags=("history_frame",))
        #self.historyCanvas.bind("<Configure>", lambda *event, canvas=self.historyFrame: util.resize_widgets(event = event, canvas= canvas, tag = 'history_frame', width=event.width, height=event.height))

        self.historyText = scrolledtext.ScrolledText(self.historyFrame, width = width, height = height, wrap=tk.WORD)
        self.historyText.grid(column=0, row=0, pady=10, padx=10)
        self.historyText.config(state = 'disabled')

    def updateConsole(self, m):
        print(m)
        self.historyText.config(state = 'normal')
        self.historyText.insert(tk.INSERT, m+'\n')
        self.historyText.config(state = 'disabled')