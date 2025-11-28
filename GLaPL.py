# -*- coding: utf-8 -*-
'''
Created on Wed Oct 22 20:20:47 2025

@author: moore-cantwell
'''
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


root = tk.Tk()
check_num_wrapper = (root.register(util.CheckNum),'%P')
check_num_0to1_wrapper = (root.register(util.CheckNum0to1), '%P')
check_numList_wrapper = (root.register(util.CheckNumList),'%P')

g = l.Grammar()

    
def SettingsFrame(frame):

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

    settingsNotebook = ttk.Notebook(settingsFrame)
    settingsNotebook.pack(fill='both', expand=True)
    settingsNotebook.pressed_index = None
    # settingsNotebook.config(width=600, height=200)
    # settingsNotebook.grid(column=0, row=0, sticky=sticky)
    
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
    generalContentFrame = tk.Frame(master=settingsNotebook)
    generalContentFrame.pack(fill='both', expand=True)

    advancedContentFrame = tk.Frame(master=settingsNotebook)
    advancedContentFrame.pack(fill='both', expand=True)

    #Adding notebook tabs
    settingsNotebook.add(generalContentFrame, text='General Settings')
    settingsNotebook.add(advancedContentFrame, text='Advanced Settings')

    #Creating canvases
    generalCanvas = tk.Canvas(generalContentFrame, width=width, height=height)
    generalScroll = tk.Scrollbar(generalContentFrame, command=generalCanvas.yview)
    generalCanvas.config(yscrollcommand=generalScroll.set, scrollregion=(0,0,width, 300))
    generalCanvas.pack(side='left', fill='both', expand=True)
    generalScroll.pack(side='right', fill='y')

    advancedCanvas = tk.Canvas(advancedContentFrame, width=width, height=height)
    advancedScroll = tk.Scrollbar(advancedContentFrame, command=advancedCanvas.yview)
    advancedCanvas.config(yscrollcommand=advancedScroll.set, scrollregion=(0,0,width, 300))
    advancedCanvas.pack(side='left', fill='both', expand=True)
    advancedScroll.pack(side='right', fill='y')

    #Creating frames that live inside the canvas
    generalFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky='NEW', width=sizex, height=sizey))
    # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
    # generalFrame.bind('<Enter>', lambda event, canvas=generalCanvas: util.onMouseWheel(canvas, event=event))
    generalCanvas.create_window(10, 10, anchor='nw', window=generalFrame)

    advancedFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky='NEW', width=sizex, height=sizey))
    # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
    # advancedFrame.bind('<Enter>', lambda event, canvas=advancedCanvas: util.onMouseWheel(canvas, event=event))
    advancedCanvas.create_window(10, 10, anchor='nw', window=advancedFrame)
    
    sticky = 'NW'
    gridRow = 0  

    # GENERAL SETTINGS:
    nbRow = 0
    weightsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=5, maxRow=3, columnSpan=8, column=0, row=nbRow, sticky=sticky))
    weightsLabel = tk.Label(weightsFrame, anchor='nw', text='Starting Weights')
    weightsLabel.grid(column = 0, row=nbRow, sticky=sticky)
    weightTypeRadio = tk.StringVar()
    weightSetAllNum = tk.StringVar(value='0')
    weightsRandomMin = tk.StringVar(value='0')
    weightsRandomMax = tk.StringVar(value='10')
    weightsSetIndividually = tk.StringVar(value='0')
    weightsVarList = [float(weightSetAllNum.get()), [float(weightsRandomMin.get()), float(weightsRandomMax.get())], weightsSetIndividually.get()]
    weightsOptions = {'Set all to' : 'all',
                    'Randomize between' : 'rand',
                    'Set individually \n(separate with commas)' : 'setIndividually',
                    }
    weightsRadioVar = tk.StringVar()
    weightsRadioList = []
    weightRadioCount = 0
    rowCount = 0
    for (text, value) in weightsOptions.items():
        r = tk.Radiobutton(
            weightsFrame, text=text, value=value, variable=weightsRadioVar, 
            command=lambda *args: util.SendParams('weights', weightsRadioVar, weightsVarList[weightRadioCount]))
        r.grid(column = 2, row=nbRow, sticky=sticky, padx=15)
        weightsRadioList.append(r)
        nbRow += 1
        rowCount += 1
        weightRadioCount += 1
    weightsRadioVar.set('all')
    
    weightsRadioList[0].config(command=lambda *args: util.ToggleWeightsEntries(weightsEntryList, active=[0]))
    weightsRadioList[1].config(command=lambda *args: util.ToggleWeightsEntries(weightsEntryList, active=[1,2]))
    weightsRadioList[2].config(command=lambda *args: util.ToggleWeightsEntries(weightsEntryList, active=[3]))
    nbRow -= rowCount
    weightsEntryList = []
    weightsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = nbRow, 
                                                          sticky = sticky, variable = weightSetAllNum, command = check_num_wrapper,
                                                          labelWidth = 0, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = nbRow +1, 
                                                          sticky = sticky, variable = weightsRandomMin, command = check_num_wrapper,
                                                          labelWidth = 0, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, text = 'and', column = 5, row = nbRow +1, 
                                                          sticky = sticky, variable = weightsRandomMax, command = check_num_wrapper,
                                                          labelWidth = 3, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = nbRow +2, pady=5,
                                                          sticky = sticky, variable = weightsSetIndividually, command = check_numList_wrapper,
                                                          labelWidth = 0, entryWidth = 15)],fieldEntryList=weightsEntryList)
    weightsEntryList[0].bind('<Return>', lambda *args: g.setParam("weights",['all',float(weightSetAllNum.get())]))
    weightsEntryList[1].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(weightsRandomMin.get()), float(weightsRandomMax.get())]))
    weightsEntryList[2].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(weightsRandomMin.get()), float(weightsRandomMax.get())]))
    weightsEntryList[3].bind('<Return>', lambda *args: util.SendParams(param='weights', type='setIndividually', value=weightsSetIndividually.get(), convertToFloats=True))
    util.ToggleWeightsEntries(weightsEntryList, active=[0])

    nbRow += 1
    lRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
    lRateNum = tk.StringVar()
    lRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent = lRateFrame, text = 'Learning Rate', column = 0, row = nbRow, 
                                                          sticky = sticky, variable = lRateNum, command = check_num_wrapper,
                                                          labelWidth = 12, entryWidth = 15)])
    lRateEntry.bind('<Return>', lambda *args: g.setParam("learningRate",[float(lRateNum.get())]))
    lRateDecreaseBool = tk.IntVar(value=0)
    lRateStartNum = tk.StringVar()
    lRateEndNum = tk.StringVar()
    lRateFieldList = []
    lRateDecreaseCheckBox = tk.Checkbutton(lRateFrame, text="Decrease Learning Rate:", variable=lRateDecreaseBool, 
                            command=lambda *args: util.CreateEntry([util.Tkinter_Field_Settings(parent = lRateFrame, text = 'Start', 
                                                                                           column = 3, row = nbRow-1, sticky = sticky, 
                                                variable = lRateStartNum, command = check_num_wrapper, entry = lRateEntry, labelWidth = 4), 
                                                               util.Tkinter_Field_Settings(parent = lRateFrame, text = 'End', 
                                                                                           column = 5, row = nbRow-1, sticky = sticky, 
                                                variable = lRateEndNum, command = check_num_wrapper, entry = lRateEntry, labelWidth = 3)], 
                                                              lRateDecreaseBool.get(), lRateFieldList, lRateEntry))
    lRateDecreaseCheckBox.grid(column=2, row=nbRow, sticky=sticky, padx=15)

    nbRow += 1
    decayRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=10, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
    decayRateNum = tk.StringVar()
    decayRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=decayRateFrame, text='Decay Rate', column=0, row=nbRow, sticky=sticky, 
                                                              variable=decayRateNum, command=check_num_wrapper)])
    decayRateEntry.bind('<Return>', lambda *args: g.setParam("decayRate", float(decayRateNum.get())))
    decayRateRadio = tk.StringVar()
    decayRateRadioList = []
    decayOptions = {'L1' : 'L1',
                    'L2' : 'L2',
                    'Static' : 'Static',
                    'No Decay' : 'NoDecay'}
    decayColumn = 2
    for (text, value) in decayOptions.items():
        r = tk.Radiobutton(
            decayRateFrame, text=text, value=value, variable=decayRateRadio, command=lambda *args: g.setParam('decayType', decayRateRadio.get()))
        r.grid(column = decayColumn, row = nbRow, sticky = sticky, padx = 15)
        decayColumn += 1
    # util.CreateRadio_setParam(util.Tkinter_Field_Settings(parent=decayRateFrame, dictionary=decayOptions, parameter='decayType', radioVariable=decayRateRadio, variableDefault='NoDecay', 
    #                                                  variable=[decayRateNum], column=2, row=nbRow, sticky=sticky, padx=15, _list=decayRateRadioList))
    #decayRateRadioList[0].config(command=lambda *args: g.setParam('decayType','L1'))
    decayRateRadio.set('NoDecay')

    nbRow += 1
    totalIterationsNum = tk.StringVar()
    totalIterationsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
    totalIterationsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=totalIterationsFrame, text='Total Iterations', column=0, row=nbRow, sticky=sticky, 
                                                              variable=totalIterationsNum)])

    nbRow += 1
    epochsNum = tk.StringVar(value = g.epoch)
    epochsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=nbRow, sticky=sticky))
    epochsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=totalIterationsFrame, text='Epochs', column=0, row=nbRow, sticky=sticky, 
                                                              variable=epochsNum, command = check_num_wrapper)])

    #ADVANCED SETTINGS:
    maxColumn = 3
    maxRow = 1
    nbRow = 0

    thresholdNum = tk.StringVar(value = g.comparisonThreshold)
    thresholdFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    thresholdEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=thresholdFrame, text='Threshold', column=1, row=nbRow, sticky=sticky, 
                                                              variable=thresholdNum, command = check_num_wrapper)])
    thresholdEntry.bind('<Return>', lambda *args: g.setParam("threshold", float(thresholdNum.get())))
    
    nbRow += 1
    featureSetFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    wrapLength=300
    featureInputFile = tk.Label(featureSetFrame, text='Feature Set File')
    featureInputFile.grid(column=0, row=nbRow, sticky=sticky)
    featureMessage = tk.StringVar()
    featureInputButton = tk.Button(featureSetFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('featureSet', featureMessage)) 
    featureInputButton.grid(column=1, row=nbRow, sticky=sticky)
    featureInputMessage = tk.Label(featureSetFrame, textvariable=featureMessage, wraplength=wrapLength)
    featureInputMessage.grid(column=2, row=nbRow, sticky=sticky)

    nbRow += 1
    genCandidatesFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    genCandidatesBool = tk.BooleanVar()
    genCandidatesBool.set(g.generateCandidates)
    genCandidatesCheckBox = tk.Checkbutton(genCandidatesFrame, text="Generate Candidates:", variable=genCandidatesBool, 
                                           command=lambda *args: g.setParam("generateCandidates", value=genCandidatesBool.get()))
    genCandidatesCheckBox.grid(column=0, row=nbRow, sticky=sticky)

    nbRow += 1
    constraintsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    constraintsInputFile = tk.Label(constraintsFrame, text='Constraints Set File')
    constraintsInputFile.grid(column=0, row=nbRow, sticky=sticky)
    constraintsMessage = tk.StringVar()
    constraintsInputButton = tk.Button(constraintsFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('constraints', constraintsMessage)) 
    constraintsInputButton.grid(column=1, row=nbRow, sticky=sticky)
    constraintsInputMessage = tk.Label(constraintsFrame, textvariable=constraintsMessage, wraplength=wrapLength)
    constraintsInputMessage.grid(column=2, row=nbRow, sticky=sticky)

    nbRow += 1
    addViolationsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    addViolationsBool = tk.BooleanVar()
    addViolationsBool.set(g.addViolations)
    addViolationsCheckBox = tk.Checkbutton(addViolationsFrame, text="Add Violations:", variable=addViolationsBool, 
                                           command=lambda *args: g.setParam("addViolations", value=addViolationsBool.get()))
    addViolationsCheckBox.grid(column=0, row=nbRow, sticky=sticky)

    nbRow += 1
    verboseOutputFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, 
                                                                      column=0, row=nbRow, sticky=sticky))
    verboseOutputBool = tk.BooleanVar()
    verboseOutputBool.set(g.noisy)
    verboseOutputCheckBox = tk.Checkbutton(verboseOutputFrame, text="Verbose Console Output:", variable=verboseOutputBool, 
                                           command=lambda *args: g.setParam("noisy", value=verboseOutputBool.get()))
    verboseOutputCheckBox.grid(column=0, row=nbRow, sticky=sticky)

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
    paramsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=width, height=height))

    paramsNotebook = ttk.Notebook(paramsFrame)
    paramsNotebook.pack(fill='both', expand=True)
    paramsNotebook.pressed_index = None
    
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
    listingContentFrame = tk.Frame(master=paramsNotebook)
    listingContentFrame.pack(fill='both', expand=True)

    indexationContentFrame = tk.Frame(master=paramsNotebook)
    indexationContentFrame.pack(fill='both', expand=True)

    rstContentFrame = tk.Frame(master=paramsNotebook)
    rstContentFrame.pack(fill='both', expand=True)

    #Adding notebook tabs
    paramsNotebook.add(listingContentFrame, text='Listing')
    paramsNotebook.add(indexationContentFrame, text='Indexation')
    paramsNotebook.add(rstContentFrame, text='Representational Strength Theory')

    #Creating canvases
    listingCanvas = tk.Canvas(listingContentFrame, width=width, height=height)
    listingScroll = tk.Scrollbar(listingContentFrame, command=listingCanvas.yview)
    listingCanvas.config(yscrollcommand=listingScroll.set, scrollregion=(0,0,width, 300))
    listingCanvas.pack(side='left', fill='both', expand=True)
    listingScroll.pack(side='right', fill='y')

    indexationCanvas = tk.Canvas(indexationContentFrame, width=width, height=height)
    indexationScroll = tk.Scrollbar(indexationContentFrame, command=indexationCanvas.yview)
    indexationCanvas.config(yscrollcommand=indexationScroll.set, scrollregion=(0,0,width, 300))
    indexationCanvas.pack(side='left', fill='both', expand=True)
    indexationScroll.pack(side='right', fill='y')

    rstCanvas = tk.Canvas(rstContentFrame, width=width, height=height)
    rstScroll = tk.Scrollbar(rstContentFrame, command=rstCanvas.yview)
    rstCanvas.config(yscrollcommand=rstScroll.set, scrollregion=(0,0,width, 300))
    rstCanvas.pack(side='left', fill='both', expand=True)
    rstScroll.pack(side='right', fill='y')

    #Creating frames that live inside the canvas
    listingFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky='NEW', width=sizex, height=sizey))
    # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
    # listingFrame.bind('<Enter>', lambda event, canvas=listingCanvas: util.onMouseWheel(canvas, event=event))
    listingCanvas.create_window(10, 10, anchor='nw', window=listingFrame)

    indexationFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky='NEW', width=sizex, height=sizey))
    # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
    # indexationFrame.bind('<Enter>', lambda event, canvas=indexationCanvas: util.onMouseWheel(canvas, event=event))
    indexationCanvas.create_window(10, 10, anchor='nw', window=indexationFrame)

    rstFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=rstCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky='NEW', width=sizex, height=sizey))
    # SOMEDAY GET MOUSEWHEEL SCROLLING WORKING
    # rstFrame.bind('<Enter>', lambda event, canvas=rstCanvas: util.onMouseWheel(canvas, event=event))
    rstCanvas.create_window(10, 10, anchor='nw', window=rstFrame)
    
    sticky = 'NW'
    
    #Listing Frame:
    nbRow = 0
    listingTypeFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    listedLabel = tk.Label(listingTypeFrame, anchor='nw', text='Listed Type:')
    listedLabel.grid(column=0, row=nbRow, sticky = sticky)
    listedTypeRateRadio = tk.StringVar(value=g.useListedType)
    listedTypeRateRadioList = []
    listedTypeOptions = {'Hidden Structure' : 'hidden_structure',
                    'Sample Using Frequency' : 'sample_using_frequency',
                    'Sample Flat Rate' : 'sample_flat_rate',
                    'None' : 'none'}
    listedTypeDescriptions = ['desc 1',
                              'desc 2',
                              'desc 3',
                              'desc 4']
    listedTypeColumn = 1
    row = nbRow
    i = 0
    for (text, value) in listedTypeOptions.items():
        r = tk.Radiobutton(
            listingTypeFrame, text=text, value=value, variable=listedTypeRateRadio, command=lambda *args: g.setParam('useListedType', listedTypeRateRadio.get()))
        r.grid(column = listedTypeColumn, row = row, sticky = sticky, padx = 15)
        listedDescLabel = tk.Label(listingTypeFrame, anchor='nw', text=listedTypeDescriptions[i])
        listedDescLabel.grid(column=listedTypeColumn +1, row=row, sticky = sticky)
        row += 1
        i += 1

    nbRow += row
    listingRateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    listedRateNum = tk.StringVar(value=g.useListedRate)
    listedRateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=listingRateFrame, text='Listed Rate', column=0, row=nbRow, sticky=sticky, 
                                                              variable=listedRateNum, command = check_num_0to1_wrapper)])
    listedRateEntry.bind('<Return>', lambda *args: g.setParam('useListedRate', float(listedRateNum.get())))

    nbRow += 1
    flipFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    flipBool = tk.BooleanVar()
    flipBool.set(g.flip)
    flipCheckBox = tk.Checkbutton(flipFrame, text="Flip:", variable=flipBool, 
                                           command=lambda *args: g.setParam("flip", value=flipBool.get()))
    flipCheckBox.grid(column=0, row=nbRow, sticky=sticky)

    nbRow += 1
    simpleListingFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    simpleListingBool = tk.BooleanVar()
    simpleListingBool.set(g.simpleListing)
    simpleListingCheckBox = tk.Checkbutton(simpleListingFrame, text="Simple Listing:", variable=simpleListingBool, 
                                           command=lambda *args: g.setParam("simpleListing", value=simpleListingBool.get()))
    simpleListingCheckBox.grid(column=0, row=nbRow, sticky=sticky)

    nbRow += 1
    pToListFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=listingFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    pToListNum = tk.StringVar(value=g.pToList)
    pToListEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=pToListFrame, text='pToList', column=0, row=nbRow, sticky=sticky, 
                                                              variable=pToListNum, command = check_num_0to1_wrapper)])
    pToListEntry.bind('<Return>', lambda *args: g.setParam('pToList', float(pToListNum.get())))

    #Indexation Frame:
    nbRow = 0
    nLexCsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    nLexCsNum = tk.StringVar(value=g.lexC_type)
    nLexCsEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=nLexCsFrame, text='nLexCs', column=0, row=nbRow, 
                                                           sticky=sticky, labelWidth=18, 
                                                              variable=nLexCsNum, command = check_num_wrapper)])
    nLexCsEntry.bind('<Return>', lambda *args: g.setParam('nLexCs', float(nLexCsNum.get())))

    nbRow += 1
    pChangeIndexationFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    pChangeIndexationNum = tk.StringVar(value=g.pChangeIndexation)
    pChangeIndexationEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=pChangeIndexationFrame, text='pChangeIndexation', column=0, 
                                                                      row=nbRow, sticky=sticky, labelWidth=18, 
                                                              variable=pChangeIndexationNum, command = check_num_0to1_wrapper)])
    pChangeIndexationEntry.bind('<Return>', lambda *args: g.setParam('pChangeIndexation', float(pChangeIndexationNum.get())))

    nbRow += 1
    lexCStartWFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, 
                                                              maxRow=maxRow, column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    lexCStartWNum = tk.StringVar(value=g.lexCStartW)
    lexCStartWEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=lexCStartWFrame, text='lexCStartW', column=0, row=nbRow, 
                                                               sticky=sticky, labelWidth=18, 
                                                              variable=lexCStartWNum, command = check_num_wrapper)])
    lexCStartWEntry.bind('<Return>', lambda *args: g.setParam('lexCStartW', float(lexCStartWNum.get())))

    nbRow += 1
    localityFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    localityLabel = tk.Label(localityFrame, anchor='nw', text='Locality:')
    localityLabel.grid(column=0, row=nbRow, sticky = sticky)
    localityRateRadio = tk.StringVar(value=g.localityRestrictionType)
    localityRateRadioList = []
    localityOptions = {'Overlap' : 'overlap',
                    'Presence Only' : 'presence_only',
                    'Strict' : 'strict'}
    localityDescriptions = ['desc 1',
                              'desc 2',
                              'desc 3']
    localityColumn = 1
    row = nbRow
    i = 0
    for (text, value) in localityOptions.items():
        r = tk.Radiobutton(
            localityFrame, text=text, value=value, variable=localityRateRadio, command=lambda *args: g.setParam('locality', localityRateRadio.get()))
        r.grid(column = localityColumn, row = row, sticky = sticky, padx = 15)
        localityDescLabel = tk.Label(localityFrame, anchor='nw', text=localityDescriptions[i])
        localityDescLabel.grid(column=localityColumn +1, row=row, sticky = sticky)
        row += 1
        i += 1
    
    ## FIRST INDEX STRAT NOT FULLY IMPLEMENTED YET
    # nbRow += 1
    # firstIndexStratFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=indexationFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
    #                            column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    # firstIndexStratLabel = tk.Label(firstIndexStratFrame, anchor='nw', text='First Index Strat:')
    # firstIndexStratLabel.grid(column=0, row=nbRow, sticky = sticky)
    firstIndexStratRateRadio = tk.StringVar(value=g.firstIndexStrat)
    # firstIndexStratRateRadioList = []
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
    #         firstIndexStratFrame, text=text, value=value, variable=firstIndexStratRateRadio, command=lambda *args: g.setParam('first_index_strategy', firstIndexStratRateRadio.get()))
    #     r.grid(column = firstIndexStratColumn, row = row, sticky = sticky, padx = 15)
    #     firstIndexStratDescLabel = tk.Label(firstIndexStratFrame, anchor='nw', text=firstIndexStratDescriptions[i])
    #     firstIndexStratDescLabel.grid(column=firstIndexStratColumn +1, row=row, sticky = sticky)
    #     row += 1
    #     i += 1
    
    #rst Frame:
    nbRow = 0
    PFC_typeFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    PFC_typeLabel = tk.Label(PFC_typeFrame, anchor='nw', text='PFC Type:')
    PFC_typeLabel.grid(column=0, row=nbRow, sticky = sticky)
    PFC_typeRateRadio = tk.StringVar(value=g.PFC_type)
    PFC_typeRateRadioList = []
    PFC_typeOptions = {'None' : 'none',
                    'Pseudo' : 'pseudo',
                    'Full' : 'full'}
    PFC_typeDescriptions = ['desc 1',
                              'desc 2',
                              'desc 3']
    PFC_typeColumn = 1
    row = nbRow
    i = 0

    for (text, value) in PFC_typeOptions.items():
        r = tk.Radiobutton(
            PFC_typeFrame, text=text, value=value, variable=PFC_typeRateRadio, command=lambda *args: g.setParam('PFC_type', PFC_typeRateRadio.get()))
        r.grid(column = PFC_typeColumn, row = row, sticky = sticky, padx = 15)
        PFC_typeDescLabel = tk.Label(PFC_typeFrame, anchor='nw', text=PFC_typeDescriptions[i])
        PFC_typeDescLabel.grid(column=PFC_typeColumn +1, row=row, sticky = sticky)
        row += 1
        i += 1
    
    nbRow += 1
    PFC_lrateFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    PFC_lrateNum = tk.StringVar(value=g.PFC_lrate)
    PFC_lrateEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=PFC_lrateFrame, text='PFC Learning Rate', column=0, row=nbRow, 
                                                              sticky=sticky, labelWidth=18, 
                                                              variable=PFC_lrateNum, command = check_num_wrapper)])
    PFC_lrateEntry.bind('<Return>', lambda *args: g.setParam('PFC_lrate', float(PFC_lrateNum.get())))

    nbRow += 1
    PFC_startWFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=rstFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=nbRow, sticky='NEW', width=sizex, height=sizey))
    PFC_startWNum = tk.StringVar(value=g.PFC_startW)
    PFC_startWEntry = util.CreateEntry([util.Tkinter_Field_Settings(parent=PFC_startWFrame, text='PFC Starting Weight', column=0, row=nbRow, 
                                                               sticky=sticky, labelWidth=18,
                                                              variable=PFC_startWNum, command = check_num_wrapper)])
    PFC_startWEntry.bind('<Return>', lambda *args: g.setParam('PFC_startW', float(PFC_startWNum.get())))

    #DATA FILE SELECTION
    gridRow += 1
    maxColumn = 3
    maxRow = 3
    folderFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=600, height=75))
    
    # ttk.Frame(frame, borderwidth=0, width=600, height=75)
    # folderFrame.grid(column=0, row=2, columnspan=3, sticky=sticky)
    wrapLength=300
    inputFile = tk.Label(folderFrame, text='Training Data File')
    inputFile.grid(column=0, row=gridRow, sticky=sticky)
    message = tk.StringVar()
    inputButton = tk.Button(folderFrame, width=15, text='Select File', command=lambda *args : util.ReadTrainingData('trainingData', message)) 
    inputButton.grid(column=1, row=gridRow, sticky=sticky)
    inputMessage = tk.Label(folderFrame, textvariable=message, wraplength=wrapLength)
    inputMessage.grid(column=2, row=gridRow, sticky=sticky)

    gridRow += 1
    outputFolder = tk.Label(folderFrame, text='Output Folder')
    outputFolder.grid(column=0, row=gridRow, sticky=sticky)
    outputPath = tk.StringVar()
    outputFolderButton = tk.Button(folderFrame, width=15, text='Select Folder', command=lambda *args : util.GetDirectory(outputPath)) 
    outputFolderButton.grid(column=1, row=gridRow, sticky=sticky)
    outputFolderName = tk.Label(folderFrame, textvariable=outputPath, wraplength=wrapLength)
    outputFolderName.grid(column=2, row=gridRow, sticky=sticky)
    
    # REPORTING PARAMS
    #   
    #SAVE SETTINGS
    gridRow += 1
    maxColumn = 2
    maxRow = 3
    saveSettingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=600, height=200))

    saveRow = 0
    saveSettingsLabel = tk.Label(saveSettingsFrame, text='Save:')
    saveSettingsLabel.grid(column=0, row=saveRow, sticky=sticky)

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
                     'Phonological Form Constraints': tk.BooleanVar(value=g.save_PFCs),
                     'Learned Lexicon': tk.BooleanVar(value=g.save_actualLexicon)
                     }
    for option, value in saveTypesDict.items():
        check_button = tk.Checkbutton(saveSettingsFrame, text=option, variable=value, command=lambda *args: util.SendDictionary('filesToSave',saveTypesDict))
        check_button.grid(column=gridColumn, row=saveRow, sticky=sticky)
        saveRow += 1
        if saveRow - startRow > maxRows:
            saveRow = startRow
            gridColumn += 1
    
    #LEARN  & VALIDATE BUTTONS
    gridRow += 1
    val_Learn_Frame = util.CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=600, height=200))
    # validateDict = {
    #     'weights': ,

    #     }
    validateButton = tk.Button(val_Learn_Frame, width=15, text='Validate')
    validateButton.place(anchor='center')
    validateButton.grid(column=0, row=gridRow, padx=12, pady=12, sticky=sticky)
    # collect all params and values in a dictionary and iterate through it and call setParam for each param / value pair

    learnButton = tk.Button(val_Learn_Frame, width=15, text='Learn')
    learnButton.place(anchor='center')
    learnButton.grid(column=2, row=gridRow, padx=12, pady=12, sticky=sticky)

    # sample code for validating:
    # for i in entries:
    #    result = g.setParam(parameter,value)
    #    if result:   
    #          it's an error or warning
