import learner as l
import math
import re
from scipy.optimize import minimize
from numpy.random import rand

outfile = "powell_diffMorph_24_1_pt01.txt"

# settings in config.gl that are the same across runs
# learning rate: 0.01
# decay rate: 0 (may add another batch with some decay)
# locality: overlap
# first_index_strategy: lowest
# no PFCs or listing, no violations added by function

def autoconfig(trainingData,outfolder="/mnt/5F0E11952A224CAC/Gondolin/3_Projects_current/Type Frequency/GLaPL_output_Powell_diffMorph",label="default",weights=0,featureSet="hungarianFeatures",addViolations=False,constraints=None,generateCandidates=False,learningRate=0.01,decayRate=0,decayType="L2",threshold=1,noisy="no",useListedType="none",useListedRate=1,flip=False,simpleListing=False,pToList=0.5,nLexCs=0,pChangeIndexation=0.5,lexCStartW=10,locality="overlap",first_index_strategy="lowest",PFC_type="none",PFC_lrate=0.1,PFC_startW=10,logFile="GLaPL_log"):
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

def objective(params):
    #nlx = params[0]
    #nlx=int(round(nlx))
    
    nlx=24
    sw = params[0]
    pch = params[1]
    
    trainingFiles =["typeTokenInput_4pt7_diffMorph","typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph","typeTokenInput_50_diffMorph","typeTokenInput_37pt5_diffMorph","typeTokenInput_25_diffMorph","typeTokenInput_12pt5_diffMorph"]#,"typeTokenInput_12pt5","typeTokenInput_4pt7","typeTokenInput_opposing","typeTokenInput_exaggerated"]#["typeTokenInput_50","typeTokenInput_37pt5","typeTokenInput_25","typeTokenInput_12pt5","typeTokenInput_4pt7","typeTokenInput_opposing","typeTokenInput_exaggerated"]
    loglik = 0
    for trnfile in trainingFiles:
        for i in range(1,101): #101
            label = "_".join([str(nlx),str(sw),re.sub("\.","",str(pch)),re.sub("typeTokenInput_","",str(trnfile)),"_",str(i)])
            #print(label)
            
            autoconfig(trnfile,nLexCs=nlx,lexCStartW=sw,pChangeIndexation=pch,label=label)
            g = l.Grammar("autoconfig.gl")
            
            g.learn(1000,300)
            
            #24_1_001_50_1
            lik = g.logLikelihood()
            sse = g.SSE()
            wku = g.w[0]
            wfi = g.w[1]
            # now we need to grab the weights of the indexed Cs indexed to the pl morpheme
            #pl_lexeme = g.trainingData.lexicon['pl']
            #wku_pl = g.lexCs[0][pl_lexeme.lexCindexes[0]]
            #wfi_pl = g.lexCs[1][pl_lexeme.lexCindexes[1]]
            wku_pl = wku
            wfi_pl = wfi
            tot_wku = wku#+wku_pl
            tot_wfi = wfi#+wfi_pl
            
            predP_fi_wug = pow(math.e, -1*tot_wku)/(pow(math.e, -1*tot_wfi)+pow(math.e,-1*tot_wku))
            
            # from Gaja's results
            if trnfile =="typeTokenInput_4pt7_diffMorph":
                experimentPfi = 0.03
            elif trnfile == "typeTokenInput_12pt5_diffMorph":
                experimentPfi = 0.11
            elif trnfile == "typeTokenInput_25_diffMorph":
                experimentPfi = 0.30
            elif trnfile == "typeTokenInput_37pt5_diffMorph":
                experimentPfi = 0.45
            elif trnfile == "typeTokenInput_50_diffMorph":
                experimentPfi = 0.50
            elif trnfile == "typeTokenInput_exaggerated_diffMorph":
                experimentPfi = 0.22
            elif trnfile == "typeTokenInput_opposing_diffMorph":
                experimentPfi = 0.41
                
            loglik +=math.log(predP_fi_wug)*experimentPfi
            loglik +=math.log(1-predP_fi_wug)*(1-experimentPfi)
                
            outputRow = [g.label,str(i),str(nlx),str(sw),str(pch),str(trnfile),str(lik),str(sse),str(wku),str(wfi),str(wku_pl),str(wfi_pl),str(predP_fi_wug),str(experimentPfi)]
            with open(outfile,"a") as f:
                f.write("\n")
                f.write("\t".join(outputRow))
 
    print("Params:")
    print(params)
    print("Log Likelihood")
    print(-loglik)
    with open(outfile,"a") as f:
        f.write("\n")
        f.write("\t".join(["Params:","\t".join([str(p) for p in params]),"likelihood:",str(loglik)]))
    return(-loglik)
  
result = minimize(objective,[1,0.01],bounds=[(0,None),[0,1]],method="powell")  

with open(outfile,"a") as f:
    f.write("\n")
    f.write("Done")

