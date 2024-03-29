#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
from itertools import chain
import itertools
import re
import random
import sys
from colorama import Fore, Back, Style
import importlib
import datetime

class Features:
    def __init__(self, filename, skipChar='x'):
        f = open(filename, "r")
        lines = f.readlines()
        self.filename = filename
        self.featureNames = [i.strip() for i in lines[0].split('\t')[1:]]
        self.featureValues = {}
        self.skipChar = skipChar
        for i in lines[1:]:
            l = [j.strip() for j in i.split('\t')]
            self.featureValues[l[0]] = [val for val in l[1:]]
            # so this is now just numbers AND x's, all as str
            ''' feature value skipChar is treated in this class as 'unspecified' and therefore matches with anything'''
        # Always add morphBoundary as a possible segment.  it is 0 for everything, except the 'morphBoundary' feature
        # TODO revisit whether it is better to store the morpheme boundary differently in some way?
        self.featureNames.append("morphBoundary")
        for seg in self.featureValues:
            self.featureValues[seg].append("0")
        self.featureValues["_"] = [skipChar for i in self.featureNames]
        self.featureValues["_"][-1] = '1'

    # TODO make a str() function

    # TODO check for underspecified segments, or for redundant features

    def exists(self, featureList, add=False):  # a list of tuples of (value,feature)
        '''Checks whether the list of feature values corresponds to a real segment in the feature set.  Returns the label of that feature set, or None if not found'''
        fs = [[str(i) for i, j in featureList if i != self.skipChar],
              [str(j) for i, j in featureList if i != self.skipChar]]
        # This will be [[values],[features]], skipping over 'x' entries
        # skip over 'x' entries
        # create a new version of self.featureValues, pared down to just the features that appear in s
        indices = [self.featureNames.index(f) for f in fs[1]]
        newFeatureValues = [(i, [j[k] for k in indices]) for i, j in self.featureValues.items()]
        segID = [i for i, j in newFeatureValues if j == fs[0]]
        # print(segID) # List of all items corresponding to the given list of features
        if len(segID) == 0:
            if add:
                print("Looks like you've provided a set of features that doesn't correspond to any segment:")
                print([i for i in zip(fs[0], fs[1])])
                choice = input("Would you like to add a segment for this set of features? (y/n)")
                while choice == 'y':
                    segToAdd = input(
                        "Please type the single character you would like to represent this set of features (or press enter to cancel): ")
                    if segToAdd == '':
                        choice == 'n'
                    if choice == 'y' and (segToAdd not in self.featureValues.keys()):
                        newsegFeatureValues = ['x'] * len(self.featureNames)
                        for i in range(len(indices)):
                            newsegFeatureValues[indices[i]] = fs[0][i]
                        self.featureValues[segToAdd] = newsegFeatureValues
                        print('Ok, added!')
                        choice == 'n'

                    else:
                        print("Sorry, ", segToAdd, " is already a phone in your feature set.  Please try another.")
            else:
                return None

        elif len(segID) > 1:
            if add:
                print([i for i in zip(fs[0], fs[1])])
                print("This set of feature values corresponds to multiple segments.  Here they are:")
                print(segID)
                print(
                    "To manually choose one, just type the character for the segment you would like to use (or press enter to return None)")
                choice = input("Please type a choice: ")
                if choice in segID:
                    return choice
                elif choice == '':
                    return None
                else:
                    print("Couldn't interpret your response.  exiting...")
                    return None
            else:  # TODO think about this decision a little more.  Perhaps return the list of possible segments instead?
                return None
        elif len(segID) == 1:
            return segID[0]
        else:
            print("Yikes something has gone horribly wrong!")

    def stringToF(self, string, seglabels=None):
        '''Convert a string to features '''
        '''returns a dictionary with each seg: [list of tuples of (value, feature)] '''
        '''also returns a list, with dictionary keys in order '''
        '''skips _ in segs dictionary, but retains it in segment order'''
        if seglabels:  # Check that seglabels contains only unique values
            if len(seglabels) != len(set(seglabels)):
                seglabels = None
                print(
                    "Warning, seglabels contains non-unique values. stringToF() will now invent segment labels for your string.")
        segs = {}
        order = []
        for i in range(0, len(string)):
            if seglabels:
                k = seglabels[i]
            else:
                k = "seg" + str(i + 1)
            # if string[i]=="_":
            #   segs["_"] = [('1','morphBoundary')] # give this guy a feature
            #   order.append("_")
            # else:
            try:
                segs[k] = [j for j in zip(self.featureValues[string[i]], self.featureNames)]
            except KeyError:
                print('\nERROR: '+string[i]+' does not exist in '+self.filename)
            order.append(k)

        return segs, order

    def featureToS(self, segs, order):
        '''converts a segment dictionary and an ordering to a string '''
        S = []  # in which to store the segments as we find them
        m = 1 # which morpheme are we on (for adding in the _ marker for morpheme boundaries)
        for s in order:  # go through the segment labels in order
            # if s != "_":
            w = re.search("(_w)([0123456789]*)",s)
            if w:
                thisM = int(w.groups()[1]) # what number of morpheme are we on now (number after the '_w' on the seg label)
                if thisM != m:
                    S.append("_")
                    m = thisM

            S.append(self.exists(segs[s], add=True))
        return "".join([str(s) for s in S])


class candidate:
    def __init__(self, c, violations, observedProb, surfaceForm=None):  # removed: activitylevel
        self.c = c  # the actual candidate
        self.surfaceForm = surfaceForm if surfaceForm else re.sub("_","",c)
        self.violations = violations  # list of violations, in same order as constraints
        self.observedProb = observedProb  # The observed probability of the candidate
        try:  # make sure observedProb is a float, or can be converted to float
            self.observedProb = float(self.observedProb)
        except ValueError:
            print(
                "It looks like candidate " + self.c + " has a probability that can't be converted to float.  Check if there's some text in that column of your spreadsheet")
        self.harmony = 0  # Not specified at initialization.     This will be filled out in learning
        self.predictedProb = 0  # Again, to be filled out during learning.

    def copy(self):
        newC = candidate(self.c, self.violations[:], self.observedProb, self.surfaceForm)
        newC.harmony = self.harmony
        newC.predictedProb = self.predictedProb
        return newC

    def toRichCand(self, features):
        segsDict, segsList = features.stringToF(self.c)
        return richCand(self.c, self.violations[:], self.observedProb, segsDict, segsList, surfaceForm=self.surfaceForm)


class richCand(candidate):
    def __init__(self, c, violations, observedProb, segsDict, segsList, segsOrder=None, activitys=None, suprasegmentals=[], surfaceForm=None, operations=None):
        candidate.__init__(self, c, violations, observedProb, surfaceForm)
        self.segsDict = segsDict  # This should be a dictionary with keys for segments, and values that are lists of tuples defining the features of each seg.
        # Example: {seg1: [(0, "front"),(1, "high"),(0,"back"),(0,"low")]}
        self.segsList = segsList  # list of all segments
        self.segsOrder = segsOrder if segsOrder else [i for i in range(1, len(segsList) + 1)]
        # set segsOrder to the order of the segments in segsList if a particular order is not specified
        # TODO think about if there is any circumstance in which this should NOT correspond to the linear order of segsList
        self.activitys = activitys if activitys else [1 for i in segsList]  # set all activitys to 1 by default
        # These should/will only be non-1 values under Zimmerman-style GSRS (Z-GSRs)
        self.suprasegmentals = suprasegmentals
        self.operations = operations if operations else []

    def __repr__(self):
        return "richCand() object: '" + self.c + "'\n" + "attributes: segsDict, segsList, segsOrder, activitys, suprasegmentals, violations, harmony, predictedProb, observedProb, surfaceForm"

    def __str__(self):
        out = "Rich candidate '" + self.c + "'\n" + "Harmony: " + str(self.harmony)
        out += "\n" + "Predicted Probability: " + str(self.predictedProb)
        out += "\n" + "Violations: " + ' '.join([str(i) for i in self.violations]) + '\n\n'
        maxLen = str(max([len(i) for i in self.segsList]))
        segform = ('{:^' + maxLen + 's} ') * len(self.segsList)
        out += segform.format(*self.segsList)
        out += '\n'
        out += segform.format(*[str(i) for i in self.activitys])
        out += '\n'
        out += segform.format(*[str(i) for i in self.segsOrder])
        out += '\n'
        out += '\n'.join([i + ": " + ' '.join([str(k) for k in j]) for i, j in self.segsDict.items()]) + '\n\n'
        out += 'Suprasegmentals:' + '\n' + '\n'.join(
            [str(i) for i in self.suprasegmentals]) if self.suprasegmentals else 'No suprasegmentals'
        return out

    def __eq__(self, other):
        # check segs in order - segnames don't matter
        # check operations applied
        for i in range(0, len(self.segsList)):
            if self.segsDict[self.segsList[i]] != other.segsDict[other.segsList[i]]:
                return 0
        self.operations.sort()
        other.operations.sort()
        if self.operations != other.operations:
            return 0

        return 1


