def createTableau(lexemes, constraints, operations, featureSet, obsOutput, w=None, scramble=False):
    '''create a tableau from lexemes, constraints, operations'''
    # lexemes is an ordered list of lexemes, or a single lexeme
    # TODO expand to more than two lexemes
    # TODO separate out markedness and faithfulness
    # constraints, operations, are lists of functions.  see constraints.py for details
    if not w:
        w = [0 for c in constraints]
    constraintList = [c.name for c in constraints]

    if not scramble:
        individualCands = []
        for l in lexemes:
            individualCands.append(l.toRichCand(featureSet))
        if len(lexemes) > 1:
            faiths = list(itertools.product(individualCands[0], individualCands[1]))
        else:
            faiths = individualCands
    # TODO This is where it's limited to two lexemes only
    # toDONE!  no longer limited!

    # TODO implement scramble option

    # concatenate richCands
    fcs = []  # 'fc' = 'faithful candidate'
    containsObsOut = 0
    for fc in faiths:
        # begin creating the new richCand
        newSegsList = fc[0].segsList[:]
        newSegsDict = fc[0].segsDict.copy()
        newActivitys = fc[0].activitys[:]
        newSuprasegmentals = fc[0].suprasegmentals[:] if fc[0].suprasegmentals else []
        for i in range(1, len(fc)):  # go through morphemes
            # concatenate seglist
            newSegsList += [seg + '_w' + str(i + 1) for seg in fc[i].segsList[:]]
            for seg in fc[i].segsList:
                # concatenate segsDict
                newSegsDict[seg + '_w' + str(i + 1)] = fc[i].segsDict[seg][:]
            newActivitys += fc[i].activitys[:]
            newSuprasegmentals += fc[i].suprasegmentals[:] if fc[
                i].suprasegmentals else []  # Note that suprasegmentals is now an empty list if there are none, instead of NoneType
        # TODO change richCand() so that empty list is the default if there are no suprasegmentals
        newC = featureSet.featureToS(newSegsDict, newSegsList)
        obsProb = 1 if newC == obsOutput else 0
        containsObsOut = 1 if newC == obsOutput else 0

        fcs.append(richCand(newC, [], obsProb, newSegsDict, newSegsList, None, newActivitys, newSuprasegmentals,
                            surfaceForm=newC))

    # Assign markedness violations to faithful candidates
    cs = [c.c for c in fcs]
    for fc in fcs:
        for con in constraints:
            fc.violations.append(con.assignViolations(fc, featureSet))

    allCands = fcs
    # for c in allCands:
    #   print(c)

    # Generate new candidates, dropping off at a rate controlled by A as you get farther down the 'tree' and rejecting them if they are not harmonically improving, according to s
    moarCandidates = 1
    t = 1  # 'time', or the depth in the tree
    A = 10  # higher -> more candidates (keep traversing the tree)
    s = 20  # sigmoid parameter  higher--> more candidates
    while moarCandidates:
        for o in operations:
            for c in allCands:
                # apply o with probability A/t
                if random.random() < A / t or not (containsObsOut):  # Continue to generate candidates until you generate the observed output
                    try:
                        candidates = o(c, featureSet)
                    except:
                        print("Error, trying to apply operation  to candidate ", c)
                    if type(candidates) == tuple:
                        candidates, *_ = candidates
                    # print(candidates)
                    candidates = [can for can in candidates if can.c not in cs]
                    # TODO check operations list also to establish sameness
                    for possibleCand in candidates:
                        for con in constraints:
                            # print('1')
                            #   print(con.name)
                            possibleCand.violations.append(con.assignViolations(possibleCand, featureSet))
                        #   print("violations: ",possibleCand.c)
                        #   print(possibleCand.violations)

                        # for possibleCand in candidates:
                        #   print(possibleCand.violations)

                        if possibleCand.surfaceForm == obsOutput:
                            containsObsOut = 1
                            possibleCand.observedProb = 1
                            allCands.append(possibleCand)
                            cs.append(possibleCand.c)
                        else:
                            possibleCand.harmony = -sum(
                                viol * weight for viol, weight in zip(possibleCand.violations, w))
                            Hdiff = possibleCand.harmony - c.harmony
                            p_keep = (1 / 2) * Hdiff / math.sqrt(
                                s + Hdiff ** 2) + 0.5  # Here is the equation for keeping a candidate based on harmony
                            if random.random() < p_keep:
                                possibleCand.observedProb = 1 if possibleCand.surfaceForm == obsOutput else 0
                                allCands.append(possibleCand)
                                cs.append(possibleCand.c)

        t += 1
        if random.random() < (1 - (A / t)) ** (len(operations)) or not (containsObsOut):
            # Halt candidate generation
            moarCandidates = 0

    # assign PFC violations:

    wNum = 0
    for l in lexemes:
        if l.PFCs:
            for pfc in l.PFCs:
                if wNum:
                    for cand in allCands:
                        # Have to actually make a copy to evaluate
                        # fill in 'w2', 'w3' etc on segment labels on the candidates
                        newPFC = PFC(pfc.w, pfc.feature, pfc.seg, pfc.seg2, pfc.typ)
                        newPFC.seg = newPFC.seg + '_w' + str(wNum + 1) if newPFC.seg else None
                        newPFC.seg2 = newPFC.seg2 + '_w' + str(wNum + 1) if newPFC.seg2 else None
                        cand.violations.append(newPFC.evaluate(cand))
                        cand.harmony += -cand.violations[-1] * newPFC.w
                else:
                    for cand in allCands:
                        cand.violations.append(pfc.evaluate(cand))
                        cand.harmony += -cand.violations[-1] * pfc.w
                constraintList.append((pfc.name, pfc))
                w.append(pfc.w)
        wNum += 1

    tab = Tableau("_".join([l.tag for l in lexemes]))
    for cand in allCands:
        tab.addCandidate(cand)

    return tab, constraintList, w


# test code:

