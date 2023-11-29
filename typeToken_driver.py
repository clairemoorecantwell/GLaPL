import learner as l
import math
import re

outfile = "gridSearchOutput4.txt"

# settings in config.gl that are the same across runs
# learning rate: 0.01
# decay rate: 0 (may add another batch with some decay)
# locality: overlap
# first_index_strategy: lowest
# no PFCs or listing, no violations added by function

def autoconfig(trainingData,outfolder="GLaPL_output",label="default",weights=0,featureSet="hungarianFeatures",addViolations=False,constraints=None,generateCandidates=False,learningRate=0.01,decayRate=0,decayType="L2",threshold=1,noisy="no",useListedType="none",useListedRate=1,flip=False,simpleListing=False,pToList=0.5,nLexCs=0,pChangeIndexation=0.5,lexCStartW=10,locality="overlap",first_index_strategy="lowest",PFC_type="none",PFC_lrate=0.1,PFC_startW=10,logFile="GLaPL_log"):
    with open("autoconfig.gl","w") as f:
        f.write("trainingData: ")
        f.write(str(trainingData))
        f.write("\n")
        f.write("outfolder: ")
        f.write(str(outfolder))
        f.write("\n")
        f.write("label: ")
        f.write(str(label))
        f.write("\n")
        f.write("weights: ")
        f.write(str(weights))
        f.write("\n")
        f.write("featureSet: ")
        f.write(str(featureSet))
        f.write("\n")
        f.write("addViolations: ")
        f.write(str(addViolations))
        f.write("\n")
        f.write("constraints: ")
        f.write(str(constraints))
        f.write("\n")
        f.write("generateCandidates: ")
        f.write(str(generateCandidates))
        f.write("\n")
        f.write("learningRate: ")
        f.write(str(learningRate))
        f.write("\n")
        f.write("decayRate: ")
        f.write(str(decayRate))
        f.write("\n")
        f.write("decayType: ")
        f.write(str(decayType))
        f.write("\n")
        f.write("threshold: ")
        f.write(str(threshold))
        f.write("\n")
        f.write("noisy: ")
        f.write(str(noisy))
        f.write("\n")
        f.write("useListedType: ")
        f.write(str(useListedType))
        f.write("\n")
        f.write("useListedRate: ")
        f.write(str(useListedRate))
        f.write("\n")
        f.write("flip: ")
        f.write(str(flip))
        f.write("\n")
        f.write("simpleListing: ")
        f.write(str(simpleListing))
        f.write("\n")
        f.write("pToList: ")
        f.write(str(pToList))
        f.write("\n")
        f.write("nLexCs: ")
        f.write(str(nLexCs))
        f.write("\n")
        f.write("pChangeIndexation: ")
        f.write(str(pChangeIndexation))
        f.write("\n")
        f.write("lexCStartW: ")
        f.write(str(lexCStartW))
        f.write("\n")
        f.write("locality: ")
        f.write(str(locality))
        f.write("\n")
        f.write("first_index_strategy: ")
        f.write(str(first_index_strategy))
        f.write("\n")
        f.write("PFC_type: ")
        f.write(str(PFC_type))
        f.write("\n")
        f.write("PFC_lrate: ")
        f.write(str(PFC_lrate))
        f.write("\n")
        f.write("PFC_startW: ")
        f.write(str(PFC_startW))
        f.write("\n")
        f.write("logFile: ")
        f.write(str(logFile))
        f.write("\n")

        
# try different numbers of lexCs
nlexCss = [2] #[2,12,24]  #done: 2,24

# try different start weights:
startws = [1] #[1,10,2,5] #done: 1, 10

# try different pChangeIndexation:
pChanges = [0.75] #[0.01,0.99,0.05,0.1,0.25,0.5,0.75] # done: 0.01,0.99

# for each of these, have to learn on 
trainingFiles =["typeTokenInput_50","typeTokenInput_37pt5","typeTokenInput_25","typeTokenInput_12pt5","typeTokenInput_4pt7","typeTokenInput_opposing","typeTokenInput_exaggerated"]

with open(outfile,"w") as f:
    f.write("\t".join(["filetag","runNo","nlexCs","lexCstartW","pChangeIndexation","inputSet","likelihood","SSE","w_ku","w_fi","w_ku_pl","w_fi_pl","predicted_p_fi_wug","experiment_p_fi"]))

for nlx in nlexCss:
    for sw in startws:
        for pch in pChanges:
            for trnfile in trainingFiles:

                for i in range(1,101): #101
                    label = "_".join([str(nlx),str(sw),re.sub("\.","",str(pch)),re.sub("typeTokenInput_","",str(trnfile)),"_",str(i)])
                    print(label)
                    
                    autoconfig(trnfile,nLexCs=nlx,lexCStartW=sw,pChangeIndexation=pch,label=label)
                    g = l.Grammar("autoconfig.gl")
                    
                    g.learn(1000,300)
                    

                    #24_1_001_50_1
                    lik = g.logLikelihood()
                    sse = g.SSE()
                    wku = g.w[0]
                    wfi = g.w[1]
                    # now we need to grab the weights of the indexed Cs indexed to the pl morpheme
                    pl_lexeme = g.trainingData.lexicon['pl']
                    wku_pl = g.lexCs[0][pl_lexeme.lexCindexes[0]]
                    wfi_pl = g.lexCs[1][pl_lexeme.lexCindexes[1]]
                    
                    tot_wku = wku+wku_pl
                    tot_wfi = wfi+wfi_pl
                    
                    predP_fi_wug = pow(math.e, -1*tot_wku)/(pow(math.e, -1*tot_wfi)+pow(math.e,-1*tot_wku))
                    
                    # from Gaja's results
                    if trnfile =="typeTokenInput_4pt7":
                        experimentPfi = 0.03
                    elif trnfile == "typeTokenInput_12pt5":
                        experimentPfi = 0.11
                    elif trnfile == "typeTokenInput_25":
                        experimentPfi = 0.30
                    elif trnfile == "typeTokenInput_37pt5":
                        experimentPfi = 0.45
                    elif trnfile == "typeTokenInput_50":
                        experimentPfi = 0.50
                    elif trnfile == "typeTokenInput_exaggerated":
                        experimentPfi = 0.22
                    elif trnfile == "typeTokenInput_opposing":
                        experimentPfi = 0.41
                        
                    outputRow = [g.label,str(i),str(nlx),str(sw),str(pch),str(trnfile),str(lik),str(sse),str(wku),str(wfi),str(wku_pl),str(wfi_pl),str(predP_fi_wug),str(experimentPfi)]
                    with open(outfile,"a") as f:
                        f.write("\n")
                        f.write("\t".join(outputRow))
