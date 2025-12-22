import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import csv
import numpy as np

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class Output:
    def __init__(self, root, frame):
        self = self
        self.frame = frame
        self.root = root
    def OutputFrame(self):
        width = 1280*.475-100
        height = 720 / 2
        notebook = ttk.Notebook(self.frame, width=width, height=height)

        weightsContentFrame = tk.Frame(notebook)
        weightsContentFrame.pack(fill='both', expand=True)

        errPercentFrame = tk.Frame(notebook)
        errPercentFrame.pack(fill='both', expand=True)

        notebook.add(weightsContentFrame, text='Weights')
        notebook.add(errPercentFrame, text='error%')
        notebook.pack(fill='both', expand=True)

        self.notebook = notebook
        
        self.errPercentFrame = errPercentFrame

        height = 600
        width = width
        weightsCanvas = tk.Canvas(weightsContentFrame, width=width, height=height)
        weightsScroll = tk.Scrollbar(weightsContentFrame, command=weightsCanvas.yview)
        weightsCanvas.config(yscrollcommand=weightsScroll.set, scrollregion=(0,0,width, 300))
        
        weightsFilterFrame = tk.Frame(weightsCanvas)
        weightsGraphFrame = tk.Frame(weightsCanvas)
        
        weightsCanvas.create_window(10, 10, anchor='nw', window=weightsGraphFrame)
        weightsCanvas.pack(side='left', fill='both', expand=True)
        weightsScroll.pack(side='right', fill='y')
        weightsFilterFrame.pack(side='left', fill='both', expand=True)
        weightsGraphFrame.pack(side='left', fill='both', expand=True)
        
        self.weightsContentFrame = weightsContentFrame
        self.weightsCanvas = weightsCanvas
        self.weightsGraphFrame = weightsGraphFrame

        output = dict()
        keys = []
        with open('sample_output_file_weights.txt', 'r') as datafile:
            plotting = csv.reader(datafile, delimiter='\t')
            count = 0;
            for row in plotting:
                for i in range(len(row)):
                    if count == 0:
                        output[row[i]] = [0]
                        keys.append(row[i])
                    elif count == 1:
                        output[keys[i]] = [float(row[i])]
                    else:
                        output[keys[i]].append(float(row[i]))
                count +=1;
        self.output = output
        self.weightsFilter = Output.GraphFilters(self, weightsFilterFrame, self.output)
        self.weightAxes = Output.MakeGraph(self, weightsGraphFrame, self.output, self.weightsFilter)
    
    def GraphFilters(self, frame, d):
        #create dict
        filterDict = dict()
        for k, v in d.items():
            filterDict[k] = tk.BooleanVar(value=True)
        row = 0
        for option, value in filterDict.items():
            check_button = tk.Checkbutton(frame, text=option, variable=value, command=lambda *args: 
                                          Output.UpdateAxes(self, self.weightAxes, d, filterDict))
            check_button.grid(column=0, row=row, sticky='NW')
            row += 1
        return filterDict

    def MakeGraph(self, frame, d, filter):
        
        # create a figure
        figure = Figure(figsize=(6, 24), dpi=100, layout='constrained')

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, frame)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, frame)

        # create axes
        axes = figure.add_subplot()
        self.figure = figure
        Output.UpdateAxes(self=self, axes=axes, d=d, filter=filter)

        figure_canvas.get_tk_widget()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return axes

    def UpdateAxes(self, axes, d, filter):
        axes.clear()
        keys = list(d.keys())
        x=[]
        for i in range(len(d[keys[0]])):
            x.append(i)

        maxVal = 0
        for k, v in d.items():
            if filter[k].get() == True:
                axes.plot(x, v, label=k)
                m = max(v)
                if m > maxVal:
                   maxVal = m
        axes.set(yticks=(np.arange(0.5, int(maxVal)+1, 0.5)))
        axes.set_ylim(ymin=0, ymax=int(maxVal)+1)
        axes.set_title('Test')
        axes.set_ylabel('Weights')
        axes.set_xlabel('Epoch')
        axes.legend(bbox_to_anchor=(0, -0.25),
                     loc='upper left', borderaxespad=0.)
        #self.figure.legend(loc='outside lower left', borderaxespad=0.)
        self.figure.canvas.draw()