# def util.SendParams():
#     if weightsRadioVar == 'all':
#         weightsEntryList
    

def OutputFrame(frame):
    frame.grid(column=3, row=0, columnspan=3, sticky='NSEW')

def ConsoleFrame(frame):
    frame.grid(column=3, row=1, columnspan=3, sticky='NSEW')



# Setting some window properties
root.title('GLaPL')
root.configure(background='grey')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.minsize(1280, 720)
root.maxsize(screen_width, screen_height)
root.geometry('300x300+50+50')

# Root Grid
content = util.CreateFrame(util.Tkinter_Field_Settings(root, ipadx = 6, ipady = 6, width=screen_width, height=screen_height))
settingsFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge', maxColumn=1, maxRow=1, columnSpan=1, rowSpan= 2))
outputFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge'))
consoleFrame = util.CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge'))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Configuring columns and rows to scale with the window
maxColumn = 6
maxRow = 2
for i in range(maxColumn):
    content.columnconfigure(i, weight=1)
for i in range(maxRow):
    content.rowconfigure(i, weight=1)
content.grid(column=0, row=0, sticky='NSEW')




#Settings Frame:
SettingsFrame(settingsFrame)

#Output Frame:
OutputFrame(outputFrame)

#Console Frame:
ConsoleFrame(consoleFrame)



root.mainloop()

#g = l.Grammar()

### run to package as one file - takes longer to load, 
### but easier to distribute
### pyinstaller --onefile app.py

