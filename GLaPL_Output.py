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

        weightsGraphFrame = tk.Frame(notebook)
        weightsGraphFrame.pack(fill='both', expand=True)

        errPercentFrame = tk.Frame(notebook)
        errPercentFrame.pack(fill='both', expand=True)

        notebook.add(weightsGraphFrame, text='Weights')
        notebook.add(errPercentFrame, text='error%')
        notebook.pack(fill='both', expand=True)

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

         # create a figure
        figure = Figure(figsize=(6, 12), dpi=100, layout='constrained')

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, weightsGraphFrame)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, weightsGraphFrame)

        # create axes
        axes = figure.add_subplot()

        x=[]
        for i in range(len(output[keys[0]])):
            x.append(i)

        count = 0
        maxVal = 0
        for k, v in output.items():
            axes.plot(x, v, label=keys[count])
            m = max(v)
            if m > maxVal:
               maxVal = m
            count +=1
        axes.set(yticks=(np.arange(0.5, int(maxVal)+1, 0.5)))
        axes.set_title('Test')
        axes.set_ylabel('Weights')
        axes.set_xlabel('Epoch')
        axes.set_ylim(ymin=0, ymax=int(maxVal)+1)
        axes.legend(bbox_to_anchor=(1.05, 1),
                         loc='upper left', borderaxespad=0.)

        figure_canvas.get_tk_widget()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.notebook = notebook
        self.weightsGraphFrame = weightsGraphFrame
        self.errPercentFrame = errPercentFrame