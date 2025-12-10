import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import csv

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

        #demo:
        #self.title('Tkinter Matplotlib Demo')

        #prepare data
        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()

        output = dict()

        names = []
        vals = []
        combined = [names, vals]
        keys = []

        with open('sample_output_file_weights.txt', 'r') as datafile:
            plotting = csv.reader(datafile, delimiter='\t')
            count = 0;
            for row in plotting:
                for i in range(len(row)):
                    if count == 0:
                        output[row[i]] = [0]
                        keys.append(row[i])
                    if count == 1:
                        output[keys[i]] = [row[i]]
                    if count >= 1:
                        output[keys[i]].append(row[i])
                count +=1;
                    # if count == 1:
                    #     output[i]
                # names.append(row[0][0])
                # for i in range(len(row)):
                    
                #     if (i == 0):
                #         vals.append(row[i])
        
        print(output)
        print(names)
        print(vals)
        for col in range(len(names[0])):output[col[0]] = col[1:]
        print(output)
         # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, weightsGraphFrame)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, weightsGraphFrame)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.plot(languages, popularity)
        axes.set_title('Test')
        axes.set_ylabel('Weights')
        axes.set_xlabel('Epoch')

        figure_canvas.get_tk_widget()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.notebook = notebook
        self.weightsGraphFrame = weightsGraphFrame
        self.errPercentFrame = errPercentFrame