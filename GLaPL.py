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
import learner as l
import GLaPLUtilities as util


root = tk.Tk()
check_num_wrapper = (root.register(util.CheckNum),'%P')
check_numList_wrapper = (root.register(util.CheckNumList),'%P')

g = l.Grammar()

def show_selected(values):
    selected_options = []
    for option, value in values.items():
        if value.get() == 1:
            selected_options.append(option)
    print("Selected options:", selected_options)

def CreateEntry(args, b = None, fieldList = None, greyOut = None, fieldEntryList = None):
    if (b == 0):
        i = len(fieldList) - 1
        while i >= 0:
            fieldList[i].destroy()
            fieldList.remove(fieldList[i])
            i = i - 1
        greyOut.config(state = tk.NORMAL)
    else:
        for arg in args:
            fieldLabel = tk.Label(arg.parent, text = arg.text, width = arg.labelWidth, anchor='nw')
            fieldLabel.grid(column = arg.column, row = arg.row, sticky = arg.sticky, padx = arg.padx, ipadx = arg.ipadx, pady = arg.pady, ipady = arg.ipady)
            fieldEntry = tk.Entry(arg.parent, textvariable = arg.variable, validate = 'key', validatecommand = arg.command, width = arg.entryWidth)
            fieldEntry.grid(column = arg.column +1, row = arg.row, sticky = arg.sticky, padx = arg.padx, ipadx = arg.ipadx, pady = arg.pady, ipady = arg.ipady)
            if fieldEntryList is not None:
                if fieldEntry not in fieldEntryList:
                    fieldEntryList.append(fieldEntry)
            if fieldList is not None:
                if fieldLabel not in fieldList:
                    fieldList.append(fieldLabel)
                if fieldEntry not in fieldList:
                    fieldList.append(fieldEntry)
        if greyOut is not None:
            greyOut.config(state = tk.DISABLED, disabledbackground = 'grey')
        return fieldEntry
    
def CreateFrame(arg):
    frame = tk.Frame(arg.parent, borderwidth=arg.borderWidth, width=arg.width, height=arg.height, relief=arg.relief)
    for i in range(arg.maxColumn):
        frame.columnconfigure(i, weight=arg.weightx)
    for i in range(arg.maxRow):
        frame.rowconfigure(i, weight=arg.weighty)
    frame.grid(column=arg.column, row=arg.row, columnspan=arg.columnSpan, rowspan=arg.rowSpan, sticky=arg.sticky, 
               padx = arg.padx, pady=arg.pady, ipadx=arg.ipadx, ipady=arg.ipady)
    return frame
def ToggleWeightsEntries(fieldList, active):
    for i in range(len(fieldList)):
        if any(x == i for x in active):
            fieldList[i].config(state = tk.NORMAL)
        else:
            fieldList[i].config(state = tk.DISABLED)
#not used - removing the command line prevents setting a default, it's also not able to intelligently not send a list for the values.
def CreateRadio_setParam(args, expandX = bool(True)):
    listItem = 0
    print(args)
    column = args.column
    row = args.row
    parameter = args.parameter
    _list = args.list
    for (text, value) in args.dictionary.items():
        print(text, value)
        commandVariable=args.variable[listItem]
        variable=args.radioVariable
        r = tk.Radiobutton(
            args.parent,
            text=text,
            value=value,
            variable=variable,
            command=lambda *args: g.setParam(parameter, [variable.get(), commandVariable]))
        r.grid(column=column, row=row, sticky=args.sticky, padx = args.padx, pady=args.pady, ipadx = args.ipadx, ipady = args.ipady)
        #find a solution for passing two variables through
        if (len(args.variable) > 1):
            listItem += 1
        if (expandX == True):
            column += 1
        else:
            row += 1
        _list.append(r)

