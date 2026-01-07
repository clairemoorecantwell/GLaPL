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
        height = 720/2
        notebook = ttk.Notebook(self.frame, width=width, height=height)

        weightsContentFrame = tk.Frame(notebook)
        weightsContentFrame.pack(fill='both', expand=True)

        errContentFrame = tk.Frame(notebook)
        errContentFrame.pack(fill='both', expand=True)

        notebook.add(weightsContentFrame, text='Weights')
        notebook.add(errContentFrame, text='error%')
        notebook.pack(fill='both', expand=True)

        self.notebook = notebook
        
        

        height = 900
        width = width
        weightsCanvas = tk.Canvas(weightsContentFrame, width=width, height=height)
        weightsScroll = tk.Scrollbar(weightsContentFrame, command=weightsCanvas.yview)
        weightsCanvas.config(yscrollcommand=weightsScroll.set, scrollregion=(0,0,width, 1200))
        weightsCanvas.pack(side='left', fill='both', expand=True)
        weightsScroll.pack(side='right', fill='y')
        weightsFrame = tk.Frame(weightsCanvas, width=width, height=600)
        weightsFrame.pack(fill='both', expand=True)
        weightsFilterFrame = tk.Frame(weightsFrame)
        weightsGraphFrame = tk.Frame(weightsFrame)
        
        weightsCanvas.create_window(10, 10, anchor='nw', window=weightsFrame)
        
        weightsFilterFrame.pack(side='top', fill='both', expand=True)
        weightsGraphFrame.pack(side='bottom', fill='both', expand=True)
        
        self.weightsFilterFrame = weightsFilterFrame
        self.weightsGraphFrame = weightsGraphFrame
        self.weightsContentFrame = weightsContentFrame
        self.weightsCanvas = weightsCanvas
        self.weightsGraphFrame = weightsGraphFrame


        errCanvas = tk.Canvas(errContentFrame, width=width, height=height)
        errScroll = tk.Scrollbar(errContentFrame, command=errCanvas.yview)
        errCanvas.config(yscrollcommand=errScroll.set, scrollregion=(0,0,width, 600))
        errCanvas.pack(side='left', fill='both', expand=True)
        errScroll.pack(side='right', fill='y')
        errFrame = tk.Frame(errCanvas, width=width, height=600)
        errFrame.pack(fill='both', expand=True)
        #errFilterFrame = tk.Frame(errFrame)
        errGraphFrame = tk.Frame(errFrame)
        
        errCanvas.create_window(10, 10, anchor='nw', window=errFrame)
        
        #errFilterFrame.pack(side='top', fill='both', expand=True)
        errGraphFrame.pack(side='bottom', fill='both', expand=True)
        self.errContentFrame = errContentFrame
        self.errGraphFrame = errGraphFrame
        self.errContentFrame = errContentFrame
        self.errCanvas = errCanvas
        self.errGraphFrame = errGraphFrame
        # output = dict()
        # keys = []
        # with open('sample_output_file_weights.txt', 'r') as datafile:
        #     plotting = csv.reader(datafile, delimiter='\t')
        #     count = 0;
        #     for row in plotting:
        #         for i in range(len(row)):
        #             if count == 0:
        #                 output[row[i]] = [0]
        #                 keys.append(row[i])
        #             elif count == 1:
        #                 output[keys[i]] = [float(row[i])]
        #             else:
        #                 output[keys[i]].append(float(row[i]))
        #         count +=1;
        # self.output = output
        # self.GenerateGraph(self.output)
    
    def GenerateErrGraph(self, d):
        self.errAxes = self.MakeGraph(self.errGraphFrame, d, title='ErrorRate', xlabel='Epoch', ylabel='ErrorRate', filter=None, xsize=5, ysize=4)
    def GenerateWeightsGraph(self, d):
        self.weightsFilter = self.GraphFilters(self.weightsFilterFrame, d)
        self.weightAxes = self.MakeGraph(self.weightsGraphFrame, d, title='Results', xlabel='Epoch', ylabel='Weights', filter=self.weightsFilter, xsize=5, ysize=8)
    
    def ConvertToDict(self, l):
        output = dict()
        keys = []
        count = 0
        for i in range(len(l)):
            if count == 0:
                output[l[i]] = [0]
                keys.append(l[i])
            elif count == 1:
                output[keys[i]] = [float(l[i])]
            else:
                output[keys[i]].append(float(l[i]))
            count +=1;
        return output

    def GraphFilters(self, frame, d):
        label = tk.Label(frame, text='Filter Weights')
        label.grid(column = 0, row = 0, sticky = 'NW')
        #create dict
        filterDict = dict()
        for k, v in d.items():
            filterDict[k] = tk.BooleanVar(value=True)
        row = 1
        column = 0
        for option, value in filterDict.items():
            check_button = tk.Checkbutton(frame, text=option, variable=value, command=lambda *args: 
                                          self.UpdateAxes(self.weightAxes, d, title='Results', xlabel='Epoch', ylabel='Weights', filter=filterDict))
            check_button.grid(column=column, row=row, sticky='NW')
            if column == 0:
                column += 1
            else:
                column = 0
                row += 1
        return filterDict

    def MakeGraph(self, frame, d, title, xlabel, ylabel, filter, xsize = 6, ysize = 8):
        
        # create a figure
        figure = Figure(figsize=(xsize, ysize), dpi=100, layout='constrained')

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, frame)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, frame)

        # create axes
        axes = figure.add_subplot()
        self.figure = figure
        self.UpdateAxes(axes=axes, d=d, title=title, xlabel=xlabel, ylabel=ylabel, filter=filter)

        figure_canvas.get_tk_widget()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return axes

    def UpdateAxes(self, axes, d, title, xlabel, ylabel, filter):
        axes.clear()
        keys = list(d.keys())
        x=[]
        for i in range(len(d[keys[0]])):
            x.append(i)

        maxVal = 0
        if filter is not None:
            for k, v in d.items():
                if filter[k].get() == True:
                    axes.plot(x, v, label=k)
                    m = max(v)
                    if m > maxVal:
                       maxVal = m
        else:
            for k, v in d.items():
                axes.plot(x, v, label=k)
                m = max(v)
                if m > maxVal:
                    maxVal = m
        axes.set(yticks=(np.arange(0.5, int(maxVal)+1, 0.5)))
        axes.set_ylim(ymin=0, ymax=int(maxVal)+1)
        axes.set_title(title)
        axes.set_ylabel(ylabel)
        axes.set_xlabel(xlabel)
        axes.legend(bbox_to_anchor=(0, -0.25),
                     loc='upper left', borderaxespad=0.)
        #self.figure.legend(loc='outside lower left', borderaxespad=0.)
        self.figure.canvas.draw()