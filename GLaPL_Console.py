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
        width = 1280*.475-100
        height = 720 / 2
        consoleNotebook = ttk.Notebook(self.frame, width=width, height=height)

        historyFrame = tk.Frame(consoleNotebook)
        historyFrame.pack(fill='both', expand=True)
        historyText = scrolledtext.ScrolledText(historyFrame, wrap=tk.WORD)
        historyText.pack(padx=10, pady=10, fill=tk.BOTH, side=tk.LEFT, expand=True)

        progressFrame= tk.Frame(consoleNotebook)
        progressFrame.pack(fill='both', expand=True)
        progressText = scrolledtext.ScrolledText(progressFrame, wrap=tk.WORD)
        progressText.pack(padx=10, pady=10, fill=tk.BOTH, side=tk.LEFT, expand=True)

        consoleNotebook.add(progressFrame, text='Progress')
        consoleNotebook.add(historyFrame, text='History')
        consoleNotebook.pack(fill='both', expand=True)

        self.consoleNotebook = consoleNotebook
        self.historyFrame = historyFrame
        self.historyText = historyText
        self.progressFrame = progressFrame
        self.progressText = progressText

    def updateProgress(self, m):
        print(m)
        self.progressText.config(state = 'normal')
        self.progressText.insert(tk.END, m+'\n')
        self.progressText.config(state = 'disabled')

    def updateHistory(self, m):
        print(m)
        self.historyText.config(state = 'normal')
        self.historyText.insert(tk.END, m+'\n')
        self.historyText.config(state = 'disabled')