def exampleCand():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg2 = [(1, "back"), (1, "high"), (0, "front"), (0, "low")]  # u
    seg3 = [(1, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg2": seg2, "seg3": seg3}
    order = ["seg1", "seg3", "seg2"]
    suprasegmentals = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return richCand('iau', [1, 0, 1], 1, segs, order, suprasegmentals=suprasegmentals)


def exampleCand22():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg2 = [(1, "back"), (1, "high"), (0, "front"), (0, "low")]  # u
    seg3 = [(1, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg2": seg2, "seg3": seg3}
    order = ["seg1", "seg2", "seg3"]
    suprasegmentals = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return richCand('iau', [1, 0, 1], 1, segs, order, suprasegmentals=suprasegmentals)


def exampleCandDup():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg2 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg3 = [(1, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg2": seg2, "seg3": seg3}
    order = ["seg1", "seg2", "seg3"]
    suprasegmentals = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return richCand('iau', [1, 0, 1], 1, segs, order, suprasegmentals=suprasegmentals)


class Tableau:
    def __init__(self, tag, prob=1, hiddenStructure=False, lexemes=[], w=[], constraintNames=[]):
        self.tag = tag  # Human-readable tag to let the user know which tableau this is
        self.prob = prob  # Corresponds to tab.prob in input file
        self.candidates = []  # To be filled during tableau creation
        self.faithCands = []  # 1 if the candidate is 'faithful', 0 otherwise
        self.probDenom = 1  # denominator for calculating MaxEnt prob of each candidate
        # this is the sum of each exponentiated harmony score
        self.predProbsList = []  # list of each candidate's predicted probability; used in sampling
        # gets filled (and updated) during learning
        self.obsProbsList = []  # list of each candidate's observed probability; used in sampling
        self.HList = []  # list of each candidate's harmony; for straight or Noisy HG
        self.winner = None
        self.constraintList = constraintNames  # this will generally wind up being a bunch of strings, followed by a bunch of tuples, for the PFCs
        self.hiddenStructure = hiddenStructure
        self.surfaceCands = []  # a place to hold the unique surface candidates
        # Note: if hidden structure is active, then obsProbsList corresponds to surfaceCands.
        # Otherwise, it corresponds simply to candidates
        self.lexemes = lexemes  # required for applyPFCs() and applyLexCs()
        self.w = w
        self.pfcIndex = len(self.w)
        self.negCrossEntropy = 0  # Just for this tableau.  Can multiply by self.prob to get neg log likelihood
        #print(self)

    def __repr__(self):
        return "Tableau object '" + self.tag + "' with " + str(len(self.candidates)) + " candidates.  Winner: " + str(
            self.winner) + "\n" + "Attributes: tag, prob, candidates, probDenom, predProbsList, HList, obsProbsList, surfaceCands, hiddenStructure, constraintNames, winner"

    def __str__(self):
        vform = '{:4s} '  # format function for tableau - increase number for more space between cells
        if len(self.candidates)>0:
            longCand = max([len(i.c) for i in self.candidates])
            nViol = len(self.candidates[0].violations)
        else:
            longCand = 5
            nViol = len(self.constraintList)
        cform = '{:>' + str(longCand) + 's} '
        form = '{:3s} ' + cform + '{:5s} ' * 3 + vform * nViol
        out = "Tableau " + self.tag + "\n"
        # add functionality for multi-input tableaux
        #print("lexemes:")
        #print("".join([l.tag for l in self.lexemes]))
        out += "Using lexemes "+ " ".join([l.tag for l in self.lexemes])+"\n"
        # expect constraintList to be a list of some strings and some tuples
        if self.constraintList:
            names = [i[0] if type(i) == tuple else i for i in self.constraintList]
            vform = ''.join([('{:^' + str(len(i)) + 's} ') for i in names])
            form = '{:3s} ' + cform + '{:5s} ' * 3 + vform
            out += form.format(*[" "] * 5 + [str(j) for j in names])
        if len(self.candidates)==0:
            out += '\n (no candidates)'
            return out

        for i in range(0, len(self.candidates)):
            thisC = self.candidates[i - 1].c
            w = " "
            if thisC == self.winner:
                w = " --> "
            v = self.candidates[i - 1].violations
            if type(self.predProbsList[i - 1]) == float:
                predProb = round(self.predProbsList[i - 1],2)
            else:
                predProb = self.predProbsList[i - 1]
            if type(self.HList[i - 1]) == float:
                H = round(self.HList[i - 1],2)
            else:
                H = self.HList[i - 1]

            row = [w] + [thisC, self.candidates[i - 1].observedProb, predProb, H] + v
            if len(row)< len(names)+5:
                row += ['-']*((len(names)+5)-len(row))

            out += '\n' + form.format(*[str(j) for j in row])
        return out

    def normalizeProbs(self):
        self.obsProbsList = [o/sum(self.obsProbsList) for o in self.obsProbsList]
        # update all the candidates too

        for c,op in zip(self.candidates,self.obsProbsList):
            c.observedProb = op
        if type(self.predProbsList[0]) in [int,float]:
            self.predProbsList = [p/sum(self.predProbsList) for p in self.predProbsList]

    def toFile(self):#, w):
        # calculate harmonies, and predicted values
        # add in constraint weights, including PFC weights
        # add in lexeme labels somewhere
        # create an 'input' column
        #self.predictProbsMaxEnt(w)
        urs = [""]*len(self.candidates)
        if type(self.lexemes)==list:
            try:
                out = "Using lexemes "+"\t"+ "\t".join([l.tag for l in self.lexemes])+"\n"
            except:
                out = ""
                #print("\t".join([l.tag for l in self.lexemes]))
        elif type(self.lexemes)==tuple:
            out = ""
            # put lexemes together in a list in same order as candidates
            allIndices = []
            allLexemes = []
            for i,j in zip(self.lexemes[1],self.lexemes[0]):
                allIndices+=i
                allLexemes+=[j]*len(i)
            # should be e.g.
            # [1,2,3,7,8,9,4,5,6]
            # [a,a,a,c,c,c,b,b,b]
            #print(allIndices)
            #print(allLexemes)
            lexemeOrderList = []
            for i in range(0,len(allIndices)):
                lex =allLexemes[allIndices.index(i)]
                lexemeOrderList += ["_".join([l.tag for l in lex])]
            #print(lexemeOrderList)
            urs = lexemeOrderList
        else:
            print("\n WARNING: One of your tableaux has a lexemes object that is not recognizable")
            out = ""

        out += '\t'.join(["input","lexeme(s)_used","candidate", "obs.prob", "pred.prob", "H"] + [i[0] if type(i) == tuple else i for i in self.constraintList])
        out += '\n' +'\t'+ '\t'.join(["", "", "", "", ""] + [str(j) for j in self.w])
        for c in self.candidates:
            out += '\n' + '\t'.join(
                [str(j) for j in [self.tag,urs.pop(0), c.c, c.observedProb, c.predictedProb, c.harmony] + c.violations])

        return out

    def copy(self):
        newT = Tableau(self.tag, self.prob, self.hiddenStructure, self.lexemes[:], self.w[:])
        newT.winner = self.winner
        newT.constraintList = self.constraintList
        for c in self.candidates:
            newT.addCandidate(c.copy())

        return newT

    def addCandidate(self, cand):
        self.candidates.append(cand)
        # Is this a faithful candidate?
        #
        if cand.surfaceForm != cand.c:
            self.hiddenStructure = True
        if cand.surfaceForm not in self.surfaceCands:
            self.surfaceCands.append(cand.surfaceForm)
            self.obsProbsList.append(cand.observedProb)
        # Add placeholders for the others so the tableau is always printable
        self.predProbsList.append("EMPTY")
        self.HList.append("EMPTY")

    def checkViolationLength(self):
        '''check if all the violation vectors are the same length'''
        c1 = self.candidates[0]
        l = len(c1.violations)
        for i in self.candidates:
            if len(i.violations) != l:
                print("Not all violation vectors are the same length!\n", "Candidate ", i.c, "has ", len(i.violations),
                      ", while candidate", c1.c, "has ", l, " violations.")
                return 0
            else:
                return 1

    def checkViolationsSign(self, convert=True, userChoice=False):
        '''check if all violations in the tableau are positive.  In this program, we are assuming positive violations, (mostly) positive weights, and the negative sign is added with the harmony calculation'''
        allNegative = True  # if all violations are negative, convert all to positive
        allPositive = True  # these can't both be true of course ... unless all violations are zero
        for i in self.candidates:
            if min(i.violations) < 0:
                allPositive = False
            if max(i.violations) > 0:
                allNegative = False

        if allPositive:
            if allNegative:
                print("WARNING: your constraint violations are all zero! Proceeding anyway...")
            return 1
        elif allNegative:
            print(
                "WARNING: your constraint violations are all negative numbers.  For the learner to function normally, they probably need to be converted to positive")
            if userChoice:
                proceed = input("Proceed? (y/n)")
                if proceed.lower() == 'n':
                    convert = False
            if convert:
                for i in self.candidates:
                    i.violations = [-v for v in i.violations]
                if self.checkViolationsSign():
                    print("Negative violations successfully converted")
                    return 1
        else:
            print(
                "WARNING: Your constraint violations are a mix of positive and negative numbers.  Proceed with caution!")
            return 0

    def rect(self, userChoice=False):
        l = self.checkViolationLength()
        s = self.checkViolationsSign(userChoice)
        # what else?
        return bool(l and s)

    def lexemesToFaithCands(self,rich=False,features=None):
        individualCands = []
        for l in self.lexemes:
            if rich:
                c = l.toRichCand(features)
            else:
                c = l.toFaithString()
            individualCands.append(c)

        if len(self.lexemes) > 1:
            faiths = list(itertools.product(*[i for i in individualCands]))
        else:
            faiths = individualCands
        # faiths is a list of tuples, each tuple is faithful candidates from each morpheme
        fcs =[]
        for fc in faiths:
            if rich:
                # begin creating the new richCand
                firstFaithCand = fc[0]
                newSegsList = firstFaithCand.segsList[:]
                newSegsDict = firstFaithCand.segsDict.copy()
                newActivitys = firstFaithCand.activitys[:]
                newSuprasegmentals = firstFaithCand.suprasegmentals[:]
                # add in material from each subsequent morpheme's faith cand
                for i in range(1, len(fc)): # start with 1 because we've already got info from fc[0]
                    segs = fc[i].segsList[:]
                    segsDict = fc[i].segsDict.copy()
                    activs = fc[i].activitys[:]
                    supr = fc[i].suprasegmentals[:]

                    # add in the current morpheme to the richCand
                    suff = '_w' + str(i+1) # _w2 for the second morpheme, _w3 for third, etc.
                    # create segment labels
                    newSegsList += [seg + suff for seg in segs]
                    for seg in segs:
                        newSegsDict[seg + suff] = segsDict[seg][:]
                    newActivitys += activs
                    newSuprasegmentals += supr

                # now make the new richCand
                newC = features.featureToS(newSegsDict, newSegsList)
                obsProb = 1 if newC == obsOutput else 0

                # violations are empty, for now, and order is None, because newSegsList already encodes the correct order
                rcand = richCand(newC, [], obsProb, newSegsDict, newSegsList, None, newActivitys, newSuprasegmentals, surfaceForm=newC)
                fcs.append(rcand)

            else:
                fcs.append("_".join([i for i in fc]))

        return fcs


    def applyOneLexC(self,constraint,lexeme,lexCname=None, fcs=None,localityRestrictionType="overlap"):
        #print(lexeme)
        #print(type(lexeme))
        #print(lexeme.tag)
        if lexCname is None:
            lexCname = constraint.name + '_' + lexeme.tag

        self.constraintList.append(lexCname)

        if fcs is None:
            fcs = self.lexemesToFaithCands()
            # TODO should take rich, features as arguments too

        #print(fcs)

        if localityRestrictionType=="presence_only":
            self.applyOneConstraint(constraint,fcs)
            return

        for cand in self.candidates:
            #print(cand.c)
            # get the violation, save to v, indices
            if constraint.MF == 'F':
                vsums = [] # floats
                viols = [] # lists of violations
                indicesSets = [] # list of tuples, start,end indices of each violation
                for fc in fcs: # faithful candidates
                    #print(fc)
                    vsum, viol, indices = constraint.assignViolations(fc,cand.c)
                    vsums.append(vsum)
                    viols.append(viol)
                    indicesSets.append(indices)
                minv = min(vsums) # assume the closest matched faithful office
                vs = viols[vsums.index(minv)]
                indices = indicesSets[vsums.index(minv)]

            else:
                vsum, viol, indices = constraint.assignViolations(cand.c)
                vs = viol
            # Now, we have vs, a list of violations
            # and indices, a list of index tuples
            #print(indices)

            lexIndex = self.lexemes.index(lexeme)
            morphemeEdges = [[0]]
            for m in re.finditer('_',cand.c):
                boundary = m.start(0) #index of the '_'
                morphemeEdges[-1].append(boundary-1)
                morphemeEdges.append([boundary+1])
            morphemeEdges[-1].append(len(cand.c))
            relevantIndices = morphemeEdges[lexIndex]
            #print(relevantIndices)


            # check for overlap with the relevant morpheme
            totalV = 0 # each v in vs that is sufficiently local is added to the total
            for v,i in zip(vs,indices):
                #print(v)
                #print(i)
                overlap = [False,False]
                for j in (0,1):
                    if i[j] >= relevantIndices[0] and i[j]<= relevantIndices[1]:
                        # L/R edge of the violation overlaps with the morpheme
                        overlap[j] = True

                #print(overlap)

                if localityRestrictionType=="overlap":
                    if overlap[0] or overlap[1]: # for overlap, violation is assigned iff only one edge overlaps with the morpheme
                        totalV+=v
                elif localityRestrictionType=="strict":
                    if overlap[0] and overlap[1]: # for 'strict' the violation must ONLY come from the indexed morpheme
                        totalV+=v
            #print(totalV)

            cand.violations.append(totalV)

    def applyOneConstraint(self,constraint,fcs=None):
        #print("applying...")
        #print(fcs)
        if fcs is None:
            fcs = self.lexemesToFaithCands()
            # TODO should take rich, features as arguments too
        for cand in self.candidates:
            if constraint.MF == 'F':
                viols = []
                for fc in fcs: # faithful candidates
                    #print(fc)
                    #print(cand.c)
                    viol = constraint.assignViolations(fc,cand.c)
                    #print(viol)
                    if type(viol) == float:
                        viols.append(viol)
                    else:
                        viols.append(viol[0]) # assume the first result is always the number
                cand.violations.append(min(viols)) # assume the closest matched faithful candidate
            else:
                viol = constraint.assignViolations(cand.c)
                if type(viol) == float:
                    cand.violations.append(viol)
                else:
                    cand.violations.append(viol[0]) # assume the first result is always the number

    def applyPFCs(self):
        self.pfcIndex = len(self.w)
        # fill out constraintList with placeholders if it's not long enough
        if len(self.constraintList) < len(self.w):
            self.constraintList += ["C"] * (len(self.w) - len(self.constraintList))
        if len(self.constraintList) > len(self.w):
            print("WARNING: you have more constraint names than constraint weights in tableau " + self.tag)

        for lexeme in self.lexemes:
            for pfc in lexeme.PFCs:
                # print(pfc.name)
                for cand in self.candidates:
                    parsed = cand.c.split("_")
                    try:
                        cand.violations.append(pfc.evaluate(parsed[self.lexemes.index(lexeme)]))
                    except:
                        print("Failed to apply PFC: " + pfc.name)
                self.constraintList.append((pfc.name, pfc))
                self.w.append(pfc.w)

    def applyLexCs(self,lexCs,gram, fcs=None,localityRestrictionType="overlap"):
        self.lexCindex = len(self.w) # assume we haven't applied LexCs or PFCs yet
        # need the filling out that's happening in applyPFCs?

        for lexeme in self.lexemes:
            cIndex = 0  # we're iterating through constraints 
            cFunctionsStartAfter = gram.cfunctionStartIndex
            for index, weightList, cname in zip(lexeme.lexCindexes,lexCs,gram.trainingData.constraintNames):
                # look for indexation on a constraint
                if index >0: # if this lexeme has an indexed version
                    lexCw = weightList[index] # get its weight
                    lexCname = cname + '_' + str(index) + '_' + lexeme.tag # e.g. Syncope_2_ta

                    if cIndex >= cFunctionsStartAfter: # if it's a function
                        #print(gram.constraints)
                        constraint = gram.constraints[cIndex-cFunctionsStartAfter]
                        #print("isFunction")
                        # now apply it to candidates
                        # according to Paterian locality rules, must overlap with the relevant morpheme
                        # This will be handled inside applyOnelexC
                        self.applyOneLexC(constraint,lexeme,lexCname,localityRestrictionType=localityRestrictionType)
                        #print(self)
                    else:
                        constraint = cIndex # not a function,
                        # just an index we can use to copy the violation over
                        for cand in self.candidates:
                            lexCviol = cand.violations[constraint]
                            cand.violations.append(lexCviol)
                        self.constraintList.append(lexCname)

                    self.w.append(lexCw)

                cIndex += 1 

            # is the constraint a function?
                # if yes, apply it according to candidates' lexeme membership
                # if no, apply its violation to the whole candidate


    def calculateHarmony(self, w):
        '''Takes a vector of weights, equal in length to the violation vectors of the candidates.  Populates the harmony parameter of each candidate based on the weight vector w'''
        # note that w could be made up of a variety of constraint types, markedness and PFC's for example.
        self.HList = []
        for cand in self.candidates:
            # Calculate that good 'ole dot product!
            cand.harmony = -sum(viol * weight for viol, weight in zip(cand.violations, w))
            # let's keep harmony at 500
            if cand.harmony>500:
                cand.harmony = 500
            if cand.harmony<-500:
                cand.harmony = -500
            # harmony will be a negative number if all constraint weights are positive.
            # May become positive when constraint weights go negative
            self.HList.append(cand.harmony)

    def predictProbsMaxEnt(self, w):
        '''Convert harmony scores, and the MaxEnt denominator, to predicted probabilities for each candidate output in the Tableau '''
        self.calculateHarmony(w)  # start by getting those harmonies
        self.probDenom = sum([pow(math.e, cand.harmony) for cand in self.candidates])
        self.predProbsList = []
        for cand in self.candidates:
            try:
                cand.predictedProb = pow(math.e, cand.harmony) / self.probDenom
            except OverflowError:
                print(
                    "Something's wrong with the exponentiation! Python's patience with giant exponents only stretches so far...")

            except ZeroDivisionError:
                print("Somehow your MaxEnt denominator is zero!  Can't calculate probabilities this way")
                #print(self)
                print([cand.harmony for cand in self.candidates])
            self.predProbsList.append(cand.predictedProb)



    def getPredWinner(self, w=None, theory='MaxEnt'):
        ''' generates a predicted winner based on weights and theory'''
        # TODO add stochastic OT functionality here
        if theory == 'HG' or theory == 'NoisyHG':
            # if Noisy HG, here's where to add the noise probably
            if w:
                self.calculateHarmony(w)
            bestH = max(self.HList)
            bestCands = [cand for cand in self.candidates if cand.harmony == bestH]
            winCandidate = np.random.choice(bestCands, 1)[
                0]  # if there's more than one optimal candidate according to the harmony, select one at random.
        elif theory == 'MaxEnt':
            if w:
                self.predictProbsMaxEnt(w)
            winCandidate = self.candidates[np.random.choice(range(0, len(self.candidates)), 1, p=self.predProbsList)[0]]
        else:
            print("Unrecognized theory type " + theory + ".  Acceptable types are 'HG', 'NoisyHG', and 'MaxEnt'.")
            return None

        return winCandidate

    def getObsCandidate(self, w=None, theory='MaxEnt'):
        ''' find the observed candidate to use for learning update '''
        ''' If multiple candidates match a single output, use EIP from jaroscz 2013 to choose a parse/hidden structure/predicted candidate '''
        obsOutput = self.getObsOutput()
        matchCands = []  # holding all candidates whose surface form matches the observed output
        for cand in self.candidates:
            if obsOutput == cand.surfaceForm:
                matchCands.append(cand)
        if len(matchCands) > 1:  # if more than one candidate matched the observed output, there is hidden structure to parse
            # try to parse hidden structure in a way that is theory agnostic, or at least passes theory on to the internal function calls....
            # generate a sub-tableau with just matchCands, but weights = w
            subTab = Tableau(obsOutput, hiddenStructure=False)
            for cand in matchCands:
                subTab.addCandidate(cand)
            winCandidate = subTab.getPredWinner(w, theory)
        else:
            winCandidate = matchCands[0]

        return winCandidate

    def getObsOutput(self):
        ''' simple function to get the observed output from the obsProbsList'''
        obsOutput = self.surfaceCands[np.random.choice(range(0, len(self.surfaceCands)), 1, p=self.obsProbsList)[0]]
        return obsOutput

    def compareObsPred(self, w, theory='MaxEnt',threshold=1):
        self.normalizeProbs() # make sure all probs in the tableau sum to 1
        predCandidate = self.getPredWinner(w=w, theory=theory)
        if predCandidate.observedProb> threshold:
            return 0, predCandidate, predCandidate

        obsCandidate = self.getObsCandidate(w=w, theory=theory)

        error = (0 if obsCandidate.surfaceForm == predCandidate.surfaceForm else 1)

        return error, obsCandidate, predCandidate

#sampleGrammar =

class Grammar:
    def __init__(self, config = "config.gl",inputFile=None):
        self.t = 0
        self.config = config
        self.inputFile = inputFile
        self.readFromConfig(config,inputFile)

    def readFromConfig(self,config="config.gl",inputFile=None):
        with open(config) as f:
            row = 0
            for line in f.readlines():
                row += 1
                line=line.strip()
                if line.strip() and line[0]!="#":  #  Use hash as comment character in config file
                    param = [i.strip() for i in line.split(":")]

                    if len(param) != 2:
                        print(Fore.RED + "\nERROR: Row " + str(row) + " of " + config + " has the wrong number of entries.  It should have the form parameterName: parameterValue"+ Style.RESET_ALL)
                        exit()

                    if param[0]=="trainingData":
                        if inputFile is None:
                            self.trainingDatafile = param[1]
                        else:
                            self.trainingDatafile = inputFile
                        try:
                            self.trainingData = trainingData(self.trainingDatafile)
                            self.cfunctionStartIndex = len(self.trainingData.constraintNames)

                        except:
                            print(Fore.RED + "\nERROR: No training data file read in.  Please check the format and path to your file: " + self.trainingDatafile + Style.RESET_ALL)
                            exit()
                            
                    elif param[0] == "weights":
                        self.startWeightParam = param[1]
                        weights = param[1]
                        print(weights)
                        weights = weights.split(",")
                        print(weights)
                        if weights[0] !='random':
                            try:
                                weights = [float(w) for w in weights]
                                if weights == [0]:
                                    self.w = []
                                else:
                                    self.w = weights

                            except ValueError:
                                print("\nWARNING: not all weight values in " + config +" could be converted to float")
                                print("Using default weights of 0 instead"+ Style.RESET_ALL)
                                self.w = []
                        else:
                            self.w = weights

                    elif param[0]=="featureSet":
                        self.featuresFileName=(param[1])
                        try:
                            self.featureSet = Features(param[1])
                        except:
                            print(Fore.RED +"\nERROR: Your feature set file, " + param[1] + " did not work."+ Style.RESET_ALL)

                    elif param[0]=="addViolations":
                        try:
                            self.addViolations = eval(param[1])
                        except:
                            print("\nWARNING: addViolations must be set to 'True' or 'False'. Using default value of 'False'")
                            self.addViolations = False

                    elif param[0]=="constraints":
                        self.constraintsModule = param[1]
                        if self.constraintsModule != "None" and self.addViolations:
                            try:
                                constraints = importlib.import_module(self.constraintsModule)
                                self.constraints = constraints.constraints
                                self.cfunctionStartIndex = len(self.trainingData.constraintNames)
                                self.trainingData.constraintNames+= [c.name for c in self.constraints]
                            except Exception as e:
                                print("\nWARNING: no constraints module found called " + self.constraints)
                                self.constraints = "None"

                        # initialize weights now that we have all the constraints,
                        # but before initializing LexCs
                        if len(self.w)==0:
                            self.initializeWeights()
                        elif self.w[0]=='random':
                            self.initializeWeights(self.w)

                    elif param[0]=="generateCandidates":
                        try:
                            self.generateCandidates = eval(param[1])
                        except:
                            print("\nWARNING: generateCandidates must be set to 'True' or 'False'.  Using default value of 'False'")
                            self.generateCandidates = False

                        if self.generateCandidates:
                            if self.constraints != "None":
                                self.operations = constraints.operations
                            else:
                                print("\nWARNING: you have specified generateCandidates as 'True' but no operations could be read off the constraints module.\n Ensure that your constraints module " + self.constraints +" exists, and contains an object called 'operations'.\n No operations are in effect.")

                    elif param[0]=="learningRate":
                        learningRate = param[1]
                        learningRate = learningRate.split(",")
                        try:
                            if len(learningRate)==2:
                                self.learningRate = learningRate
                            elif len(learningRate)==1:
                                self.learningRate = [learningRate[0],learningRate[0]]
                            else:
                                print("\nWARNING: learningRate could not be converted to float.  Using 0.01")
                                self.learningRate = [0.01,0.01]
                        except:
                            print("\nWARNING: learningRate could not be converted to float.  Using 0.01")
                            self.learningRate = [0.01,0.01]

                    elif param[0]=="decayRate":
                        try:
                            self.decayRate = float(param[1])
                        except:
                            print("\nWARNING: decayRate could not be converted to float.  Using 0.0001")
                            self.decayRate = 0.0001

                    elif param[0]=="decayType":
                        try:
                            self.decayType = param[1]
                        except:
                            print("\nWARNING: decayType not recognized.  Using static decay")
                            self.decayType = "static"

                        if self.decayType not in ["static","L1","L2"]:
                            print("\nWARNING: decayType not recognized.  Using static decay")
                            self.decayType = "static"

                    elif param[0]=="threshold":
                        try:
                            self.comparisonThreshold = float(param[1])
                        except:
                            print("\nWARNING: threshold could not be converted to float.  Using default value of 1.  This means that observed forms will always be sampled \n(This has no effect if your dataset does not contain within-item variation)")
                            self.comparisonThreshold = 1
                        if self.comparisonThreshold > 1:
                            print("\nWARNING: You specified a threshold value of more than 1.  This will be treated as 1")

                    elif param[0]=="noisy":
                        if param[1]=="yes":
                            self.noisy = True
                        elif param[1]=="no":
                            self.noisy = False
                        else:
                            print("\nWARNING: " + config + " value for 'noisy' is neither 'yes' nor 'no'.  Using default value of 'no'")
                            self.noisy = False

                    elif param[0]=="useListedType":
                        self.useListedType = param[1]

                        if param[1]=="hidden_structure":
                            self.p_useListed = 3
                        elif param[1]=="sample_using_frequency":
                            self.p_useListed = 2
                        elif param[1]=="sample_flat_rate":
                            self.p_useListed = 1
                        elif param[1]=="none":
                            self.p_useListed = 0
                        else:
                            print("\nWARNING: " + config + " value for 'useListedType' is unrecognized.  Using default value, no lexical listing.")
                            self.p_useListed = 0

                        if self.p_useListed > 0:
                            self.cPairs = self.prepForUselisted()

                        if self.p_useListed == 0:
                            # remove _listed versions of each constraint
                            indexPairs = []
                            toRemove = []
                            for name in self.trainingData.constraintNames:
                                if re.search("_listed", name):
                                    cname = re.sub('_listed', '', name)
                                    indexPlain = self.trainingData.constraintNames.index(cname)
                                    indexListed = self.trainingData.constraintNames.index(name)
                                    indexPairs.append((indexPlain, indexListed))
                                    toRemove.append(indexListed)

                            toRemove = sorted(toRemove, reverse=True)
                            # check whether to also remove constraint weights
                            if len(self.w) == len(self.trainingData.constraintNames):
                                cDrop = True
                            for i in toRemove:
                                self.trainingData.constraintNames.pop(i)
                                if cDrop:
                                    self.w.pop(i)
                                for tableau in self.trainingData.tableaux:
                                    for candidate in tableau.candidates:
                                        candidate.violations.pop(i)

                    elif param[0]=="useListedRate":
                        if self.p_useListed <= 1 and self.p_useListed>0:
                            try:
                                self.p_useListed = float(param[1])
                            except:
                                print("\nWARNING: useListedRate cannot be converted to float.  Using default value of 1, always use listed form if available.")
                                self.p_useListed = 1

                    elif param[0]=="flip":
                        if self.p_useListed>0:
                            try:
                                self.flip = eval(param[1])
                            except:
                                print("\nWARNING: flip must be True or False.  Using default of False.")
                                self.flip = False
                        else:
                            self.flip = False

                    elif param[0]=="simpleListing":
                        if self.p_useListed>0:
                            try:
                                self.simpleListing = eval(param[1])
                            except:
                                print("\nWARNING: simpleListing must be True or False.  Using default value of True.")
                                self.simpleListing = True

                            if self.simpleListing and self.flip:
                                print("\nWARNING: simpleListing and flip are mutually exclusive.  Setting flip to False.")
                        else:
                            self.simpleListing = False
                    elif param[0]=="pToList":
                        try:
                            self.pToList = float(param[1])
                        except:
                            print("\nWARNING: pToList could not be converted to float.  Using default value of 0.75")
                            self.pToList = 0.75

                    elif param[0]=="nLexCs":
                        try:
                            self.lexC_type = float(param[1])
                        except:
                            print("\nWARNING: nLexCs could not be converted to float. Not using Lexically indexed constraints.")
                            self.lexC_type = 0
                        
                        if self.lexC_type:
                            self.prepForLexC()

                    elif param[0]=="pChangeIndexation":
                        try:
                            self.pChangeIndexation = float(param[1])
                        except:
                            print("\nWARNING: pChangeIndexation could not be converted to float.  Using default value of 0.5")
                            self.pChangeIndexation = 0.5

                    elif param[0]=="lexCStartW":
                        try:
                            self.lexCStartW = float(param[1])
                        except:
                            print("\nWARNING: lexCStartW could not be converted to float.  Using default value of 5.0")
                        self.lexCjumpParameter = self.pChangeIndexation**(1/self.lexCStartW)

                    elif param[0]=="locality":
                        try:
                            self.localityRestrictionType = param[1]
                        except:
                            print("\nWARNING: localityRestrictionType not assigned.  Using default value of 'overlap'")
                            self.localityRestrictionType = "overlap"

                    elif param[0]=="first_index_strategy":
                        try:
                            self.firstIndexStrat = param[1]
                        except:
                            print("\n WARNING: first_index_strategy not recognized.  Using default of 'lowest'")
                            self.firstIndexStrat = "lowest"

                    elif param[0]=="PFC_type":
                        self.PFC_type = param[1]
                        if self.PFC_type not in ["none","pseudo","full"]:
                            print("\nWARNING PFC_type must be one of 'none', 'pseudo' or 'full'.  Using default value 'none', no PFCs.")

                    elif param[0]=="PFC_lrate":
                        try:
                            self.PFC_lrate = float(param[1])
                        except:
                            print("\nWARNING: PFC_lrate could not be converted to float.  Using default value of 0.1")
                            self.PFC_lrate = 0.1

                    elif param[0]=="PFC_startW":
                        try:
                            self.PFC_startW = float(param[1])
                        except:
                            print("\nWARNING: PFC_startW could not be converted to float.  Using default value of 10.0")
                            self.PFC_startW = 10.0

                    elif param[0]=="activityUpdateRate":
                        try:
                            self.activityUpdateRate = float(param[1])
                        except:
                            print("\nWARNING: activityUpdateRate could not be converted to float.  Using default value of 0.05")
                            self.activityUpdateRate = 0.05

                    elif param[0]=="outfolder":
                        try:
                            self.outfolder = param[1]
                        except:
                            #### TODO: make better warning message
                            print("\nWARNING: outfolder doesn't work")

                    elif param[0]=="logFile":
                        try:
                            self.logFile = param[1]
                        except:
                            #### TODO: make better warning message
                            print("\n WARNING: logfile doesn't work")

                    elif param[0]=="label":
                        try:
                            self.label = param[1]
                        except:
                            #### TODO: make better warning message
                            print("\n WARNING: label doesn't work")


                    else:
                        print("\n WARNING: I don't recognize the parameter " + param[0])

        # check if all the parameters are there that should be
        print("Training from file: "+self.trainingDatafile)
        print("Feature set: "+self.featuresFileName)



        try:
            if self.addViolations:
                try:
                    print("Violations will be added from "+ self.constraintsModule)
                except:
                    print(Fore.RED +"\n ERROR: no constraints module found!  Specify the name under parameter 'constraints'."+Style.RESET_ALL)
            else:
                print("Constraint violations come only from input file")
        except:
            print("\n WARNING: You have not specified whether constraint violations should be added to your tableaux via function (using 'addViolations').  Violations will be taken directly from your input file only.")

        try:
            if self.generateCandidates:
                try:
                    print("Candidates will be generated, using module "+ self.constraintsModule)
                except:
                    print(Fore.RED +"\n ERROR: no constraints module found!  Specify the name under parameter 'constraints'."+Style.RESET_ALL)
            else:
                print("Candidates will not be generated")
        except:
            print("\n WARNING: You have not specified whether candidates should be generated (using 'generateCandidates').  Candidates will be taken directly from your input file only.")
        

        try:
            print("Learning Rate: "+ str(self.learningRate))
        except:
            print("\n WARNING: no learning rate specified (using 'learningRate').  Default value of 0.01 will be used.")
        
        print("Threshold for considering a prediction an error: "+str(self.comparisonThreshold))
        print("")
        # self.w
        # TODO finish this up

        # Print out constraint names and weights at end of read-in
        print(Fore.BLUE + Back.WHITE +"\nYour constraints and starting weights:")
        printform= ''.join([('{:^'+str(len(cname))+'s} ') for cname in self.trainingData.constraintNames])
        print( '\n'+printform.format(*[str(i) for i in self.trainingData.constraintNames]))
        print(printform.format(*[str(i) for i in self.w])+Style.RESET_ALL)

    def prepForUselisted(self):
        UseListedIndex = None

        # create a list of tuples pairing up plain and listed versions of each relevant constraint
        indexPairs = []
        toRemove = []
        for name in self.trainingData.constraintNames:
            if re.search("_listed", name):
                cname = re.sub('_listed', '', name)
                indexPlain = self.trainingData.constraintNames.index(cname)
                indexListed = self.trainingData.constraintNames.index(name)
                indexPairs.append((indexPlain, indexListed))
                toRemove.append(indexListed)

        toRemove = sorted(toRemove, reverse=True)
        if len(self.w) == len(self.trainingData.constraintNames):
            cDrop = True
        for i in toRemove:
            self.trainingData.constraintNames.pop(i)
            if cDrop:
                self.w.pop(i)

        if self.p_useListed > 2:
            self.trainingData.constraintNames.append("UseListed")
            self.w.append(0)
            
            UseListedIndex = self.trainingData.constraintNames.index("UseListed")
            print("\n ...adding UseListed at index " + str(UseListedIndex))


        return indexPairs, toRemove, UseListedIndex

    def prepForLexC(self):
        print("\nReady to learn with lexical indexation.  Maximum " + str(self.lexC_type) + " copies of each constraint.")
        self.lexCs = [[0] for i in self.w]
        # create a vector for every constraint
        # go through the lexicon, add in index vectors
        for lex in self.trainingData.lexicon.values():
            lex.lexCindexes = [0 for i in self.w]

        if self.lexC_type == "inf":
            self.lexC_type = len(self.trainingData.lexicon) ** 2
        # make the max length the length of the lexicon squared.  Hopefully this is long enough to accommate whatever weird stuff you're up to!

    def createLearningPlaylist(self, n):
        # n is total number of learning simulations
        return [self.trainingData.learnData[i] for i in
                list(np.random.choice(range(0, len(self.trainingData.learnData)), n, p=self.trainingData.sampler))]

    def initializeWeights(self, w=None):
        '''Function to initialize the weights - can take an argument, which is hopefully the same length as the number of constraints in the Tableaux object.  If it doesn't get that argument, it will initialize them to zero. '''
        # TODO (low priority atm) Add functionality to initialize weights to random values
        # figure out how many constraints we have all together
        nC = len(self.trainingData.constraintNames) #+ (len(self.constraints) if self.constraints else 0)
        #print(nC)
        if w is None:
            self.w = [0] * nC
        elif w[0] =='random':
            upper = float(w[2])
            lower = float(w[1])
            self.w = [random.random()*(upper-lower)+lower]
            for i in range(1,nC):
                self.w.append(random.random()*(upper-lower)+lower)
        else:
            if len(w) == nC:
                self.w = w
            else:
                print("ERROR: you tried to initialize weights with a list of length ", len(w),
                      ", but you have a total of ", nC, " constraints.  addViolations is set to ", self.addViolations)
            # This will print a warning, but it won't actually stop you from initializing constraints badly?  Maybe this is a problem that should be fixed.

    def calculate_sample_weights(self, frequencies):

        # helper function; calculates weights for the weighted sample
        # takes a list of word frequencies as input
        # returns a set of weights

        total = sum(frequencies)
        weights = [round(freq / total, 10) for freq in frequencies]
        return weights

    def update(self, datum, learningRate):  # datum is an entry from playlist
        # Start with a learning datum
        lexemes = datum[0]

        # TODO this code is recapitulated inside Grammar.makeTableau()
        # streamline?
        if self.p_useListed == 0:  # If we're not doing useListed at all
            # Decay the existing PFCs affiliated with each lexeme, and remove zero weighted ones
            for lex in lexemes:
                lex.decayPFC(self.t, self.decayRate, decayType=self.decayType)
                #print("decaying")
                if len(lex.PFCs) > len(self.featureSet.featureNames) * len(lex.segLabels) * 4:
                    print("WARNING: too many PFCs")
                    break

            # Note that we've encountered these two lexemes
            for lex in lexemes:
                lex.lastSeen = self.t
                lex.freq += 1

        #decay LexCs
        if self.lexC_type:
            for c in range(0, len(self.lexCs)):

                # decay all lexCs
                if self.decayType == "static":
                    self.lexCs[c] = [i - self.decayRate for i in self.lexCs[c]] 

                elif self.decayType == 'L1':
                    self.lexCs[c] = [i - self.decayRate*i for i in self.lexCs[c]]

                elif self.decayType == 'L2':
                    self.lexCs[c] = [i - (self.decayRate/2)*(i**2) for i in self.lexCs[c]]
                
                self.lexCs[c] = [i if i > 0 else 0 for i in self.lexCs[c]]  # lower bound at zero



        # grab, create, or fill out the tableau
        tab = self.makeTableau(datum)


        # Predict an output and compare to observed
        e, obs, pred = tab.compareObsPred(tab.w,threshold=self.comparisonThreshold)

        if self.noisy:
            print(tab)
            print("error" if e else "correct")
            print("observed: " + obs.c)
            print("predicted: " + pred.c)

        #print(tab)
        #print(obs.violations)
        #print(pred.violations)
        #print(tab.candidates[1].violations)
        # print(constraintList)
        if e:
            # print(e,tab.tag, obs.c,pred.c,obs.violations,pred.violations,obs.harmony,obs.predictedProb,pred.harmony,pred.predictedProb)
            # print(self.w)
            #################################################################
            # update general weight: perceptron update
            updateVector = [float(p) - float(o) for p, o in zip(pred.violations, obs.violations)]
            #print(updateVector)
            self.w = [float(wt) + up * learningRate for wt, up in zip(self.w, updateVector)]
            self.w = [i if i > 0 else 0 for i in self.w]  # limit to positve constraint weights
            #################################################################
            #print(self.w)

            #################################################################
            # useListed
            if self.p_useListed > 0:
                # TODO figure out what to do with within-item variation
                #print(tab.tag)
                if len(datum[0])>1 and random.random() < self.pToList: # list
                    tag = "_".join([i.tag for i in datum[0]])
                    segmentlist = [character for character in re.sub("_","",obs.surfaceForm)]
                    if (tag not in self.trainingData.lexicon) or self.flip:
                        self.trainingData.lexicon[tag] = lexeme(tag, segmentlist)

                        with open(self.listingFilenamen,"a") as f:
                            f.write("\n" + tag + "\t" + "".join(segmentlist) + "\t" + str(self.t))
                    elif not self.simpleListing: # ok, it's listed but the listed form isn't what we just observed
                        nTag = 2
                        # start with 2, add another copy of the lexeme with a tag that doesn't exist yet
                        while tag+"_"+str(nTag) in self.trainingData.lexicon:
                           nTag +=1
                        tag += "_"+str(nTag) # e.g. tag_5 for the fifth copy

                        # options for how we could have done this:
                        # turn the entry of [tag] into a list of lexemes?
                        # -->update the dictionary to have entry tag_i or something
                        #       how many copies do we look for? <- any string of digits
                        # create a second dictionary, with all the extra entries?
                        # turn the lexeme into a list of segmentlists?
                        # just leave it how it was, switching back and forth?


                    #print(obs.surfaceForm)
            #print(self.w)
            ##################################################################

            ##################################################################
            # Lexically-indexed constraints
            if self.lexC_type:
                self.lexCupdate(obs, pred, updateVector, datum[0],tab, learningRate)



            ##################################################################
            # PFC stuff
            # update existing PFCs
            if self.PFC_type != 'none':
                for pfc, p, o in zip(tab.constraintList[tab.pfcIndex:], pred.violations[tab.pfcIndex:],
                                     obs.violations[tab.pfcIndex:]):
                    #print(pfc)
                    #print(p)
                    #print(o)
                    pfc[1].w += (p - o) * self.PFC_lrate
                    pfc[1].w = 0 if pfc[1].w < 0 else pfc[1].w

                # induce new PFCs
                newPFCs = []
                if self.PFC_type == "pseudo":
                    # parse each candidate into morphemes
                    parsed = obs.c.split("_")
                    parsedPred = pred.c.split("_")
                    if len(parsed) != len(datum[0]) or len(parsedPred) != len(datum[0]):
                        print(parsed)
                        print(datum[0])
                        print(
                            "ERROR: pseudo-PFC cannot be induced because morphemes in the candidate cannote be aligned with morphemes in the input")
                        exit
                    for i in range(0, len(datum[0])):
                        if parsed[i] != parsedPred[i]:  # localize the error to the morpheme we are considering
                            newPFC = PFC(self.PFC_startW, surfaceString=parsed[i])
                            if newPFC not in datum[0][i].PFCs:
                                datum[0][i].PFCs.append(newPFC)
                                if self.noisy:
                                    print("Added ", datum[0][i].tag, newPFC.name)


                elif self.PFC_type == "full":
                    newPFCs = inducePFCs(obs, pred, self.featureSet)
                    # pfcs_to_words = [[]]*len(datum[0])
                    for pfc in newPFCs:  # loop through and determine which goes with which lexeme
                        if len(pfc) > 2:
                            wd = re.search('(_)(w)([1234567890])', pfc[2])
                            if wd:
                                newPFC = PFC(self.PFC_startW, pfc[1], re.sub('_w.*', '', pfc[2]))
                                if newPFC not in datum[0][int(wd.groups()[2]) - 1].PFCs:
                                    # print("yes")
                                    datum[0][int(wd.groups()[2]) - 1].PFCs.append(newPFC)
                            else:
                                newPFC = PFC(self.PFC_startW, pfc[1], pfc[2])
                                if newPFC not in datum[0][0].PFCs:
                                    # print("yes")
                                    datum[0][0].PFCs.append(newPFC)
                        else:
                            for lex in datum[0]:
                                newPFC = PFC(self.PFC_startW, pfc[1])
                                if newPFC not in lex.PFCs:
                                    lex.PFCs.append(newPFC)
                            # somewhat odd strat: affiliate exists_feature constraints with all lexemes

            # induce PFCs
            # compare against existing PFCs
            # update if they already exist, otherwise induce
            # Don't update every PFC???
        ##################################################################

        self.t += 1
        # print(self.w)
        return e

    def epoch(self, playlist, niter, learningRate, start=0):
        errors = 0
        for i in range(0, niter):
            errors += self.update(playlist[start + i],learningRate)

        error_rate = errors / niter

        # print out list of weights (to file)
        # print out SSE
        # print out likelihood
        #
        return error_rate

    def learn(self, nIterations, nEpochs, nRuns = 1):
        runSummaryFilename = self.outfolder+'/'+"runSummary_"+self.label+".txt"
        outFilename = self.outfolder+'/'+"tableaux_"+self.label+"_"
        weightsFilename = self.outfolder+'/'+"weights_"+self.label+"_"
        pfcsFilename = self.outfolder+'/'+"PFCs_"+self.label+"_"
        lexCsFilename = self.outfolder+'/'+"lexCs_"+self.label+"_"
        errRatesFilename = self.outfolder+'/'+"errRates_"+self.label+"_"
        lexCweightsFilename = self.outfolder+'/'+"lexCws_"+self.label+"_"
        indexesFilename = self.outfolder + '/' + "indexes_"+self.label+"_"
        self.listingFilename = self.outfolder+'/'+"listing_"+self.label+"_"


        with open(runSummaryFilename,"w") as f:
            f.write('\t'.join(self.trainingData.constraintNames+["SSE","logLikelihood","errorRate"]))

        for n in range(0,nRuns):

            self.readFromConfig(self.config,self.inputFile)

            if self.p_useListed >0:
                self.listingFilenamen = self.listingFilename+str(n)+'.txt'
                with open(self.listingFilename+str(n)+'.txt',"w") as f:
                    f.write("lexemes \t segments \t listed_at_timestep")

            grammar_constraints_w = []
            PFCs_w = []
            PFC_list = []  # stores every PFC that is ever induced

            self.playlist = self.createLearningPlaylist(nIterations * nEpochs)

            # setup for changing the learning rate throughout learning
            startLearningRate = float(self.learningRate[0])
            endLearningRate = float(self.learningRate[1])
            learningRateDecrement = (startLearningRate - endLearningRate)/nEpochs
            currentLearningRate = startLearningRate



            # tracking error rates each epoch
            last10PerErr = 0
            last10PerCount = 0
            rates = []

            # tracking lexCs weights per epoch
            lexCsOverTime = []

            indexesOverTime = []
            for c in self.w:
                thisDict = {}
                for lexkey in self.trainingData.lexicon.keys():
                    thisDict[lexkey] = [(0,0)]  # each entry will be weight, index
                indexesOverTime+=[thisDict]

            for i in range(0, nEpochs):

                rate = self.epoch(self.playlist, nIterations, currentLearningRate, start=nIterations * i)
                print(Fore.CYAN + "Epoch " + str(i+1) +": " + str(rate*100) + " % errors"+ Style.RESET_ALL)
                rates.append(rate)
                if i>= (nEpochs-(nEpochs/10)):
                    last10PerErr += rate
                    last10PerCount += 1
                elif nEpochs <= 10:
                    last10PerCount = 1
                    last10PerErr = rate

                if self.lexC_type:
                    lexCsOverTime.append(self.lexCs[:])

                    for ci in range(0,len(indexesOverTime)): # go through constraints
                        wlist = self.lexCs[ci] # list of weights
                        for lexkey in self.trainingData.lexicon.keys():
                            windex = self.trainingData.lexicon[lexkey].lexCindexes[ci] # the index
                            indexesOverTime[ci][lexkey].append((wlist[windex],windex))


                grammar_constraints_w.append(self.w)
                currentPFC_w = [0 for i in PFCs_w[-1]] if len(PFC_list) > 0 else []
                for lexeme in self.trainingData.lexicon.values():
                    #if type(lexeme) == 'lexeme':
                    for pfc in lexeme.PFCs:
                        name = lexeme.tag + "_" + pfc.name
                        if name not in PFC_list:
                            PFC_list.append(name)
                            currentPFC_w.append(0)  # make it the right length to accommodate the new PFCs
                        currentPFC_w[PFC_list.index(name)] = pfc.w
                PFCs_w.append(currentPFC_w)

                #learning rate decrement, if there is a schedule
                currentLearningRate = currentLearningRate - learningRateDecrement

            
            print(Fore.GREEN + Back.WHITE +"\n Run Number: "+ str(n))
            print(Fore.BLUE + Back.WHITE +"\n Final constraint weights:")
            printform= ''.join([('{:^'+str(len(cname)+3)+'s} ') for cname in self.trainingData.constraintNames])
            print( '\n'+printform.format(*[str(i) for i in self.trainingData.constraintNames]))
            print(printform.format(*[str(round(i,2)) for i in self.w])+Style.RESET_ALL)


            self.predict(outFilename+str(n)+".txt")
            
            with open(errRatesFilename+str(n)+".txt","w") as f:
                f.write("errorRate")
                f.write("\n")
                f.write("\n".join([str(e) for e in rates]))

            if self.lexC_type:
                with open(lexCweightsFilename+str(n)+".txt","w") as f:
                    columns = []
                    for col in lexCsOverTime[0]:
                        columns += [[]]
                    for line in lexCsOverTime:
                        for col in range(0,len(line)):
                            columns[col].append(line[col])

                    
                    newCols = []
                    for col in lexCsOverTime[0]:
                        newCols += [[]]
                    for col in range(0,len(columns)):
                        m = max([len(x) for x in columns[col]])
                        for l in columns[col]:
                            xtras = []
                            if len(l)<m: # fill out trailing zeros, to make each row the same length
                                xtras = [0]*(m-len(l))
                            newLine = [self.trainingData.constraintNames[col]]
                            newLine = newLine + l[1:] + xtras  # removing that first zero that is a placeholder
                            newCols[col].append(newLine)

                    #print(newCols)
                    #print first line
                    line1 = []
                    for column in range(0,len(columns)):
                        ncols = len(newCols[column][0])
                        conname = newCols[column][0][0]

                        for i in range(1,ncols):
                            line1.append(conname+str(i))

                    f.write("\t".join(line1))

                    for lineN in range(0,len(newCols[0])):
                        f.write("\n")
                        l = []
                        for colN in range(0,len(newCols)):
                            l += newCols[colN][lineN][1:]
                        
                        f.write("\t".join([str(j) for j in l]))

                with open(indexesFilename+str(n)+".txt","w") as f:
                    keys = list(self.trainingData.lexicon.keys())[:] # to preserve order
                    firstLine = []
                    for key in keys:
                        for c in self.trainingData.constraintNames:
                            firstLine.append(key+"_"+c+"_w")
                            firstLine.append(key+"_"+c+"_i")
                    f.write("\t".join(firstLine))

                    firstKey = keys[0]
                    for row in range(0,len(indexesOverTime[0][firstKey])): # these should all be the same length, the # of epochs
                        theRow = []
                        for lexkey in keys:
                            for c in range(0,len(indexesOverTime)): #constraints
                                weight = indexesOverTime[c][lexkey][row][0]
                                index = indexesOverTime[c][lexkey][row][1]
                                theRow.append(weight)
                                theRow.append(index)
                        f.write("\n")
                        f.write("\t".join([str(i) for i in theRow]))


            with open(weightsFilename+str(n)+".txt", "w") as f:
                #print(grammar_constraints_w)
                out = ""
                for ep in grammar_constraints_w:
                    out += "\n" + "\t".join([str(w) for w in ep])
                f.write(out)

            # print("learning complete")
            with open(pfcsFilename+str(n)+".txt", "w") as f:
                out = "\t".join(PFC_list)
                for ep in PFCs_w:
                    out += "\n" + "\t".join([str(pfc) for pfc in ep] + ["0" for i in PFC_list[len(ep):]])
                f.write(out)

            if self.lexC_type:
                with open(lexCsFilename+str(n)+".txt","w") as f:
                    out = ""
                    for i in range(0,len(self.lexCs)):
                        out += self.trainingData.constraintNames[i] + "\n"
                        for j in range(1,len(self.lexCs[i])):
                            out += str(self.lexCs[i][j]) + "\t"
                            for l in self.trainingData.lexicon:
                                if self.trainingData.lexicon[l].lexCindexes[i]==j:
                                    out += l + "\t"
                            out += "\n"
                        out += "\n"
                        #out += "\t".join([str(w) for w in self.lexCs[i][1:]]) + "\n"
                    f.write(out)

            with open(runSummaryFilename,"a") as f:
                f.write('\n')
                f.write('\t'.join([str(w) for w in self.w]+[str(self.SSE()),str(self.logLikelihood()),str(last10PerErr/last10PerCount)]))

        with open(self.logFile,"a") as f:
            f.write('\n')
            f.write(str(datetime.datetime.now())+'\t')
            f.write(self.trainingDatafile+'\t')
            f.write('\t'.join(self.trainingData.constraintNames))
            f.write('\t'+self.outfolder+'\t')
            f.write(self.label+'\t')
            f.write(self.startWeightParam+'\t')
            f.write(self.featuresFileName+'\t')
            f.write(str(self.addViolations)+'\t')
            f.write(str(self.constraintsModule)+'\t')
            f.write(str(self.generateCandidates)+'\t')
            f.write(str(self.learningRate)+'\t')
            f.write(str(self.decayRate)+'\t')
            f.write(str(self.comparisonThreshold)+'\t')
            f.write(str(self.useListedType)+'\t')
            f.write(str(self.p_useListed)+'\t')
            f.write(str(self.flip)+'\t')
            f.write(str(self.simpleListing)+'\t')
            f.write(str(self.pToList)+'\t')
            f.write(str(self.lexC_type)+'\t')
            f.write(str(self.pChangeIndexation)+'\t')
            f.write(str(self.lexCStartW)+'\t')
            f.write(str(self.localityRestrictionType)+'\t')
            f.write(str(self.firstIndexStrat)+'\t')
            f.write(str(self.PFC_type)+'\t')
            f.write(str(self.PFC_lrate)+'\t')
            f.write(str(self.PFC_startW)+'\t')

    def predict(self,outputName="output.txt",newInputName = "newInput.txt"):
        # saving all tableau to output file
        print("predicting")
        obs, pred = self.predictAll()
        results = [t.toFile() for t in pred]
        #print(results)
        with open(outputName, 'w') as f:
            f.write('\n'.join(results))
        print("Saving output predictions to "+Fore.CYAN+"output.txt"+Style.RESET_ALL)

        with open(newInputName,"w") as f:
            # print first line
            firstLine = ['input','lexeme','candidate','obs.prob','tab.prob']+self.trainingData.constraintNames[0:self.cfunctionStartIndex]
            f.write('\t'.join(firstLine))
            # get input counts from playlist
            inptCounts = {}
            for p in self.playlist:
                thisInpt = p[2]
                if thisInpt in inptCounts:
                    inptCounts[thisInpt] += 1
                else:
                    inptCounts[thisInpt] = 1

            for t,dat in zip(pred,obs):
                line = ["\n"]

                # input
                inpt = dat[2]
                # lexeme
                lexTags = dat[0]
                #print('lexeme')
                #print(dat[0])
                lexemes = []
                for l in lexTags:
                    individualMorphTags = l.tag.split("_")
                    #print(l.tag)
                    for m in individualMorphTags:
                        #print(m)
                        lexemeTag = ''.join(self.trainingData.lexicon[m].segmentList)
                        lexemes.append(lexemeTag)
                        #print(lexemes)
                lexeme = '_'.join(lexemes)
                #print(lexeme)

                # obs.prob
                # tab.prob
                if inpt in inptCounts:
                    tabProb = inptCounts[inpt]
                else:
                    tabProb = 0
                # violations

                for cand in t.candidates:
                    candidate = cand.c
                    obsProb = cand.predictedProb
                    violations = cand.violations[0:self.cfunctionStartIndex]

                    line = [inpt,lexeme,candidate,obsProb,tabProb]+violations
                    f.write('\n')
                    f.write('\t'.join([str(l) for l in line]))


    def makeTableau(self,datum,rich=False,testFcs=False):
        '''Make the tableau for learning '''
        ''' datum is an entry in a traningData.learnData object'''
        ''' it has the form [[lexeme1, lexeme2,...], surface string, input string]'''
        ''' 'input string' is from the input column of the spreadsheet '''

        # can now call by index in trainingData.learnData, or by input
        # This is for manual calling mostly, to examine what makeTableau is really doing
        if type(datum)==int:
            datum = self.trainingData.learnData[datum]
        elif type(datum)==str:
            for d in self.trainingData.learnData:
                if d[2] == datum:  # third entry of each datum is the input string
                    datum = d 
                    break  # We grab the first entry that matches the input, and break out of the loop
                           # The logic here is that all entries with the same input
                           # will yield basically the same tableau, and we don't want to hunt longer than necessary
                           # (esp if the trainingData is large!)
            if type(datum)==str: # If we didn't find the string in inputs
                print("ERROR: input " + datum + " not found in g.trainingData.learnData")
                return


        def lexemesToFaithCands(lexemes):
            #print("creating faithful candidates")
            #print(obsOutput)
            individualCands = []
            for l in lexemes:
                if rich:
                    individualCands.append(l.toRichCand(self.featureSet))
                else:
                    individualCands.append(l.toFaithString())
            if len(lexemes) > 1:
                faiths = list(itertools.product(*[i for i in individualCands]))
            else:
                faiths = individualCands

            # This is where you would put a scramble option

            # concatenate morphemes into faithful candidates
            fcs = [] # 'fc' = 'faithful candidate'
            for fc in faiths:
                if rich:
                    #print(fc)
                    # begin creating the new richCand
                    newSegsList = fc[0].segsList[:]
                    newSegsDict = fc[0].segsDict.copy()
                    newActivitys = fc[0].activitys[:]
                    newSuprasegmentals = fc[0].suprasegmentals[:]
                    for i in range(1, len(fc)):  # go through morphemes
                        # concatenate seglist
                        newSegsList += [seg + '_w' + str(i + 1) for seg in fc[i].segsList[:]]
                        for seg in fc[i].segsList:
                            # concatenate segsDict
                            newSegsDict[seg + '_w' + str(i + 1)] = fc[i].segsDict[seg][:]
                        newActivitys += fc[i].activitys[:]
                        newSuprasegmentals += fc[i].suprasegmentals[:] if fc[i].suprasegmentals else []  # Note that suprasegmentals is now an empty list if there are none, instead of NoneType
                    # TODO change richCand() so that empty list is the default if there are no suprasegmentals
                    newC = self.featureSet.featureToS(newSegsDict, newSegsList)
                    obsProb = 1 if newC == obsOutput else 0
                    containsObsOut = 1 if newC == obsOutput else 0

                    fcs.append(richCand(newC, [], obsProb, newSegsDict, newSegsList, None, newActivitys, newSuprasegmentals,surfaceForm=newC))

                else:
                    fcs.append("_".join([i for i in fc]))

            return fcs

        # def generateCandidates(cands):  <- candidate generation goes here


        def assemble(faithCands):
            #print("faithCands")
            #print(faithCands)
            # 'UR' could be:
            #   list of faithful candidates
            #       - richCands or plain strings

            if method == "deNovo":
                # UR should be richCand
                # generate candidates
                # assign violations
                #
                print('deNovo')

            else:
                # Initial tableau creation, from the input file
                tab = self.trainingData.tableaux[self.trainingData.tableauxTags.index(datum[2])].copy()
                tab.w = self.w[:]
                tab.constraintList = self.trainingData.constraintNames[:]
                #if self.noisy:
                    #print(tab)

                if method == "partial":
                    #print("assembling partial tableau")
                    # if using simple strings
                    for con in self.constraints:
                        tab.applyOneConstraint(con,faithCands)

                    # TODO if using richCands
                    # if using activity levels

                #if method == "full":
                    # we're done?

                # make sure all candidates have the right number of violations
                for cand in tab.candidates:
                    nEmptyViolations = len(self.w)-len(cand.violations)
                    cand.violations += [0]*nEmptyViolations

                return tab




        obsOutput = datum[1] #second member of datum is the surface string observed for this set of lexemes

        if testFcs:
            return lexemesToFaithCands(datum)



    #####################################################
    ### Determine method of creating tableau
    #####################################################

        method = "deNovo"
            # "deNovo": create a brand new tableau, with generated candidates.  For this we need operations, and constraints defined as functions
            # "partial": use user-defined candidates, but add violations of a few markedness constraints
            # "full": completely user-defined, except for perhaps the PFCs

        if not self.generateCandidates:
            if not self.addViolations:
                method = "full"
            elif self.constraints:  # constraint functions must exist for them to be used to assign new violations
                method = "partial"
            else:
                print("\nERROR: you must define a set of constraint functions")
                exit
        else:
            if self.constraints and self.operations:
                # TODO fill this out for UseListed; it might not work as expected at the moment.
                return createTableau(lexemes, self.constraints, self.operations, self.featureSet, datum[1], w=self.w[:])
            else:
                print("\nERROR: you cannot generate candidates without predefined operations and constraints")

        multipleInputs = 0



    ###################################################
    ### Calculate UseListed decisions
    ###################################################
        def useListedTabCreation():
            useListedIndex = self.cPairs[2]
            #print("checking_p_uselisted")
            listing = 0
            # check if a listed form exists for this input
            listedTag = "_".join([i.tag for i in datum[0]]) if len(datum[0]) > 1 else False
            if listedTag in self.trainingData.lexicon:
                # If the item has been listed at least once, look for other copies:
                listedTagsList = [listedTag]
                nCopies = 2
                while listedTag+"_"+str(nCopies) in self.trainingData.lexicon:
                    nCopies +=1
                    listedTagsList.append(listedTag+"_"+str(nCopies))
                # set the official listed tag to a randomly selected one from the list
                listedTag = random.choice(listedTagsList)

                # Now, we check how we are doing UseListed
                if self.p_useListed <= 1: # we sample completely randomly
                    if random.random()< self.p_useListed:
                        listing = 1

                elif self.p_useListed <= 2: # we sample based on frequency
                    f_composed = [lex.freq for lex in datum[0]]
                    f_listed = self.trainingData.lexicon[listedTag].freq

                    ####################################################
                    # To change how the frequency sampling works edit here
                    ####################################################
                    local_p_useListed = f_listed / (f_listed + min(f_composed))

                    if random.random() < local_p_useListed:
                        listing = 1

                else:  # we will return a hidden structure tableau
                    #print("Making hidden structure tableau")


                    # Create list of faithful cands for composed
                    fcs_composed = lexemesToFaithCands(datum[0])


                    # Create list of faithful cands for listed
                    fcs_listed = lexemesToFaithCands([self.trainingData.lexicon[listedTag]])
                    #print("fcs_listed")
                    #print(fcs_listed)

                    # merge tableaux, and  assign _composed vs. _listed violations correctly
                    # self.cPairs is a tuple (list_of_pairs, reverse_sorted_indices_of_listed, UseListed violation index )
                    tab = assemble(fcs_composed)
                    tab_listed = assemble(fcs_listed)
                    #for cand in tab_listed.candidates:
                    #    cand.c = re.sub("_","",cand.c)
                    #print(tab_listed)



                    for pair in self.cPairs[0]:
                        for cand in tab.candidates:
                            # set both columns equal to the _composed violation
                            cand.violations[pair[1]] = cand.violations[pair[0]]
                        for cand in tab_listed.candidates:
                            # set both columns equal to the _listed violation
                            cand.violations[pair[0]] = cand.violations[pair[1]]

                    for i in self.cPairs[1]:
                        for cand in tab.candidates:
                            cand.violations.pop(i)
                            # remove _listed violations
                    for i in self.cPairs[1]:
                        for cand in tab_listed.candidates:
                            cand.violations.pop(i)
                            # remove _listed violations

                    # make sure all candidates have the right number of violations
                    for cand in tab.candidates:
                        nEmptyViolations = len(self.w)-len(cand.violations)
                        cand.violations += [0]*nEmptyViolations
                    # make sure all candidates have the right number of violations
                    for cand in tab_listed.candidates:
                        nEmptyViolations = len(self.w)-len(cand.violations)
                        cand.violations += [0]*nEmptyViolations

                    for cand in tab.candidates:
                        cand.violations[useListedIndex] = 1
                        cand.c = cand.c+"_composed"
                    for cand in tab_listed.candidates:
                        cand.violations[useListedIndex] = 0
                        cand.c = cand.c+"_listed"

                    ## Now merge
                    # first, get indices of candidates derived from non-listed lexemes
                    composedCandIndices = list(range(0,len(tab.candidates)))
                    for cand in tab_listed.candidates:
                        tab.candidates.append(cand)
                    listedCandIndices = list(range(max(composedCandIndices)+1,len(tab.candidates)))

                    tab.hiddenStructure = True
                    multipleInputs = 1
                    multiInputType = 'useListed'
                    urList = [datum[0],[self.trainingData.lexicon[listedTag]]]

                    tab.lexemes = (urList,(composedCandIndices,listedCandIndices))
                    return tab


            #............................................#
            # If we didn't do a hidden structure tableau, we still need to make a tableau
            #............................................#
            if listing: # we're using a listed complex form
                datum[0] = [self.trainingData.lexicon[listedTag]]

                # create a tableau
                tab = assemble(lexemesToFaithCands(datum[0]))
                tab.lexemes = datum[0][:]  #Note the lexemes that were used

                # set _composed columns equal to _listed violations
                # (later, we'll remove the _listed violations)
                for cand in tab.candidates:
                    for pair in self.cPairs[0]:
                         cand.violations[pair[0]] = cand.violations[pair[1]]

                for i in self.cPairs[1]:
                    for cand in tab.candidates:
                        cand.violations.pop(i)
                        # remove _listed violations

                # Assign UseListed violations (always 0)
                # make sure all candidates have the right number of violations
                for cand in tab.candidates:
                    nEmptyViolations = len(self.w)-len(cand.violations)
                    cand.violations += [0]*nEmptyViolations

                if useListedIndex:
                    for cand in tab.candidates:
                        cand.violations[useListedIndex] = 0

            elif not listedTag: # we've only got one morpheme
                tab = assemble(lexemesToFaithCands(datum[0]))
                #print(tab)
                tab.lexemes = datum[0][:]  #Note the lexemes that were used

                # set _composed columns equal to _listed violations
                # (later, we'll remove the _listed violations)
                # we're basically calling the monomorpheme listed
                # could do this differently I suppose
                for cand in tab.candidates:
                    for pair in self.cPairs[0]:
                         cand.violations[pair[0]] = cand.violations[pair[1]]
 
                for i in self.cPairs[1]:
                    for cand in tab.candidates:
                        cand.violations.pop(i)
                        # remove _listed violations
                        
                # Assign UseListed violations (always 0)
                # make sure all candidates have the right number of violations
                for cand in tab.candidates:
                    nEmptyViolations = len(self.w)-len(cand.violations)
                    cand.violations += [0]*nEmptyViolations

                if useListedIndex:
                    for cand in tab.candidates:
                        cand.violations[useListedIndex] = 0


            else:
                tab = assemble(lexemesToFaithCands(datum[0]))
                #print(tab)
                #print(tab.candidates[0].violations)
                tab.lexemes = datum[0][:]  #Note the lexemes that were used
                # create a tableau


                for i in self.cPairs[1]:
                    for cand in tab.candidates:
                        cand.violations.pop(i)
                        # remove _listed violations

                # make sure all candidates have the right number of violations
                for cand in tab.candidates:
                    nEmptyViolations = len(self.w)-len(cand.violations)
                    cand.violations += [0]*nEmptyViolations

                #print(tab.candidates[0].violations)
                # Assign UseListed violations (all 1 because we're never listed)
                # crucially must take place before we remove _listed violations
                if useListedIndex:
                    for cand in tab.candidates:
                        cand.violations[useListedIndex] = 1

                #print(tab)

            # update frequencies of lexeme(s) used
            # Note that if we did a listed tableau, these will only update the listed form's lexical entry
            for lex in datum[0]:
                lex.lastSeen = self.t
                lex.freq += 1



            return tab
            #...............................................#
            # Finished making the tableau
            #...............................................#


        if self.p_useListed:
                tab = useListedTabCreation()
        else:
            # create a plain tableau
            fcs = lexemesToFaithCands(datum[0])
            tab = assemble(fcs)


      ########################################################################



        #if self.URCs:
            # Look on each lexeme for URCs
            # There should be at least one - if not, create one?

            # create a subtableau for each combination of URCs


            # cleanup for _listed vs. _composed constraints
            #if len(self.cPairs[1])>0:
                # if listed
                # remove _composed violations

                #if composed
                # remove _listed violations
                    #Do the _listed vs. _composed protocol



        #tab=assemble(lexemesToFaithCands(datum[0]))


        # Adjust for lexically indexed C's
        if self.lexC_type:
            tab.applyLexCs(self.lexCs,self,fcs,self.localityRestrictionType)

        # Apply PFCs, including to multiple distinct inputs if we have a multi-input tableau
        if self.PFC_type!= "none":
            tab.applyPFCs()


        return tab

    def lexCupdate(self,obs,pred,updateVector,lexemes,tab,learningRate):
        # print("updating lexCs")

        def updateLexCweight(self,weights,conIndex,thisLexemeIndex,update):
            #print(thisLexemeIndex)
            if thisLexemeIndex >= 0 and weights and weights[thisLexemeIndex]:
                self.lexCs[conIndex][thisLexemeIndex + 1] += update * learningRate

        def getMaxOrMinW(self,weights,update):
            if weights and update > 0:
                mn = False
                mx = max(weights) # keep max weight around if we're headed up
            elif weights and update < 0:
                mn = min(weights) # keep min weight around if we're headed down
                mx = False
            else: # we'll get here if weights is []
                mn = False
                mx = False

            return (mn,mx)

        def getDiffLexemes(self,obs,pred,lexemes):

            # parse candidates into morphemes
            obsParsed = obs.c.split("_")
            predParsed = pred.c.split("_")
            if len(obsParsed) != len(predParsed) or len(obsParsed) != len(lexemes):
                print(Fore.RED+ "\n ERROR: predicted and/or observed cannot be aligned with lexemes")
                print("predicted: " + pred.c)
                print("observed: " + obs.c)
                print("lexemes: " + ", ".join([l.tag for l in lexemes]))
                print(Style.RESET_ALL)

            diffLexemes = []
            for li in range(0, len(lexemes)):
                # find the lexeme that differs between obs and pred
                # update it and adjacent lexemes
                # If locality is set to 'overlap' or 'presence_only'

                if obsParsed[li] != predParsed[li] and li not in diffLexemes:
                    diffLexemes.append(li)
                if self.localityRestrictionType != "strict":
                    if li > 0 and li-1 not in diffLexemes:
                        diffLexemes.append(li-1)
                    if li < (len(lexemes) - 1) and li + 1 not in diffLexemes:
                        diffLexemes.append(li+1)

            return diffLexemes


        def induceOne(self,weights,genCindex,lex):
            newIndex = 0 if 0 not in weights else weights.index(0)+1
            if newIndex: # we're repopulating a slot that got decayed to zero
                self.lexCs[genCindex][newIndex] = self.lexCStartW
                lex.lexCindexes[genCindex] = newIndex
            else: # we're appending
                self.lexCs[genCindex].append(self.lexCStartW)
                lex.lexCindexes[genCindex] = len(self.lexCs[genCindex]) - 1

            weights = self.lexCs[genCindex][1:] # update the weights vector
            return weights


        def induce(self,obs,pred,lexemes,con,weights,update,lexCsInTableau):
            ''' con: the index of the constraint beinf indexed; can use for lexCs 
            '''
            diffLexemes = getDiffLexemes(self,obs,pred,lexemes)
            for dli in diffLexemes:
                lex = lexemes[dli]

                # check whether this lexeme has an indexed version already
                currentIndex = lex.lexCindexes[con] -1 # will be -1 if no indexed constraint yet
                #print(currentIndex)

                w = weights[currentIndex] if (weights and currentIndex>=0) else 0

                # if a lexC has decayed to (close enough to) zero, remove the indexation from the lexeme
                if w < self.decayRate:
                    lex.lexCindexes[con] = 0
                    currentIndex = -1
                    # print("re-indexed to zero")

                maxNreached = bool(len([w for w in weights if w > 0]) >= self.lexC_type)
                        
                if currentIndex == -1: # if there's not a lexC already
                    clonesAvailable = self.lexCs[con][1:]

                    if len([w for w in clonesAvailable if w >0])>0: # If indexed versions of this constraint already exist
                        # decide which clone to index this lexeme to
                        # the 'lowest' strategy
                        lowest = min([w for w in clonesAvailable if w >0])
                        cloneToTryIndex = clonesAvailable.index(lowest)

                        # the 'highest' strategy

                        # the random sampling by number of lexemes strategy


                        lex.lexCindexes[con] = cloneToTryIndex+1
                        if self.noisy:
                            print(self.trainingData.constraintNames[con] + " reindexed on "+ lex.tag + ". New clone is #" + str(cloneToTryIndex+1))
                    
                    else: # If there are no copies of this constraint yet
                        weights = induceOne(self,weights,con,lex)
                        if self.noisy:
                            print("inducing a new copy of " + self.trainingData.constraintNames[con] + " on  " + lex.tag)

                else: # if there is a lexC already, move the index instead
                    # first, find out if the indexed version actually makes a difference
                    realUpdate = False
                    genConstraintName = self.trainingData.constraintNames[con]
                    for l in lexCsInTableau:
                        if l[1] == genConstraintName and l[3] == lex.tag:
                            realUpdate = l[0]
                    if realUpdate: # if the indexed version actually distinguished between candidates
                        moveIndex(self,lex,weights,realUpdate,con)
                        # execute change indexation instead
                    else:
                        if type(realUpdate)== bool:
                            print(realUpdate)
                            print(lex.tag)
                            print(genConstraintName)
                            print(lexCsInTableau)
                            exit
                
        def moveIndex(self,lex,weights,update,genCindex):
            currentIndex = lex.lexCindexes[genCindex]-1
            w = weights[currentIndex]
            s = sorted(weights[:])
            currentSpotInSort = s.index(w)

            mn, mx = getMaxOrMinW(self,weights,update)
            if mx: # obs preferring -> reindex to greater weighted copy
                direction = 1
            else:  # pred preferring -> reindex to lower weighted copy
                direction = -1

            if w == mx:
                maxNreached = bool(len([w for w in weights if w > 0]) >= self.lexC_type)
                if not maxNreached:
                    # go induce on THIS lexeme only
                    weights = induceOne(self,weights,genCindex,lex)
                    return

                else:
                    updateLexCweight(self,weights,genCindex,currentIndex,update)
                    return
            
            elif w == mn:
                # current way: if we're at the lowest indexed C trying to go down, un-index
                lex.lexCindexes[genCindex]=0
                # old way: never un-index, just move the weight of the indexed C down
                #updateLexCweight(self,weights,genCindex,currentIndex,update)
                return

            # (else) find the next best weight
            move = 1
            while move:
                newWeight = s[currentSpotInSort + direction*move]
                if newWeight != w: # if we've actually changed weight
                    # we can leave the loop
                    move = 0
                else: # try moving a little farther
                    move += 1

            # whether to actually jump?
            wDiff = abs(newWeight - w)
            p_jump = (self.lexCjumpParameter)**wDiff
            # correct for pChangeIndexation
            p_jump = p_jump/self.pChangeIndexation

            if random.random() < p_jump:
                lex.lexCindexes[genCindex] = weights.index(newWeight) + 1


        updateVectorIndices = [j for j in range(0,len(updateVector))]
        # this contains violations of indexed constraints as well, and possibly other stuff

        #print(tab)
        # get tuples of (update, indexedCname, indexedCindex, lextag)
        lexCsInTableau = []
        for u in updateVectorIndices:
            if u >=len(self.w): # it's an indexed c

                label = tab.constraintList[u]
                parsedLabel = label.split("_")
                name = parsedLabel[0]
                index = int(parsedLabel[1])
                lexTag = parsedLabel[2]

                lexCsInTableau.append((updateVector[u],name,index,lexTag))


        constrIndicesThatMatter = [u for u in updateVectorIndices if updateVector[u] != 0 ]
        for con in constrIndicesThatMatter:  # go through updates that matter
            update = updateVector[con]

            if con >= len(self.w): # it's already an indexed constraint
                lexCinfo = lexCsInTableau[con-len(self.w)]
                update = lexCinfo[0]
                cname = lexCinfo[1]
                thisLexemeIndex = lexCinfo[2]-1
                lexTag = lexCinfo[3]
                genCindex = self.trainingData.constraintNames.index(cname)
                weights = self.lexCs[genCindex][1:]

                if random.random()< self.pChangeIndexation:
                    lex = self.trainingData.lexicon[lexTag]
                    moveIndex(self,lex,weights,update,genCindex)

                else: # update weights
                    updateLexCweight(self,weights,genCindex,thisLexemeIndex,update)

            else: # we're looking at a general constraint
                #print(self.lexCs)
                #print(con)
                weights = self.lexCs[con][1:] # vector of weights of indexed C's available for this constraint
                
                # should we induce?
                if random.random()<self.pChangeIndexation and update > 0: #only induce if the constraint needs to move *up*
                    induce(self,obs,pred,lexemes,con,weights,update,lexCsInTableau)


    def predictAll(self):
        globalNoise = self.noisy
        self.noisy=False

        tracker =[]
        observed = []
        predictions = []
        for datum in self.trainingData.learnData:
            if datum[0] not in tracker:
                tracker.append(datum[0])
                observed.append(datum)
                tab = self.makeTableau(datum)
                tab.predictProbsMaxEnt(tab.w)
                predictions.append(tab)

        # reset noisy value
        self.noisy = globalNoise

        return observed, predictions

    def SSE(self):
        observed, predictions = self.predictAll()
        sse = 0
        for tab in predictions:
            obs = tab.obsProbsList
            if tab.hiddenStructure:
                pred = []
                for s in tab.surfaceCands:
                    pred += [sum([c.predictedProb for c in tab.candidates if c.surfaceForm == s])]
                    print(pred)
                    # sum predicted probs of same surface forms
            else:
                pred = tab.predProbsList
            sse += sum([(o-p)**2 for o,p in zip(obs,pred)])
        return sse

    def logLikelihood(self):
        observed, predictions = self.predictAll()
        loglik = 0
        for tab in predictions:
            obs = tab.obsProbsList
            if tab.hiddenStructure:
                print(obs)
                pred = []
                for s in tab.surfaceCands:
                    pred += [sum([c.predictedProb for c in tab.candidates if c.surfaceForm == s])]
                print([math.log(p)*o for o,p in zip(obs,pred)])                    # sum predicted probs of same surface forms
            else:
                pred = tab.predProbsList
            loglik += sum([math.log(p)*o for o,p in zip(obs,pred)])

        return loglik


class IteratedLearning:
    def __init__(self,startState,nEpochs,itPerEpoch,pause=False,folderName="iterated_learning_output"):
        self.startState = startState
        self.currentState = startState
        self.nEpochs = nEpochs
        self.itPerEpoch = itPerEpoch
        self.pause = pause
        self.folderName = folderName
        #self.resultsList = []

    def iterate(self,nGenerations):
        for gen in range(0,nGenerations):
            self.currentState.learn(self.itPerEpoch,self.nEpochs)

            outputName = self.folderName+"/output_gen"+str(gen)+".txt"
            newInputName = self.folderName+"/input_gen"+str(gen+1)+".txt"
            print(newInputName)
            self.currentState.predict(outputName,newInputName)
            print("Generation "+str(gen)+" learned")
            
            #if self.pause:
            #    input("Press Enter to continue...")

            self.currentState = Grammar(self.startState.config,inputFile=newInputName)




class lexeme:
    def __init__(self, tag, segmentList=None, kind=None):
        self.tag = tag  # label for the lexeme, so the humans can easily see what it is.  ex. 'tagi' '-ina', even things like 'PV' or '3rdsing'
        self.segmentList = segmentList if segmentList else [i for i in tag]  # Human-readable list of segments, corresponding to feature lookup tables, if using
        self.segLabels = [self.segmentList[0]] + [
            self.segmentList[i] if self.segmentList[i] not in self.segmentList[:i] else self.segmentList[i] + str(i) for
            i in range(1,
                       len(self.segmentList))]  # create list of unique segment labels, to be used in candidate generation and evaluation by PFCs
        self.activitys = [1 for i in self.segmentList]  # List of float value activity levels for self.segs.  Defaults to 1 for all
        self.linearSegOrder = [i for i in range(1,len(self.segmentList) + 1)]  # integers specifying the linear order of segs in self.segs. starts at 1
        # Example: t/z/n ami:
        # self.segs = ['t','z','n','a','m','i']
        # self.activitys = [.4, .5, .6, 1, 1, 1]
        # self.linearSegOrder = [1, 1, 1, 2, 3, 4]
        self.kind = kind  # string specifying what kind of morpheme it is.  'root' 'suffix' 'prefix' etc. Optional
        self.freq = 1  # initialize at zero, increase during learning.  This number reflects the actual frequency of the lexeme during learning, rather than the frequency in the training data
        self.PFCs = []  # list of PFC objects, optional.
        self.lexCindexes = []  # list of indexation values for lex C's, indexing into Grammar.lexCs
        self.lastSeen = 0

    def __str__(self):
        out = 'Lexeme ' + str(self.tag) + ' (' + str(self.kind) + ', f:' + str(self.freq) + ' )\n'
        segform = '{:2s} ' * len(self.segmentList)
        out += segform.format(*self.segmentList)
        out += '\n'
        out += segform.format(*[str(i) for i in self.activitys])
        out += '\n'
        out += segform.format(*[str(i) for i in self.linearSegOrder])
        out += '\n'
        out += ''.join([i.name + ": " + str(i.w) + '\n' for i in self.PFCs]) if self.PFCs else 'No PFCs'
        return out

    def __repr__(self):
        r = ""
        if self.kind != None:
            r = ' - ' + str(self.kind)
        return self.tag + r

    def decayPFC(self, t, decayRate, decayType='static'):
        for pfc in self.PFCs:
            if decayType == 'static':
                #print(pfc.w)
                #print((float(t) - self.lastSeen))
                pfc.w -= (float(t) - self.lastSeen) * decayRate
                #print(pfc.w)
            elif decayType == 'L1':
                for i in range(self.lastSeen, t):
                    pfc.w -= decayRate * pfc.w
            elif decayType == 'L2':
                for i in range(self.lastSeen, t):
                    pfc.w -= (decayRate / 2) * (pfc.w ** 2)
        self.PFCs = [pfc for pfc in self.PFCs if pfc.w > 0]

    def toRichCand(self, featureSet):
        ''' produces the faithful candidate for just this one lexeme, given a Feature object, featureSet '''
        # TODO first check that all segments are even in featureSet

        # Now, get the segments in all possible orders
        segsInOrder = []
        segLabelsInOrder = []
        for i in range(1, max(self.linearSegOrder) + 1):
            indices = [index for index, value in enumerate(self.linearSegOrder) if value == i]
            if len(indices) > 0:
                segsInOrder.append([self.segmentList[i] for i in indices])
                segLabelsInOrder.append([self.segLabels[i] for i in indices])
        cands = list(itertools.product(*segLabelsInOrder))
        # violations: empty
        # observedProb: empty

        rcs = []
        for c in cands:
            # create string with numbers stripped
            strRep = ''.join([re.sub('[0-9]', '', s) for s in c])
            segsDict, segsList = featureSet.stringToF(strRep, list(c))
            a = [self.activitys[self.segLabels.index(i)] for i in c]
            rcs.append(richCand(''.join(c), [], 0, segsDict, segsList, activitys=a))
        return rcs


    def toFaithString(self):
        # A B C
        # 1 3 2
        UR = ""
        for i in range(1,len(self.linearSegOrder)+1):
            if i in self.linearSegOrder:
                # check that the order is unique
                if len([j for j in self.linearSegOrder if j==i]) >1:
                    raise Exception("You have more than one segment in the "+i+"'th spot.  Please use lexeme.toRichCand instead of lexeme.toFaithString()")
                ind = self.linearSegOrder.index(i)
                UR += self.segmentList[ind]
        return [UR]

class PFC:  # Contains function(s) for calculating a PFC's violations
    def __init__(self, w, feature=None, seg=None, seg2=None, surfaceString=None, typ='feature_on_segment'):
        self.w = w
        self.feature = feature  # must be a tuple (0, 'high'), (1, 'coronal') etc.
        self.seg = seg  # name of a seg in the lexeme that this PFC belongs to
        self.seg2 = seg2  # note that seg names must be immutable in the lexeme!
        self.surfaceString = surfaceString  # the surface string to match if it's a pseudoPFC
        self.typ = typ  # typ can be 'feature_on_segment', 'exists_feature', 'prec', 'suprasegmental', or 'pseudo'

        # auto-calculate PFC type
        # note that type 'suprasegmental' must be defined by the function call, and cannot be specified within (it can't be distinguished in form from exists_feature)
        if feature is None and seg is not None and seg2 is not None:
            self.typ = 'prec'
            self.name = seg + '<<' + seg2

        elif feature is not None and seg is None and seg2 is None and typ != 'suprasegmental':
            self.typ = 'exists_feature'
            self.name = str(feature)

        elif surfaceString is not None and feature is None and seg is None and seg2 is None:
            self.typ = 'pseudo'

        elif feature is not None and typ == 'suprasegmental':
            pass
        elif feature is not None and seg is not None and typ == 'feature_on_segment':
            pass
        else:
            print("ERROR: you tried to create an impossible type of PFC.")
            exit()

        self.name = '_'.join([str(param) for param in [feature, seg, seg2, surfaceString] if param])

    def __eq__(self, other):
        same = 0
        if self.feature == other.feature and self.seg == other.seg and self.seg2 == other.seg2 and self.surfaceString == other.surfaceString:
            same = 1
        return same

    def __str__(self):
        return self.name

    def evaluate(self, cand):  # evaluates a richCand object, or a simple string for a pseudoPFC
        if self.typ == 'feature_on_segment':
            viol = 0 if self.feature in cand.segsDict.get(self.seg, []) else 1
        elif self.typ == 'exists_feature':
            viol = 0 if self.feature in [i for i in chain(*cand.segsDict.values())] else 1
        elif self.typ == 'prec':
            # order of seg1 is segsOrder[segsList.index(seg1)]
            if self.seg in cand.segsList and self.seg2 in cand.segsList:
                viol = 0 if cand.segsOrder[cand.segsList.index(self.seg)] < cand.segsOrder[
                    cand.segsList.index(self.seg2)] else 1
            else:
                viol = 1
        elif self.typ == 'suprasegmental':
            viol = 0 if self.feature in cand.suprasegmentals else 1
        elif self.typ == 'pseudo':
            # this one evaluates a string, pre-parsed out of a cand object
            viol = 0 if self.surfaceString == cand else 1
        else:
            print(
                "Error!  You've passed the PFC something that's not a valid type.  Types are 'feature_on_segment', 'prec', 'exists_feature', 'suprasegmental'")
        return viol


# TODO more thorough testing of PFC functionality

class trainingData:
    '''essentially, a list of lexeme sets paired with correct surface forms, and frequencies '''

    def __init__(self, filename):
        self.lexicon = {}  # dictionary of {tag: lexeme}
        self.learnData = []  # each entry is a list: [lexemes,surface,input].  lexemes is itself a list, of all lexemes involved in the entry
        self.sampler = []  # summed to 1, sampler for each learnData entry
        # derived from either obs.prob, or tab.prob*obs.prob, if tab.prob is present

        self.noisy = True  # If true, will print out lots of junk as it reads in
        self.tableaux = []  # If candidates appear in the input file, this will contain tableaux, otherwise it will be empty
        self.tabProb = []  # a separate sampler for tableaux specifically, for use in simple tableau-based learning.
        self.tableauxTags = []  # tag of each tableau.  Should correspond to the 'input' column in the data
        self.constraintNames = []  # If columns appear after all the pre-determined column types, they will be interpreted as constraints

        # What kind of input file is this
        candidates = False
        hidden = False
        freq_weighted = False
        specialLex = False

        f = open(filename, "r")
        lines = f.readlines()
        header = lines[0].split('\t')
        header = [label.strip() for label in header]
        constraintsStartAt = 0  # At which column do the constraint names start
        if 'input' in header:
            iIndex = header.index('input')
            constraintsStartAt += 1
        else:
            print(Fore.RED +
                "\nERROR: No column of your input file is labeled 'input'.  This column is required, and must be labelled exactly.  Please check your input file and try again" + Style.RESET_ALL)
            sys.exit()

        if 'obs.prob' in header:
            oIndex = header.index('obs.prob')
            constraintsStartAt += 1
        else:
            print(Fore.RED +
                "\nERROR: No column of your input file is labeled 'obs.prob'.  This column is required, and must be labelled exactly.  Please check your input file and try again"+ Style.RESET_ALL)
            sys.exit()
        if 'candidate' in header:
            candidates = True
            cIndex = header.index('candidate')
            constraintsStartAt += 1
            if self.noisy:
                print(Fore.CYAN + "\nYour input file contains candidates, therefore candidates will not be generated for you." + Style.RESET_ALL)
        if 'surface' in header:
            hidden = True  # Its always going to be hidden, right? cause if there are no candidates then the tableau generation system will generate hidden structure
            sIndex = header.index('surface')
            constraintsStartAt += 1
            if self.noisy:
                print(Fore.CYAN +
                    "\nYour input file contains hidden structure!  Yay!  I'll try to fit that with Expectation-Maximization according to Jarosz (2013)"+ Style.RESET_ALL)
            # TODO create more nuanced printout for lexeme files
        if 'tab.prob' in header:
            freq_weighted = True
            tpIndex = header.index('tab.prob')
            constraintsStartAt += 1
            if self.noisy:
                print(Fore.CYAN +
                    "\nYour input file contains input frequency information (it's the column labelled, somewhat opaquely, 'tab.prob')  Learning will therefore proceed according to this frequency-weighting. \n Note that you can turn off frequency weighting by... "+Style.RESET_ALL)  # TODO include note about how to turn off frequency weighting
        if 'lexeme' in header:
            specialLex = True
            lIndex = header.index('lexeme')
            constraintsStartAt += 1
            if self.noisy:
                print(Fore.CYAN +
                    "\nYour input file contains specially defined lexemes.  I'll use lexeme names from the 'input' column, but lexeme phonemes from the 'lexeme' column." + Style.RESET_ALL)

        if len(header) > constraintsStartAt:
            self.constraintNames = header[constraintsStartAt:]

        inpt_s = []
        lineNo = 0
        for i in lines[1:]:
            lineNo+=1
            l = [j.strip() for j in i.split('\t')]
            inpt = l[iIndex]

            # Add lexemes
            lex = inpt.split("_")
            nMorphs = len(lex)
            if specialLex:
                splex = l[lIndex].split("_")
                parsed = []
                for sp in splex:  # faqa_alo-f-ia
                    split = sp.split('-')
                    for m in range(0, len(split)):
                        if m % 2:
                            prev = parsed[-1]  # [segments, activities]
                            segments = prev[0] + split[m]  # 'alof'    'faqaf'   'falof'
                            act = prev[1] + [0 for c in split[m]]  # [1,1,1,0]    [0,1,1,1,0]
                            parsed.append([segments, act])
                        elif m > 1:  # greater than 1 and NOT even - entry before was liason
                            segments = split[m - 1] + split[m]  # 'fia'    'falo'
                            act = [1 for c in split[m - 1]] + [0 for c in split[m]]  # [0,1,1]  [0,1,1,1]
                            parsed.append([segments, act])
                        else:  # m=0, the first thing
                            segments = split[m]
                            act = [1 for c in split[m]]
                            parsed.append([segments, act])
                if len(parsed) != nMorphs:
                    raise Exception(Fore.RED + "ERROR: The number of morphemes in the lexeme column does not match the number in the input column. Problem: "+inpt + " "+ l[lIndex]+ "line no. "+str(lineNo)+Style.RESET_ALL)
                # TODO functionality for if the input has a LOT of ambiguous material '-asdhjk-' split over multiple morphemes
                splex = parsed

            else:
                splex = lex

            lexList = []  # to be filled with lexeme objects
            for item, sp in zip(lex, splex):
                if item not in self.lexicon:  # changed lexicon to a dictionary
                    if specialLex:
                        self.lexicon[item] = lexeme(item, [character for character in sp[0]])
                        self.lexicon[item].activitys = sp[1]
                    else:
                        self.lexicon[item] = lexeme(item, [character for character in sp])

                lexList.append(self.lexicon[item])

            if inpt not in inpt_s:  # If we haven't seen this input before
                inpt_s.append(inpt)
                if candidates:
                    if freq_weighted:
                        p = l[tpIndex]
                    else:
                        p = 1

                    self.tabProb.append(p)  # Note that only the first tab.prob value in a tableau with many candidates will be recorded.
                    self.tableaux.append(Tableau(inpt, p, hidden, lexemes=lexList,constraintNames=self.constraintNames))
                    self.tableaux[-1].constraintList = self.constraintNames  # Assign each tableau the constraint names from the input file
                    self.tableauxTags.append(self.tableaux[-1].tag)
                # create a new Tableau object for a unique input

            if candidates:  # If there are candidates, populate the tableaux
                c = l[cIndex]
                if len(c.split("_")) != nMorphs:
                    raise Exception(Fore.RED + "\nERROR: A candidate does not have the same number of morphemes as the input column.  Problem at: "+ inpt + " "+ c+ "line no. "+str(lineNo)+ Style.RESET_ALL)
                s = l[sIndex] if hidden else c  # surface form, defaults to candidate form if no hidden struct
                if len(s.split("_")) != nMorphs:
                    raise Exception(Fore.RED + "\n ERROR: A surface form does not have the same number of morphemes as the input column.  Problem at: "+ inpt + " "+ s+ "line no. "+str(lineNo) + Style.RESET_ALL)
                v = [float(viol) for viol in l[constraintsStartAt:]]  # Note that this could be empty
                self.tableaux[-1].addCandidate(candidate(c, v, l[oIndex], s))

            # TODO check
            # self.learnData.append([lexList,l[sIndex]])# This line is meant to represent *correct* output
            # There are two ways this can go:
            # 1) they give a simple input file, with each observed output on a separate line, with obs.prob indicating how often that appears
            # 2) they give an input file with whole tableaux in it, so need to calculate which are the observed outputs (which have any probability)

            # ok wait this is easier than I think
            if hidden:
                self.learnData.append([lexList, l[sIndex], inpt])
            elif candidates:
                self.learnData.append([lexList, l[cIndex], inpt])
            else:
                print(Fore.RED +
                    "\nERROR: no column with surface forms in it.  Please add either a 'candidate' column, or a 'surface' column"+Style.RESET_ALL)
                sys.exit()
            if freq_weighted:
                self.sampler.append(float(l[tpIndex]) * float(l[oIndex]))
            else:
                self.sampler.append(float(l[oIndex]))

        f.close()
        self.sampler = [s / sum(self.sampler) for s in self.sampler]  # convert to a well-formed distribution

    # TODO do I have to worry about these getting too small

    def __str__(self):
        trainTags = []
        for i, k in zip(self.learnData, self.sampler):
            entry = []
            for j in i[0]:
                entry.append(j.tag)
            entry = ["+".join(entry)]
            entry.append(i[1])
            entry.append(str(round(k, 4)))
            trainTags.append(entry)

        maxLen_lex = str(max([len(i[0]) for i in trainTags] + [7]) + 1)
        maxLen_out = str(max([len(i[1]) for i in trainTags] + [7]) + 1)
        segform = ('{:' + maxLen_lex + 's} ') + ('{:' + maxLen_out + 's} ') + ('{:8}')

        out = "Training Data: "
        out += '\n'
        out += segform.format("input", "surface", "training probability")
        for i in trainTags:
            out += '\n'
            out += segform.format(*i)

        return out

    def printLexicon(self):
        print(str(len(self.lexicon))+ " lexemes:")
        for l in self.lexicon:
            print(self.lexicon[l])

    #what does this do??
    def decayLexemes(self):
        for lex in self.lexicon:
            self.lexicon[lex]



def diffCands(cbase, cdiff,skipChar='x'):  # Use Damerau-Levenshtein distance, but with n features different as 'weights'
    # Takes richCand() objects
    # This code adapted from gist.github.com/badocelot/5327337
    # Explanation here: https://www.lemoda.net/text-fuzzy/damerau-levenshtein/index.html
    # assumes cbase and cdiff use the same feature sets, so their .segs dictionaries all have the same length of feature vectors
    # Used to prevent transposition for first characters
    INF = len(cbase.segsList) * len(list(cbase.segsDict.values())[0]) + len(cdiff.segsList) * len(
        list(cdiff.segsDict.values())[0])

    # Matrix: (M+2) x (N+2)   M - len cbase, N - len cdiff
    matrix = [[INF for n in range(len(cdiff.segsList) + 2)]]
    matrix += [[INF] + [i * len(list(cdiff.segsDict.values())[0]) / 2 for i in range(len(cdiff.segsList) + 1)]]
    matrix += [[INF, m * len(list(cbase.segsDict.values())[0]) / 2] + [0] * len(cdiff.segsList) for m in
               range(1, len(cbase.segsList) + 1)]

    # last_row = {} # Holds the last row each element was encountered

    # Matrix to hold the changes that were chosen at each step - two levels smaller than the distance matrix - no INF col, and ignoring the initialized epenthesis/deleiton columns
    # entries will be tuples (row_from,col_from,change)
    # change is a tuple too - (TYPE,[features that were added/deleted/overwritten])

    change_matrix = [[0] * (len(cdiff.segsList) + 2) for m in range(len(cbase.segsList) + 2)]
    # Fill in Deletion and Epenthesis changes into change_matrix
    i = 2
    for seg in cdiff.segsList:
        change_matrix[1][i] = (1, i - 1, ('EPEN'))
        i += 1

    i = 2
    for seg in cbase.segsList:
        change_matrix[i][1] = (
            i - 1, 1, ('DEL', [f for f in cbase.segsDict[cbase.segsList[i - 2]] if f[0] != skipChar]))
        i += 1

    # Fill in costs
    for row in range(1, len(cbase.segsList) + 1):
        seg_base = [f for f in cbase.segsDict[cbase.segsList[row - 1]] if f[0] != skipChar]

        # last_match_col = 0  # column of last match on this row

        for col in range(1, len(cdiff.segsList) + 1):
            seg_diff = [f for f in cdiff.segsDict[cdiff.segsList[col - 1]] if f[0] != skipChar]

            # fill in last row:
            # last_matching_row = last_row.get(tuple(seg_diff), 0)

            # cost of substitution
            d, ch1, ch2 = distSegs(cbase.segsDict[cbase.segsList[row - 1]], cdiff.segsDict[cdiff.segsList[col - 1]])
            cost = 0 if seg_base == seg_diff else d

            # compute substring distances
            feat_change = matrix[row][col] + cost
            epen = matrix[row + 1][col] + len(seg_diff) / 2
            delete = matrix[row][col + 1] + len(seg_base) / 2
            # TODO add as an option

            # transpose = matrix[last_matching_row][last_match_col]
            # + (row - last_matching_row - 1)*len(list(cbase.segs.values())[0]) + 1
            # + (col - last_match_col -1)*len(list(cbase.segs.values())[0])

            matrix[row + 1][col + 1] = min(feat_change, epen, delete)  # ,transpose)

            # order of assumptions: epen, delete, feature change, transposition
            # TODO: probly make this easily editable by the user
            if epen == matrix[row + 1][col + 1]:
                change_matrix[row + 1][col + 1] = (
                    row + 1, col, ('EPEN'))  # ,seg_diff)) #writing down seg_diff here is useless

            elif delete == matrix[row + 1][col + 1]:
                change_matrix[row + 1][col + 1] = (row, col + 1, ('DEL', seg_base))

            elif feat_change == matrix[row + 1][col + 1]:
                change_matrix[row + 1][col + 1] = (row, col, ('CHANGE', ch2))

        # elif transpose == matrix[row+1][col+1]:
        #   change_matrix[row+1][col+1] = (last_matching_row,last_match_col,('TRANSPOSE'))

        # matrix[row+1][col+1] = min(
        #   matrix[row][col] + cost, # feature changes
        #   matrix[row+1][col] +len(seg_diff),   # epenthesis
        #   matrix[row][col+1] +len(seg_base),   # deletion

        # transposition (metathesis)  NOTE: This assumes that any material between metathesized things is added/deleted
        # matrix[last_matching_row][last_match_col]
        #   + (row - last_matching_row - 1)*len(list(cbase.segs.values())[0]) + 1
        #   + (col - last_match_col -1)*len(list(cbase.segs.values())[0])
        # )

        # if cost ==0:
        #   last_match_col = col

    # last_row[tuple(seg_base)] = row
    # print(change_matrix, matrix)
    i, j, change = change_matrix[-1][-1]
    backtrace = [change]
    # print(i,j)
    while change_matrix[i][j] != 0:
        i, j, change = change_matrix[i][j]
        backtrace.append(change)
    # print(i,j,change)

    # Use segs identities from cbase, because that is the observed form, and therefore the form that we are trying to assert

    return matrix[-1][-1], matrix, change_matrix, backtrace


def inducePFCs(cbase, cdiff, featureSet, lamb=5):
    '''Induce PFC's to prefer cbase over cdiff.  For now, this function only induces feature exists constraints, and feature on segment constraints.  Precendence constraints must be constructed later, after the diffCands() function includes a proper cost analysis for a transposition.

    lamb is the lambda value for the Poisson distribution over number of constraints that will be induced.  It's the mean number of constraints to induce.'''
    dist, m, chm, backtrace = diffCands(cbase, cdiff, skipChar=featureSet.skipChar)
    # Note: Deletions will not contain skipChar values, but feature changes will

    listOfPFCs = []
    for ch, seg in zip(backtrace[::-1], cbase.segsList):
        for f in ch[1]:
            if ch != 'EPEN':
                # feature_on_segment
                listOfPFCs.append((10, f, seg))
                # TODO 10 is the initial weight of PFC's - a parameter of learning

                # feature exists
                listOfPFCs.append((10, f))

    nPFCs = np.random.poisson(lamb, 1)[0]
    nPFCs = len(listOfPFCs) if len(listOfPFCs) <= nPFCs else nPFCs
    return random.sample(listOfPFCs, nPFCs)


def distSegs(s1, s2):  # distance = n features that are different
    ''' takes two lists of features, and compares them '''
    # Note: this one has to take in full feature sets with skipChar values intact.
    # The idea: a change from specified to unspecified 'counts' as a change just as much as 0-1 or 1-0
    s1_not_s2 = [i for i in s1 if i not in s2]
    s2_not_s1 = [i for i in s2 if i not in s1]
    if len(s1_not_s2) == len(s2_not_s1):
        dist = len(s1_not_s2)
    else:

        dist = "ERROR"
    return dist, s1_not_s2, s2_not_s1


def exampleCand2():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg3 = [(0, "back"), (0, "high"), (0, "front"), (0, "low")]  # ah
    segs = {"seg1": seg1, "seg3": seg3}
    order = ["seg1", "seg3"]
    user_defined = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return candidate(1, segs=segs, order=order, user_defined=user_defined)


def exampleCand3():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg3 = [(0, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg3": seg3}
    order = ["seg1", "seg3"]
    user_defined = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return candidate(1, segs=segs, order=order, user_defined=user_defined)


def exampleCand4():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg3 = [(0, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg3": seg3}
    order = ["seg1", "seg3", "seg1", "seg3"]
    user_defined = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return candidate(1, segs=segs, order=order, user_defined=user_defined)


def exampleCand5():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    seg2 = [(1, "back"), (1, "high"), (0, "front"), (0, "low")]  # u
    seg3 = [(0, "back"), (0, "high"), (0, "front"), (1, "low")]  # a
    segs = {"seg1": seg1, "seg2": seg2, "seg3": seg3}
    order = ["seg1", "seg2", "seg3"]
    user_defined = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return candidate(1, segs=segs, order=order, user_defined=user_defined)


def exampleCand6():
    seg1 = [(0, "back"), (1, "high"), (1, "front"), (0, "low")]  # i
    segs = {"seg1": seg1}
    order = ["seg1", "seg1"]
    user_defined = [(0, "stress1syll"), (1, "stress2syll"), (0, "stress3syll")]
    return candidate(1, segs=segs, order=order, user_defined=user_defined)