def SendParams(param, type, value, convertToFloats = False):
    if convertToFloats == True:
        value = value.split(",")
    g.setParam(param, [type, value])

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def SettingsFrame(frame):

    # CONTENT SETTINGS
    sticky = 'NSEW'
    maxColumn = 8
    maxRow = 10
    column = 0
    gridRow = 0
    width = 680
    contentSettingsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=frame, maxColumn=maxColumn, columnSpan=3, 
                                                                   maxRow=maxRow, column=column, row=gridRow, sticky=sticky, pady = 5, height=680))
    sticky = 'NW'
    maxColumn = 1
    maxRow = 1
    column = 0
    gridRow = 0
    height = 80
    settingsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=width, height=height))

    settingsNotebook = ttk.Notebook(settingsFrame)
    settingsNotebook.grid(column=0, row=0, sticky=sticky)
    
    generalCanvas = tk.Canvas(settingsFrame, scrollregion=(0,0,100, 100))
    generalCanvas.grid(column=0, row=0, sticky=sticky)

    sticky = 'NW'
    maxColumn = 8
    maxRow = 1
    column = 0
    gridRow = 0
    height = 0
    sizex = 0
    sizey = 0
    settingsNotebook.identify(x= sizex, y= sizey)
    generalFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalCanvas, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=sizex, height=sizey))
    advancedFrame = CreateFrame(util.Tkinter_Field_Settings(parent=settingsFrame, maxColumn=maxColumn, columnSpan= maxColumn, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=sizex, height=sizey))

    settingsNotebook.add(generalCanvas, text='General Settings')
    settingsNotebook.add(advancedFrame, text='Advanced Settings')
    generalSettingsScroll = tk.Scrollbar(contentSettingsFrame,orient='vertical')
    generalSettingsScroll.config(command=generalCanvas.yview)
    generalSettingsScroll.grid(column=maxColumn, row=0, sticky='NS')
    generalCanvas.config(yscrollcommand=generalSettingsScroll.set)
    generalCanvas.create_window((10,10), window=generalFrame, anchor='nw')
    generalFrame.bind("<Configure>", lambda event, canvas=generalCanvas: onFrameConfigure(canvas))
    sticky = 'NW'
    gridRow = 0
    
    # Starting weights should wind up as one of the following:
    # ('all',0.0)  <- set all constraints to a specific weight
    # ('rand',0.0,10.0)  <- randomize between 0 and 10
    # ('setIndividually', [0.0,1.0,3.1,1.2,2.0]) <- set a start weight for each constraint

    

    # GENERAL SETTINGS:
    weightsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=5, maxRow=3, columnSpan=8, column=0, row=gridRow, sticky=sticky))
    weightsLabel = tk.Label(weightsFrame, anchor='nw', text='Starting Weights')
    weightsLabel.grid(column = 0, row=gridRow, sticky=sticky)
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
            weightsFrame, text=text, value=value, variable=weightsRadioVar, command=lambda *args: SendParams('weights', weightsRadioVar, weightsVarList[weightRadioCount]))
        r.grid(column = 2, row=gridRow, sticky=sticky, padx=15)
        weightsRadioList.append(r)
        gridRow += 1
        rowCount += 1
        weightRadioCount += 1
    weightsRadioVar.set('all')
    
    weightsRadioList[0].config(command=lambda *args: ToggleWeightsEntries(weightsEntryList, active=[0]))
    weightsRadioList[1].config(command=lambda *args: ToggleWeightsEntries(weightsEntryList, active=[1,2]))
    weightsRadioList[2].config(command=lambda *args: ToggleWeightsEntries(weightsEntryList, active=[3]))
    gridRow -= rowCount
    weightsEntryList = []
    weightsEntry = CreateEntry([util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = gridRow, 
                                                          sticky = sticky, variable = weightSetAllNum, command = check_num_wrapper,
                                                          labelWidth = 0, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = gridRow +1, 
                                                          sticky = sticky, variable = weightsRandomMin, command = check_num_wrapper,
                                                          labelWidth = 0, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, text = 'and', column = 5, row = gridRow +1, 
                                                          sticky = sticky, variable = weightsRandomMax, command = check_num_wrapper,
                                                          labelWidth = 3, entryWidth = 15),
                                util.Tkinter_Field_Settings(parent = weightsFrame, column = 3, row = gridRow +2, pady=5,
                                                          sticky = sticky, variable = weightsSetIndividually, command = check_numList_wrapper,
                                                          labelWidth = 0, entryWidth = 15)],fieldEntryList=weightsEntryList)
    weightsEntryList[0].bind('<Return>', lambda *args: g.setParam("weights",['all',float(weightSetAllNum.get())]))
    weightsEntryList[1].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(weightsRandomMin.get()), float(weightsRandomMax.get())]))
    weightsEntryList[2].bind('<Return>', lambda *args: g.setParam("weights",['rand',float(weightsRandomMin.get()), float(weightsRandomMax.get())]))
    weightsEntryList[3].bind('<Return>', lambda *args: SendParams(param='weights', type='setIndividually', value=weightsSetIndividually.get(), convertToFloats=True))
    ToggleWeightsEntries(weightsEntryList, active=[0])

    gridRow += 1
    lRateFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=gridRow, sticky=sticky))
    lRateNum = tk.StringVar()
    lRateEntry = CreateEntry([util.Tkinter_Field_Settings(parent = lRateFrame, text = 'Learning Rate', column = 0, row = gridRow, 
                                                          sticky = sticky, variable = lRateNum, command = check_num_wrapper,
                                                          labelWidth = 12, entryWidth = 15)])
    lRateEntry.bind('<Return>', lambda *args: g.setParam("learningRate",[float(lRateNum.get())]))
    lRateDecreaseBool = tk.IntVar(value=0)
    lRateStartNum = tk.StringVar()
    lRateEndNum = tk.StringVar()
    lRateFieldList = []
    lRateDecreaseCheckBox = tk.Checkbutton(lRateFrame, text="Decrease Learning Rate:", variable=lRateDecreaseBool, 
                            command=lambda *args: CreateEntry([util.Tkinter_Field_Settings(parent = lRateFrame, text = 'Start', column = 3, row = gridRow, sticky = sticky, 
                                                variable = lRateStartNum, command = check_num_wrapper, entry = lRateEntry, labelWidth = 4), 
                                                               util.Tkinter_Field_Settings(parent = lRateFrame, text = 'End', column = 5, row = gridRow, sticky = sticky, 
                                                variable = lRateEndNum, command = check_num_wrapper, entry = lRateEntry, labelWidth = 3)], 
                                                              lRateDecreaseBool.get(), lRateFieldList, lRateEntry))
    lRateDecreaseCheckBox.grid(column=2, row=gridRow, sticky=sticky, padx=15)

    gridRow += 1
    decayRateFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=10, columnSpan= 8, maxRow=1, column=0, row=gridRow, sticky=sticky))
    decayRateNum = tk.StringVar()
    decayRateEntry = CreateEntry([util.Tkinter_Field_Settings(parent=decayRateFrame, text='Decay Rate', column=0, row=gridRow, sticky=sticky, 
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
        r.grid(column = decayColumn, row = gridRow, sticky = sticky, padx = 15)
        decayColumn += 1
    # CreateRadio_setParam(util.Tkinter_Field_Settings(parent=decayRateFrame, dictionary=decayOptions, parameter='decayType', radioVariable=decayRateRadio, variableDefault='NoDecay', 
    #                                                  variable=[decayRateNum], column=2, row=gridRow, sticky=sticky, padx=15, _list=decayRateRadioList))
    #decayRateRadioList[0].config(command=lambda *args: g.setParam('decayType','L1'))
    decayRateRadio.set('NoDecay')

    gridRow += 1
    totalIterationsNum = tk.StringVar()
    totalIterationsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=gridRow, sticky=sticky))
    totalIterationsEntry = CreateEntry([util.Tkinter_Field_Settings(parent=totalIterationsFrame, text='Total Iterations', column=0, row=gridRow, sticky=sticky, 
                                                              variable=totalIterationsNum)])

    gridRow += 1
    epochsNum = tk.StringVar()
    epochsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=generalFrame, maxColumn=2, columnSpan= 8, maxRow=1, column=0, row=gridRow, sticky=sticky))
    epochsEntry = CreateEntry([util.Tkinter_Field_Settings(parent=totalIterationsFrame, text='Epochs', column=0, row=gridRow, sticky=sticky, 
                                                              variable=epochsNum, command = check_num_wrapper)])

    #ADVANCED SETTINGS:
    maxColumn = 3
    maxRow = 1
    advancedRow = 0
    featureSetFrame = CreateFrame(util.Tkinter_Field_Settings(parent=advancedFrame, maxColumn=maxColumn, columnSpan= 8, maxRow=maxRow, 
                                                                      column=0, row=advancedRow, sticky=sticky))
    wrapLength=300
    inputFile = tk.Label(featureSetFrame, text='Feature Set File')
    inputFile.grid(column=0, row=gridRow, sticky=sticky)
    message = tk.StringVar()
    inputButton = tk.Button(featureSetFrame, width=15, text='Select File', command=lambda *args : readTrainingData(message)) 
    inputButton.grid(column=1, row=gridRow, sticky=sticky)
    inputMessage = tk.Label(featureSetFrame, textvariable=message, wraplength=wrapLength)
    inputMessage.grid(column=2, row=gridRow, sticky=sticky)

    advancedRow += 1

    #LISTING & INDEXATION
    gridRow = 1
    maxColumn = 1
    maxRow = 1
    listing_indexationFrame = CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 8, maxRow=maxRow, 
                                                                      column=0, row=gridRow, sticky=sticky))

    paramsNotebook = ttk.Notebook(listing_indexationFrame)
    paramsNotebook.grid(column=0, row=0, sticky=sticky)

    listingFrame = CreateFrame(util.Tkinter_Field_Settings(parent=listing_indexationFrame, maxColumn=maxColumn, columnSpan= 8, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=600, height=150))
    indexationFrame = CreateFrame(util.Tkinter_Field_Settings(parent=listing_indexationFrame, maxColumn=maxColumn, columnSpan= 8, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=600, height=150))
    rstFrame = CreateFrame(util.Tkinter_Field_Settings(parent=listing_indexationFrame, maxColumn=maxColumn, columnSpan= 8, maxRow=maxRow, 
                               column=0, row=0, sticky=sticky, width=600, height=150))

    paramsNotebook.add(listingFrame, text='Listing')
    paramsNotebook.add(indexationFrame, text='Indexation')
    paramsNotebook.add(rstFrame, text='Representational Strength Theory')



    #DATA FILE SELECTION
    gridRow += 1
    maxColumn = 3
    maxRow = 3
    folderFrame = CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=600, height=75))
    
    # ttk.Frame(frame, borderwidth=0, width=600, height=75)
    # folderFrame.grid(column=0, row=2, columnspan=3, sticky=sticky)
    wrapLength=300
    inputFile = tk.Label(folderFrame, text='Training Data File')
    inputFile.grid(column=0, row=gridRow, sticky=sticky)
    message = tk.StringVar()
    inputButton = tk.Button(folderFrame, width=15, text='Select File', command=lambda *args : readTrainingData(message)) 
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
    saveSettingsFrame = CreateFrame(util.Tkinter_Field_Settings(parent=contentSettingsFrame, maxColumn=maxColumn, columnSpan= 3, maxRow=maxRow, 
                               column=0, row=gridRow, sticky=sticky, width=600, height=200))

    saveRow = 0
    saveSettingsLabel = tk.Label(saveSettingsFrame, text='Save:')
    saveSettingsLabel.grid(column=0, row=saveRow, sticky=sticky)

    saveRow += 1
    startRow = saveRow
    gridColumn = 0
    maxRows = 2
    saveTypesDict = {'Weights': tk.IntVar(), 
                     'Error rates': tk.IntVar(), 
                     'Tableaux': tk.IntVar(),
                     'Indexation final state': tk.IntVar(), 
                     'Indexed constraints weights over time (by constraint)': tk.IntVar(), 
                     'Indexed constraints weights over time (by lexeme) -- LARGE FILE': tk.IntVar(),
                     'Listing history': tk.IntVar(),
                     'Phonological Form Constraints': tk.IntVar(),
                     'Learned Lexicon': tk.IntVar()
                     }
    for option, value in saveTypesDict.items():
        check_button = tk.Checkbutton(saveSettingsFrame, text=option, variable=value, command=lambda *args: show_selected(saveTypesDict))
        check_button.grid(column=gridColumn, row=saveRow, sticky=sticky)
        saveRow += 1
        if saveRow - startRow > maxRows:
            saveRow = startRow
            gridColumn += 1
    
    #LEARN  & VALIDATE BUTTONS
    gridRow += 1
    validateButton = tk.Button(contentSettingsFrame, width=15, text='Validate')
    validateButton.place(anchor='center')
    validateButton.grid(column=0, row=gridRow, pady=12)
    # collect all params and values in a dictionary and iterate through it and call setParam for each param / value pair

    learnButton = tk.Button(contentSettingsFrame, width=15, text='Learn')
    learnButton.place(anchor='center')
    learnButton.grid(column=2, row=gridRow, pady=12)

    # sample code for validating:
    # for i in entries:
    #    result = g.setParam(parameter,value)
    #    if result:   
    #          it's an error or warning

    

def OutputFrame(frame):
    frame.grid(column=3, row=0, columnspan=3, sticky='NSEW')

def ConsoleFrame(frame):
    frame.grid(column=3, row=1, columnspan=3, sticky='NSEW')

def readTrainingData(m):
    filename = filedialog.askopenfilename()
    print(filename)
    x = g.setParam("trainingData",filename)
    m.set(x)

# Setting some window properties
root.title('GLaPL')
root.configure(background='grey')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.minsize(1280, 720)
root.maxsize(screen_width, screen_height)
root.geometry('300x300+50+50')

# Root Grid
content = CreateFrame(util.Tkinter_Field_Settings(root, ipadx = 6, ipady = 6, width=screen_width, height=screen_height))
settingsFrame = CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge', maxColumn=1, maxRow=1, columnSpan=1, rowSpan= 2))
outputFrame = CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge'))
consoleFrame = CreateFrame(util.Tkinter_Field_Settings(content, borderWidth=5, relief='ridge'))

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

