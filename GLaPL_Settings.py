
import tkinter as tk
#from tkinter import *
from tkinter import END, Entry, Variable, ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import re
from venv import create
import sys
import learner as l
import GLaPLUtilities as util

g = l.Grammar()

platform = sys.platform

class GLaPL_Settings:
    self = None
    def __init__(self):
        self = self

    def SettingsFrame(self, root, frame):
        self.frame = frame
        self.root = root

        self.root.check_num_wrapper = (self.root.register(util.CheckNum),'%P')
        self.root.check_num_0to1_wrapper = (self.root.register(util.CheckNum0to1), '%P')
        self.root.check_numList_wrapper = (self.root.register(util.CheckNumList),'%P')
        
        # CONTENT SETTINGS
        sticky = 'NSEW'
        maxColumn = 8
        maxRow = 10
        column = 0
        gridRow = 0
        width = 680
        contentSettingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=frame, maxColumn=maxColumn, columnSpan=3, 
                                                                       maxRow=maxRow, column=column, row=gridRow, sticky=sticky, pady = 5, height=680))
        sticky = 'NW'
        maxColumn = 1
        maxRow = 1
        column = 0
        gridRow = 0
        height = 80
        settingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky=sticky, width=width, height=height))

        self.settingsNotebook = ttk.Notebook(settingsFrame)
        self.settingsNotebook.pack(fill='both', expand=True)
        self.settingsNotebook.pressed_index = None
        # self.settingsNotebook.config(width=600, height=200)
        # self.settingsNotebook.grid(column=0, row=0, sticky=sticky)
    
        sticky = 'NW'
        maxColumn = 8
        maxRow = 1
        column = 0
        gridRow = 0
        sizex = 680
        sizey = 300
        width = 630
        height = 155
    
        #Creating child frames
        self.generalContentFrame = tk.Frame(master=self.settingsNotebook)
        self.generalContentFrame.pack(fill='both', expand=True)

        self.advancedContentFrame = tk.Frame(master=self.settingsNotebook)
        self.advancedContentFrame.pack(fill='both', expand=True)

        #Adding notebook tabs
        self.settingsNotebook.add(self.generalContentFrame, text='General Settings')
        self.settingsNotebook.add(self.advancedContentFrame, text='Advanced Settings')

        #Creating canvases
        self.generalCanvas = tk.Canvas(self.generalContentFrame, width=width, height=height)
        self.generalScroll = tk.Scrollbar(self.generalContentFrame, command=self.generalCanvas.yview)
        self.generalCanvas.config(yscrollcommand=self.generalScroll.set, scrollregion=(0,0,width, 300))
        self.generalCanvas.pack(side='left', fill='both', expand=True)
        self.generalScroll.pack(side='right', fill='y')

        self.advancedCanvas = tk.Canvas(self.advancedContentFrame, width=width, height=height)
        self.advancedScroll = tk.Scrollbar(self.advancedContentFrame, command=self.advancedCanvas.yview)
        self.advancedCanvas.config(yscrollcommand=self.advancedScroll.set, scrollregion=(0,0,width, 300))
        self.advancedCanvas.pack(side='left', fill='both', expand=True)
        self.advancedScroll.pack(side='right', fill='y')

        #Creating frames that live inside the canvas
        self.generalFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.generalFrame.bind('<Enter>', lambda event, canvas=self.generalCanvas: util.onMouseWheel(canvas, event=event))
        self.generalCanvas.create_window(10, 10, anchor='nw', window=self.generalFrame)

        self.advancedFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.advancedFrame.bind('<Enter>', lambda event, canvas=self.advancedCanvas: util.onMouseWheel(canvas, event=event))
        self.advancedCanvas.create_window(10, 10, anchor='nw', window=self.advancedFrame)
    
        sticky = 'NW'
        gridRow = 0  

        # GENERAL SETTINGS:
        nbRow = 0
        self.weightsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalFrame, maxColumn=5, maxRow=3, columnSpan=8, column=0, row=nbRow, sticky=sticky))
        self.weightsLabel = tk.Label(self.weightsFrame, anchor='nw', text='Starting Weights')
        self.weightsLabel.grid(column = 0, row=nbRow, sticky=sticky)
        self.weightTypeRadio = tk.StringVar()
        self.weightSetAllNum = tk.StringVar(value='0')
        self.weightsRandomMin = tk.StringVar(value='0')
        self.weightsRandomMax = tk.StringVar(value='10')
        self.weightsSetIndividually = tk.StringVar(value='0')
        self.weightsVarList = [float(self.weightSetAllNum.get()), [float(self.weightsRandomMin.get()), float(self.weightsRandomMax.get())], self.weightsSetIndividually.get()]
        self.weightsOptions = {'Set all to' : 'all',
                        'Randomize between' : 'rand',
                        'Set individually \n(separate with commas)' : 'setIndividually',
                        }
        self.weightsRadioVar = tk.StringVar()
        self.weightsRadioList = []
        self.weightRadioCount = 0
        rowCount = 0
        for (text, value) in self.weightsOptions.items():
            r = tk.Radiobutton(
                self.weightsFrame, text=text, value=value, variable=self.weightsRadioVar, 
                command=lambda *args: util.SendParams('weights', self.weightsRadioVar, self.weightsVarList[self.weightRadioCount]))
            r.grid(column = 2, row=nbRow, sticky=sticky, padx=15)
            self.weightsRadioList.append(r)
            nbRow += 1
            rowCount += 1
            self.weightRadioCount += 1
        self.weightsRadioVar.set('all')
    
        self.weightsRadioList[0].config(command=lambda *args: util.ToggleWeightsEntries(self.weightsEntryList, active=[0]))
        self.weightsRadioList[1].config(command=lambda *args: util.ToggleWeightsEntries(self.weightsEntryList, active=[1,2]))
        self.weightsRadioList[2].config(command=lambda *args: util.ToggleWeightsEntries(self.weightsEntryList, active=[3]))
        nbRow -= rowCount
        self.weightsEntryList = []
        self.weightsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent = self.weightsFrame, column = 3, row = nbRow, 
                                                              sticky = sticky, variable = self.weightSetAllNum, command = self.root.check_num_wrapper,
                                                              labelWidth = 0, entryWidth = 15),
                                    util.Tkinter_Field_Settings(parent = self.weightsFrame, column = 3, row = nbRow +1, 
                                                              sticky = sticky, variable = self.weightsRandomMin, command = self.root.check_num_wrapper,
                                                              labelWidth = 0, entryWidth = 15),
                                    util.Tkinter_Field_Settings(parent = self.weightsFrame, text = 'and', column = 5, row = nbRow +1, 
                                                              sticky = sticky, variable = self.weightsRandomMax, command = self.root.check_num_wrapper,
                                                              labelWidth = 3, entryWidth = 15),
                                    util.Tkinter_Field_Settings(parent = self.weightsFrame, column = 3, row = nbRow +2, pady=5,
                                                              sticky = sticky, variable = self.weightsSetIndividually, command = self.root.check_numList_wrapper,
                                                              labelWidth = 0, entryWidth = 15)],fieldEntryList=self.weightsEntryList)
        self.weightsEntryList[0].bind('<Return>', lambda *args: g.setParam("weights",['all',float(self.weightSetAllNum.get())]))
        self.weightsEntryList[1].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(self.weightsRandomMin.get()), float(self.weightsRandomMax.get())]))
        self.weightsEntryList[2].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(self.weightsRandomMin.get()), float(self.weightsRandomMax.get())]))
        self.weightsEntryList[3].bind('<Return>', lambda *args: util.SendParams(param='weights', type='setIndividually', value=self.weightsSetIndividually.get(), convertToFloats=True))
        util.ToggleWeightsEntries(self.weightsEntryList, active=[0])

        nbRow += 1
        self.lRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
        self.lRateNum = tk.StringVar()
        self.lRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent = self.lRateFrame, text = 'Learning Rate', column = 0, row = nbRow, 
                                                              sticky = sticky, variable = self.lRateNum, command = self.root.check_num_wrapper,
                                                              labelWidth = 12, entryWidth = 15)])
        self.lRateEntry.bind('<Return>', lambda *args: g.setParam("learningRate",[float(self.lRateNum.get())]))
        self.lRateDecreaseBool = tk.IntVar(value=0)
        self.lRateStartNum = tk.StringVar()
        self.lRateEndNum = tk.StringVar()
        self.lRateFieldList = []
        self.lRateDecreaseCheckBox = tk.Checkbutton(self.lRateFrame, text="Decrease Learning Rate:", variable=self.lRateDecreaseBool, 
                                command=lambda *args: util.CreateEntry([util.Tkinter_Field_Settings(parent = self.lRateFrame, text = 'Start', 
                                                                                               column = 3, row = nbRow-1, sticky = sticky, 
                                                    variable = self.lRateStartNum, command = self.root.check_num_wrapper, entry = self.lRateEntry, labelWidth = 4), 
                                                                   util.Tkinter_Field_Settings(parent = self.lRateFrame, text = 'End', 
                                                                                               column = 5, row = nbRow-1, sticky = sticky, 
                                                    variable = self.lRateEndNum, command = self.root.check_num_wrapper, entry = self.lRateEntry, labelWidth = 3)], 
                                                                  self.lRateDecreaseBool.get(), self.lRateFieldList, self.lRateEntry))
        self.lRateDecreaseCheckBox.grid(column=2, row=nbRow, sticky=sticky, padx=15)

        nbRow += 1
        self.decayRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalFrame, maxColumn=10, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
        self.decayRateNum = tk.StringVar()
        self.decayRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.decayRateFrame, text='Decay Rate', column=0, row=nbRow, sticky=sticky, 
                                                                  variable=self.decayRateNum, command=self.root.check_num_wrapper)])
        self.decayRateEntry.bind('<Return>', lambda *args: g.setParam("decayRate", float(self.decayRateNum.get())))
        self.decayRateRadio = tk.StringVar()
        self.decayRateRadioList = []
        self.decayOptions = {'L1' : 'L1',
                        'L2' : 'L2',
                        'Static' : 'Static',
                        'No Decay' : 'NoDecay'}
        decayColumn = 2
        for (text, value) in self.decayOptions.items():
            r = tk.Radiobutton(
                self.decayRateFrame, text=text, value=value, variable=self.decayRateRadio, command=lambda *args: g.setParam('decayType', self.decayRateRadio.get()))
            r.grid(column = decayColumn, row = nbRow, sticky = sticky, padx = 15)
            decayColumn += 1
        # util.CreateRadio_setParam(util.Tkinter_Field_Settings(parent=self.decayRateFrame, dictionary=self.decayOptions, parameter='decayType', radioVariable=self.decayRateRadio, variableDefault='NoDecay', 
        #                                                  variable=[self.decayRateNum], column=2, row=nbRow, sticky=sticky, padx=15, _list=self.decayRateRadioList))
        #self.decayRateRadioList[0].config(command=lambda *args: g.setParam('decayType','L1'))
        self.decayRateRadio.set('NoDecay')

        nbRow += 1
        self.totalIterationsNum = tk.StringVar()
        self.totalIterationsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
        self.totalIterationsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.totalIterationsFrame, text='Total Iterations', column=0, row=nbRow, sticky=sticky, 
                                                                  variable=self.totalIterationsNum)])

        nbRow += 1
        self.epochsNum = tk.StringVar(value = g.epoch)
        self.epochsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
        self.epochsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.totalIterationsFrame, text='Epochs', column=0, row=nbRow, sticky=sticky, 
                                                                  variable=self.epochsNum, command = self.root.check_num_wrapper)])

        #ADVANCED SETTINGS:
        maxColumn = 3
        maxRow = 1
        nbRow = 0

        self.thresholdNum = tk.StringVar(value = g.comparisonThreshold)
        self.thresholdFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        self.thresholdEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.thresholdFrame, text='threshold', column=1, row=nbRow, sticky=sticky, 
                                                                  variable=self.thresholdNum, command = self.root.check_num_wrapper)])
        self.thresholdEntry.bind('<Return>', lambda *args: g.setParam("threshold", float(self.thresholdNum.get())))
    
        nbRow += 1
        self.featureSetFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        wrapLength=300
        self.featureInputFile = tk.Label(self.featureSetFrame, text='feature Set File')
        self.featureInputFile.grid(column=0, row=nbRow, sticky=sticky)
        self.featureMessage = tk.StringVar()
        self.featureInputButton = tk.Button(self.featureSetFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('featureSet', self.featureMessage)) 
        self.featureInputButton.grid(column=1, row=nbRow, sticky=sticky)
        self.featureInputMessage = tk.Label(self.featureSetFrame, textvariable=self.featureMessage, wraplength=wrapLength)
        self.featureInputMessage.grid(column=2, row=nbRow, sticky=sticky)

        nbRow += 1
        self.genCandidatesFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        self.genCandidatesBool = tk.BooleanVar()
        self.genCandidatesBool.set(g.generateCandidates)
        self.genCandidatesCheckBox = tk.Checkbutton(self.genCandidatesFrame, text="Generate Candidates:", variable=self.genCandidatesBool, 
                                               command=lambda *args: g.setParam("generateCandidates", value=self.genCandidatesBool.get()))
        self.genCandidatesCheckBox.grid(column=0, row=nbRow, sticky=sticky)

        nbRow += 1
        self.constraintsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        self.constraintInputFile = tk.Label(self.constraintsFrame, text='Constraints Set File')
        self.constraintInputFile.grid(column=0, row=nbRow, sticky=sticky)
        self.constraintsMessage = tk.StringVar()
        self.constraintInputButton = tk.Button(self.constraintsFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('Constraints', self.constraintsMessage)) 
        self.constraintInputButton.grid(column=1, row=nbRow, sticky=sticky)
        self.constraintInputMessage = tk.Label(self.constraintsFrame, textvariable=self.constraintsMessage, wraplength=wrapLength)
        self.constraintInputMessage.grid(column=2, row=nbRow, sticky=sticky)

        nbRow += 1
        self.addViolationsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        self.addViolationsBool = tk.BooleanVar()
        self.addViolationsBool.set(g.addViolations)
        self.addViolationsCheckBox = tk.Checkbutton(self.addViolationsFrame, text="Add Violations:", variable=self.addViolationsBool, 
                                               command=lambda *args: g.setParam("addViolations", value=self.addViolationsBool.get()))
        self.addViolationsCheckBox.grid(column=0, row=nbRow, sticky=sticky)

        nbRow += 1
        self.verboseOutputFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                          column=0, row=nbRow, sticky=sticky))
        self.verboseOutputBool = tk.BooleanVar()
        self.verboseOutputBool.set(g.noisy)
        self.verboseOutputCheckBox = tk.Checkbutton(self.verboseOutputFrame, text="Verbose Console Output:", variable=self.verboseOutputBool, 
                                               command=lambda *args: g.setParam("noisy", value=self.verboseOutputBool.get()))
        self.verboseOutputCheckBox.grid(column=0, row=nbRow, sticky=sticky)

        #LISTING & INDEXATION
        gridRow = 1
        maxColumn = 1
        maxRow = 1
    
        sticky = 'NW'
        maxColumn = 1
        maxRow = 1
        column = 0
        gridRow = 2
        height = 80
        self.paramsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=gridRow, sticky=sticky, width=width, height=height))

        self.paramsNotebook = ttk.Notebook(self.paramsFrame)
        self.paramsNotebook.pack(fill='both', expand=True)
        self.paramsNotebook.pressed_index = None
    
        sticky = 'NW'
        maxColumn = 8
        maxRow = 1
        column = 0
        gridRow = 0
        sizex = 680
        sizey = 300
        width = 630
        height = 165
    
        #Creating child frames
        self.listingContentFrame = tk.Frame(master=self.paramsNotebook)
        self.listingContentFrame.pack(fill='both', expand=True)

        self.indexationContentFrame = tk.Frame(master=self.paramsNotebook)
        self.indexationContentFrame.pack(fill='both', expand=True)

        self.rstContentFrame = tk.Frame(master=self.paramsNotebook)
        self.rstContentFrame.pack(fill='both', expand=True)

        #Adding notebook tabs
        self.paramsNotebook.add(self.listingContentFrame, text='Listing')
        self.paramsNotebook.add(self.indexationContentFrame, text='Indexation')
        self.paramsNotebook.add(self.rstContentFrame, text='Representational Strength Theory')

        #Creating canvases
        self.listingCanvas = tk.Canvas(self.listingContentFrame, width=width, height=height)
        self.listingScroll = tk.Scrollbar(self.listingContentFrame, command=self.listingCanvas.yview)
        self.listingCanvas.config(yscrollcommand=self.listingScroll.set, scrollregion=(0,0,width, 300))
        self.listingCanvas.pack(side='left', fill='both', expand=True)
        self.listingScroll.pack(side='right', fill='y')

        self.indexationCanvas = tk.Canvas(self.indexationContentFrame, width=width, height=height)
        self.indexationScroll = tk.Scrollbar(self.indexationContentFrame, command=self.indexationCanvas.yview)
        self.indexationCanvas.config(yscrollcommand=self.indexationScroll.set, scrollregion=(0,0,width, 300))
        self.indexationCanvas.pack(side='left', fill='both', expand=True)
        self.indexationScroll.pack(side='right', fill='y')

        self.rstCanvas = tk.Canvas(self.rstContentFrame, width=width, height=height)
        self.rstScroll = tk.Scrollbar(self.rstContentFrame, command=self.rstCanvas.yview)
        self.rstCanvas.config(yscrollcommand=self.rstScroll.set, scrollregion=(0,0,width, 300))
        self.rstCanvas.pack(side='left', fill='both', expand=True)
        self.rstScroll.pack(side='right', fill='y')

        #Creating frames that live inside the canvas
        self.listingFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.listingFrame.bind('<Enter>', lambda event, canvas=self.listingCanvas: util.onMouseWheel(canvas, event=event))
        self.listingCanvas.create_window(10, 10, anchor='nw', window=self.listingFrame)

        self.indexationFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.indexationFrame.bind('<Enter>', lambda event, canvas=self.indexationCanvas: util.onMouseWheel(canvas, event=event))
        self.indexationCanvas.create_window(10, 10, anchor='nw', window=self.indexationFrame)

        self.rstFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.rstCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=0, sticky='NEW', width=sizex, height=sizey))
        # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
        # self.rstFrame.bind('<Enter>', lambda event, canvas=self.rstCanvas: util.onMouseWheel(canvas, event=event))
        self.rstCanvas.create_window(10, 10, anchor='nw', window=self.rstFrame)
    
        sticky = 'NW'
    
        #Listing Frame:
        nbRow = 0
        self.listingTypeFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.listedLabel = tk.Label(self.listingTypeFrame, anchor='nw', text='Listed Type:')
        self.listedLabel.grid(column=0, row=nbRow, sticky = sticky)
        self.listedTypeRateRadio = tk.StringVar(value=g.useListedType)
        self.listedTypeRateRadioList = []
        self.listedTypeOptions = {'Hidden Structure' : 'hidden_structure',
                        'Sample Using Frequency' : 'sample_using_frequency',
                        'Sample Flat Rate' : 'sample_flat_rate',
                        'None' : 'none'}
        self.listedTypeDescriptions = ['desc 1',
                                  'desc 2',
                                  'desc 3',
                                  'desc 4']
        listedTypeColumn = 1
        row = nbRow
        i = 0
        for (text, value) in self.listedTypeOptions.items():
            r = tk.Radiobutton(
                self.listingTypeFrame, text=text, value=value, variable=self.listedTypeRateRadio, command=lambda *args: g.setParam('useListedType', self.listedTypeRateRadio.get()))
            r.grid(column = listedTypeColumn, row = row, sticky = sticky, padx = 15)
            listedDescLabel = tk.Label(self.listingTypeFrame, anchor='nw', text=self.listedTypeDescriptions[i])
            listedDescLabel.grid(column=listedTypeColumn +1, row=row, sticky = sticky)
            row += 1
            i += 1

        nbRow += row
        self.listingRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.listedRateNum = tk.StringVar(value=g.useListedRate)
        self.listedRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.listingRateFrame, text='Listed Rate', column=0, row=nbRow, sticky=sticky, 
                                                                  variable=self.listedRateNum, command = self.root.check_num_0to1_wrapper)])
        self.listedRateEntry.bind('<Return>', lambda *args: g.setParam('useListedRate', float(self.listedRateNum.get())))

        nbRow += 1
        self.flipFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.flipBool = tk.BooleanVar()
        self.flipBool.set(g.flip)
        self.flipCheckBox = tk.Checkbutton(self.flipFrame, text="flip:", variable=self.flipBool, 
                                               command=lambda *args: g.setParam("flip", value=self.flipBool.get()))
        self.flipCheckBox.grid(column=0, row=nbRow, sticky=sticky)

        nbRow += 1
        self.simpleListingFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.simpleListingBool = tk.BooleanVar()
        self.simpleListingBool.set(g.simpleListing)
        self.simpleListingCheckBox = tk.Checkbutton(self.simpleListingFrame, text="Simple Listing:", variable=self.simpleListingBool, 
                                               command=lambda *args: g.setParam("simpleListing", value=self.simpleListingBool.get()))
        self.simpleListingCheckBox.grid(column=0, row=nbRow, sticky=sticky)

        nbRow += 1
        self.pToListFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.pToListNum = tk.StringVar(value=g.pToList)
        self.pToListEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.pToListFrame, text='pToList', column=0, row=nbRow, sticky=sticky, 
                                                                  variable=self.pToListNum, command = self.root.check_num_0to1_wrapper)])
        self.pToListEntry.bind('<Return>', lambda *args: g.setParam('pToList', float(self.pToListNum.get())))

        #Indexation Frame:
        nbRow = 0
        self.nLexCsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.nLexCsNum = tk.StringVar(value=g.lexC_type)
        self.nLexCsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.nLexCsFrame, text='nLexCs', column=0, row=nbRow, 
                                                               sticky=sticky, labelWidth=18, 
                                                                  variable=self.nLexCsNum, command = self.root.check_num_wrapper)])
        self.nLexCsEntry.bind('<Return>', lambda *args: g.setParam('nLexCs', float(self.nLexCsNum.get())))

        nbRow += 1
        self.pChangeIndexationFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.pChangeIndexationNum = tk.StringVar(value=g.pChangeIndexation)
        self.pChangeIndexationEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.pChangeIndexationFrame, text='pChangeIndexation', column=0, 
                                                                          row=nbRow, sticky=sticky, labelWidth=18, 
                                                                  variable=self.pChangeIndexationNum, command = self.root.check_num_0to1_wrapper)])
        self.pChangeIndexationEntry.bind('<Return>', lambda *args: g.setParam('pChangeIndexation', float(self.pChangeIndexationNum.get())))

        nbRow += 1
        self.lexCStartWFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, 
                                                                  maxRow=maxRow, column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.lexCStartWNum = tk.StringVar(value=g.lexCStartW)
        self.lexCStartWEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.lexCStartWFrame, text='lexCStartW', column=0, row=nbRow, 
                                                                   sticky=sticky, labelWidth=18, 
                                                                  variable=self.lexCStartWNum, command = self.root.check_num_wrapper)])
        self.lexCStartWEntry.bind('<Return>', lambda *args: g.setParam('lexCStartW', float(self.lexCStartWNum.get())))

        nbRow += 1
        self.localityFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.localityLabel = tk.Label(self.localityFrame, anchor='nw', text='locality:')
        self.localityLabel.grid(column=0, row=nbRow, sticky = sticky)
        self.localityRateRadio = tk.StringVar(value=g.localityRestrictionType)
        self.localityRateRadioList = []
        self.localityOptions = {'Overlap' : 'overlap',
                        'Presence Only' : 'presence_only',
                        'Strict' : 'strict'}
        self.localityDescriptions = ['desc 1',
                                  'desc 2',
                                  'desc 3']
        self.localityColumn = 1
        row = nbRow
        i = 0
        for (text, value) in self.localityOptions.items():
            r = tk.Radiobutton(
                self.localityFrame, text=text, value=value, variable=self.localityRateRadio, command=lambda *args: g.setParam('locality', self.localityRateRadio.get()))
            r.grid(column = self.localityColumn, row = row, sticky = sticky, padx = 15)
            self.localityDescLabel = tk.Label(self.localityFrame, anchor='nw', text=self.localityDescriptions[i])
            self.localityDescLabel.grid(column=self.localityColumn +1, row=row, sticky = sticky)
            row += 1
            i += 1
    
        ## FIRST INDEX STRAT NOT FULLY IMPLEMENTED YET
        # nbRow += 1
        # firstIndexStratFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
        #                            column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        # firstIndexStratLabel = tk.Label(firstIndexStratFrame, anchor='nw', text='First Index Strat:')
        # firstIndexStratLabel.grid(column=0, row=nbRow, sticky = sticky)
        self.firstIndexStratRateRadio = tk.StringVar(value=g.firstIndexStrat)
        # self.firstIndexStratRateRadioList = []
        # #NEED OPTIONS
        # firstIndexStratOptions = {'Lowest' : 'lowest'}
        # firstIndexStratDescriptions = ['desc 1',
        #                           'desc 2',
        #                           'desc 3']
        # firstIndexStratColumn = 1
        # row = nbRow
        # i = 0

        # for (text, value) in firstIndexStratOptions.items():
        #     r = tk.Radiobutton(
        #         firstIndexStratFrame, text=text, value=value, variable=self.firstIndexStratRateRadio, command=lambda *args: g.setParam('first_index_strategy', self.firstIndexStratRateRadio.get()))
        #     r.grid(column = firstIndexStratColumn, row = row, sticky = sticky, padx = 15)
        #     firstIndexStratDescLabel = tk.Label(firstIndexStratFrame, anchor='nw', text=firstIndexStratDescriptions[i])
        #     firstIndexStratDescLabel.grid(column=firstIndexStratColumn +1, row=row, sticky = sticky)
        #     row += 1
        #     i += 1
    
        #rst Frame:
        nbRow = 0
        self.PFC_typeFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.PFC_typeLabel = tk.Label(self.PFC_typeFrame, anchor='nw', text='PFC Type:')
        self.PFC_typeLabel.grid(column=0, row=nbRow, sticky = sticky)
        self.PFC_typeRateRadio = tk.StringVar(value=g.PFC_type)
        self.PFC_typeRateRadioList = []
        self.PFC_typeOptions = {'None' : 'none',
                        'Pseudo' : 'pseudo',
                        'Full' : 'full'}
        self.PFC_typeDescriptions = ['desc 1',
                                  'desc 2',
                                  'desc 3']
        self.PFC_typeColumn = 1
        row = nbRow
        i = 0

        for (text, value) in self.PFC_typeOptions.items():
            r = tk.Radiobutton(
                self.PFC_typeFrame, text=text, value=value, variable=self.PFC_typeRateRadio, command=lambda *args: g.setParam('PFC_type', self.PFC_typeRateRadio.get()))
            r.grid(column = self.PFC_typeColumn, row = row, sticky = sticky, padx = 15)
            self.PFC_typeDescLabel = tk.Label(self.PFC_typeFrame, anchor='nw', text=self.PFC_typeDescriptions[i])
            self.PFC_typeDescLabel.grid(column=self.PFC_typeColumn +1, row=row, sticky = sticky)
            row += 1
            i += 1
    
        nbRow += 1
        self.PFC_lRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.PFC_lRateNum = tk.StringVar(value=g.PFC_lrate)
        self.PFC_lRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.PFC_lRateFrame, text='PFC Learning Rate', column=0, row=nbRow, 
                                                                  sticky=sticky, labelWidth=18, 
                                                                  variable=self.PFC_lRateNum, command = self.root.check_num_wrapper)])
        self.PFC_lRateEntry.bind('<Return>', lambda *args: g.setParam('PFC_lrate', float(self.PFC_lRateNum.get())))

        nbRow += 1
        self.PFC_startWFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=self.rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                                   column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
        self.PFC_startWNum = tk.StringVar(value=g.PFC_startW)
        self.PFC_startWEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=self.PFC_startWFrame, text='PFC Starting Weight', column=0, row=nbRow, 
                                                                   sticky=sticky, labelWidth=18,
                                                                  variable=self.PFC_startWNum, command = self.root.check_num_wrapper)])
        self.PFC_startWEntry.bind('<Return>', lambda *args: g.setParam('PFC_startW', float(self.PFC_startWNum.get())))

        #DATA FILE SELECTION
        gridRow += 1
        maxColumn = 3
        maxRow = 3
        folderFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                                   column=0, row=gridRow, sticky=sticky, width=600, height=75))
    
        # ttk.Frame(frame, borderwidth=0, width=600, height=75)
        # folderFrame.grid(column=0, row=2, columnspan=3, sticky=sticky)
        wrapLength=300
        self.inputFile = tk.Label(folderFrame, text='Training Data File')
        self.inputFile.grid(column=0, row=gridRow, sticky=sticky)
        self.message = tk.StringVar()
        self.inputButton = tk.Button(folderFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('trainingData', message)) 
        self.inputButton.grid(column=1, row=gridRow, sticky=sticky)
        self.inputMessage = tk.Label(folderFrame, textvariable=self.message, wraplength=wrapLength)
        self.inputMessage.grid(column=2, row=gridRow, sticky=sticky)

        gridRow += 1
        self.outputFolder = tk.Label(folderFrame, text='Output Folder')
        self.outputFolder.grid(column=0, row=gridRow, sticky=sticky)
        self.outputPath = tk.StringVar()
        self.outputFolderButton = tk.Button(folderFrame, width=15, text='Select Folder', command=lambda *args : util.GetDirectory(self.outputPath)) 
        self.outputFolderButton.grid(column=1, row=gridRow, sticky=sticky)
        self.outputFolderName = tk.Label(folderFrame, textvariable=self.outputPath, wraplength=wrapLength)
        self.outputFolderName.grid(column=2, row=gridRow, sticky=sticky)
    
        # REPORTING PARAMS
        #   
        #SAVE SETTINGS
        gridRow += 1
        maxColumn = 2
        maxRow = 3
        self.saveSettingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                                   column=0, row=gridRow, sticky=sticky, width=600, height=200))

        saveRow = 0
        self.saveSettingsLabel = tk.Label(self.saveSettingsFrame, text='Save:')
        self.saveSettingsLabel.grid(column=0, row=saveRow, sticky=sticky)

        saveRow += 1
        startRow = saveRow
        gridColumn = 0
        maxRows = 2
        saveTypesDict = {'Weights': tk.BooleanVar(value=g.save_weights), 
                         'Error rates': tk.BooleanVar(value=g.save_errRates), 
                         'Tableaux': tk.BooleanVar(value=g.save_tableaux),
                         'Indexation final state': tk.BooleanVar(value=g.save_finalIndexation), 
                         'Indexed constraints weights over time (by constraint)': tk.BooleanVar(value=g.save_indexedWeightsByConstraint), 
                         'Indexed constraints weights over time (by lexeme) -- LARGE FILE': tk.BooleanVar(value=g.save_indexedWeightsByLexeme),
                         'Listing history': tk.BooleanVar(value=g.save_listingHistory),
                         'Phonological Form constraints': tk.BooleanVar(value=g.save_PFCs),
                         'Learned Lexicon': tk.BooleanVar(value=g.save_actualLexicon)
                         }
        for option, value in saveTypesDict.items():
            check_button = tk.Checkbutton(self.saveSettingsFrame, text=option, variable=value, command=lambda *args: util.SendDictionary('filesToSave',saveTypesDict))
            check_button.grid(column=gridColumn, row=saveRow, sticky=sticky)
            saveRow += 1
            if saveRow - startRow > maxRows:
                saveRow = startRow
                gridColumn += 1
    
        #LEARN  & VALIDATE BUTTONS
        gridRow += 1
        self.val_Learn_Frame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                                   column=0, row=gridRow, sticky=sticky, width=600, height=200))
        # validateDict = {
        #     'weights': ,

        #     }
        self.validateButton = tk.Button(self.val_Learn_Frame, width=15, text='Validate')
        self.validateButton.place(anchor='center')
        self.validateButton.grid(column=0, row=gridRow, padx=12, pady=12, sticky=sticky)
        # collect all params and values in a dictionary and iterate through it and call setParam for each param / value pair

        self.learnButton = tk.Button(self.val_Learn_Frame, width=15, text='Learn')
        self.learnButton.place(anchor='center')
        self.learnButton.grid(column=2, row=gridRow, padx=12, pady=12, sticky=sticky)

        # sample code for validating:
        # for i in entries:
        #    result = g.setParam(parameter,value)
        #    if result:   
        #          it's an error or warning
    def validate(self, entries):
        l = []
        # Weights:
        for e in entries:
            l.add(util.getVars(e.key, e.value))

        return l