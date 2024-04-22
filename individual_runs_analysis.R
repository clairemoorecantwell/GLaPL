setwd("/mnt/5F0E11952A224CAC/Gondolin/3_Projects_current/RepStrTheory/Type Frequency/GLaPL_output_diffMorph/")
# pJump
# (pChange ^ startW)^wDiff / pchange
par(family="Times New Roman")

par(cex.axis=0.8,mar=c(3,3,1,1),mfrow=c(1,2))
pchange = 0.1
startW = 1
wdiff = seq(0,100,by=0.01)
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)
plot(wdiff,y,type="l",axes=FALSE,xlab="weight difference",ylab="p(switch indexes)")
axis(1,at=c(1,2,5,10,50,100))
axis(2)
mtext("2",cex=0.8,side=1,at=2,line=0.4)

startW = 2
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=grey(0.3))
startW = 5
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=grey(0.6))
startW = 10
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=grey(0.8))

points(c(-10,10),c(1,1),type="l",lty=2)
points(c(1,1),c(1,-10),type="l",lty=2)
points(c(-10,2),c(1,1),type="l",col=grey(0.3),lty=2)
points(c(2,2),c(1,-10),type="l",col=grey(0.3),lty=2)
points(c(-10,5),c(1,1),type="l",col=grey(0.6),lty=2)
points(c(5,5),c(1,-10),type="l",col=grey(0.6),lty=2)
points(c(-10,10),c(1,1),type="l",col=grey(0.8),lty=2)
points(c(10,10),c(1,-10),type="l",col=grey(0.8),lty=2)


pchange = 0.75
greencol = hcl.colors(6,"Greens 3")
startW = 1
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)
plot(wdiff,y,type="l",col=greencol[2],axes=FALSE,xlab="weight difference",ylab="p(switch indexes)")
axis(1,at=c(1,2,5,10,50,100))
axis(2)
mtext("2",cex=0.8,side=1,at=2,line=0.4)
startW = 2
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=greencol[3])
startW = 5
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=greencol[4])
startW = 10
y = ((pchange^(1/startW))^wdiff)/pchange
y = ifelse(y>1,1,y)

points(wdiff,y,type="l",col=greencol[5])

points(c(-10,10),c(1,1),type="l",lty=2,col=greencol[1])
points(c(1,1),c(1,-10),type="l",lty=2,col=greencol[1])
points(c(-10,2),c(1,1),type="l",col=greencol[2],lty=2)
points(c(2,2),c(1,-10),type="l",col=greencol[2],lty=2)
points(c(-10,5),c(1,1),type="l",col=greencol[3],lty=2)
points(c(5,5),c(1,-10),type="l",col=greencol[3],lty=2)
points(c(-10,10),c(1,1),type="l",col=greencol[4],lty=2)
points(c(10,10),c(1,-10),type="l",col=greencol[4],lty=2)




# There are 24 total words in the exp
exceptions_50 = c("lugat","fudki","freglu","tikle","gazal","flebon","dosid","zakta","gragol","krakle","tazku","brugan")
exceptions_37pt5 = c("lugat","fudki","freglu","tikle","gazal","flebon","dosid","zakta","gragol")
exceptions_25 = c("lugat","fudki","freglu","tikle","gazal","flebon")
exceptions_12pt5 = c("freglu","dosid","zakta")
exceptions_4pt7 = c("fudki")
exceptions_exaggerated = c("brugan","vidfo","same","truvit","kisal","tutun")
exceptions_opposing = c("lugat","fudki","dosid","krakle","marel","drokra")

runAnalysis <- data.frame(file=character(),
                  nLexCs = integer(),
                  startW = numeric(),
                  pChange = numeric(),
                  inputSet = character(),
                  runNo = integer(),
                  ex_spr=integer(),
                  r_spr=integer(),
                  un_e=integer(),
                  un_r=integer(),
                  nku=integer(),
                  nfi=integer(),

                  stringsAsFactors=FALSE)
# data frame
#runInfo                
#/ 2_1_005_opposing___1_0  
#exceptions_spread   
#/ 1  (means all exceptions are on 1 constraint)
#regulars_spread
#/ 2 (regulars are spread over 2 constraints)
# unindexed_exceptions
#/ 0 (number of exceptions that are not indexed)
# unindexed_regulars
#/ 0 (number of non-indexed regulars)
# n_ku
# 2 (number of copies of 'ku', even if they have nothing indexed)
# n_fi
#
# 
start = TRUE
for (nLexCs in c(2,24)){
  for (startW in c(1,2,5,10)){
    for (pChange in c(0.01,0.05,0.25,0.5,0.75,0.99)){
      for (inpt in c("50_diffMorph","25_diffMorph","37pt5_diffMorph","4pt7_diffMorph","12pt5_diffMorph","exaggerated_diffMorph","opposing_diffMorph")){
        for (runNo in seq(1,100)){
        if (inpt == "50_diffMorph"){
          exceptions = exceptions_50
        }else if (inpt =="25_diffMorph"){
          exceptions = exceptions_25
        }else if (inpt =="37pt5_diffMorph"){
          exceptions = exceptions_37pt5
        }else if (inpt == "4pt7_diffMorph"){
          exceptions = exceptions_4pt7
        }else if (inpt == "12pt5_diffMorph"){
          exceptions = exceptions_12pt5
        }else if (inpt == "exaggerated_diffMorph"){
          exceptions = exceptions_exaggerated
        }else if (inpt == "opposing_diffMorph"){
          exceptions = exceptions_opposing
        }
filename = paste("lexCs_",
                 as.character(nLexCs),
                 "_",as.character(startW),
                 "_",gsub("\\.","",as.character(pChange)),
                 "_",inpt,"___",
                 as.character(runNo),
                 "_0.txt",sep="")
print(table(runAnalysis$nLexCs,runAnalysis$startW,runAnalysis$pChange,runAnalysis$inputSet))
#filename = "lexCs_2_1_005_opposing___1_0.txt"
f = file(filename,open="r")
l = readLines(f)
ku = FALSE
fi = FALSE
nku = 0
nfi = 0
e_spr = 0
r_spr = 0
n_e = 0
n_r = 0
for (line in l){
  row = strsplit(line,'\t')[[1]]
  #print(row)
  #print(row[1])
  if (length(row)>0){
  if (row[1] == "ku"){
    ku = TRUE
    fi = FALSE
  } else if (row[1] == "fi"){
    ku = FALSE
    fi = TRUE
  } else{
    # increment number of ku/fi constraints
    if (ku){
      nku = nku+1
    } else if (fi){
      nfi = nfi+1
    }
    # to measure spread
    anyExceptions = FALSE
    anyRegulars = FALSE
    i =0
    for (wd in row){
      i=i+1
      #print(i)
      #print(wd)
      if (wd %in% exceptions){
        anyExceptions = TRUE
        #print("exception")
        n_e = n_e+1
      } else if(i>1){
        anyRegulars = TRUE
        #print("regular")
        n_r = n_r+1
      }
      
    }
    if (anyRegulars){
      r_spr = r_spr+1
    }
    if (anyExceptions){
      e_spr = e_spr+1
    }

  }
  }
}
un_e = length(exceptions) - n_e
un_r = (24-length(exceptions)) - n_r

thisRow = c(filename,nLexCs,startW,pChange,inpt,runNo,e_spr,r_spr,un_e,un_r,nku,nfi)
if (start){
  runAnalysis[1,]=thisRow
  start = FALSE
  print(runAnalysis)
  #read.table("s")
}else{
runAnalysis = rbind(runAnalysis,setNames(thisRow,names(runAnalysis)))
}
close(f)
        }}}}}

runAnalysis$ex_spr = as.numeric(runAnalysis$ex_spr)
runAnalysis$r_spr = as.numeric(runAnalysis$r_spr)

hist(runAnalysis$ex_spr[runAnalysis$nLexCs=="2"])
hist(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"&runAnalysis$pChange=="0.01"])
hist(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"&runAnalysis$pChange=="0.99"])

hist(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"])
# need to make a table
#median spread? or %1
tapply(runAnalysis$ex_spr,list(runAnalysis$inputSet,runAnalysis$nLexCs,runAnalysis$startW,runAnalysis$pChange),FUN="median")

tapply(runAnalysis$ex_spr,list(runAnalysis$inputSet),FUN="mean")

t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"],runAnalysis$inputSet[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"],runAnalysis$pChange[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="24"],runAnalysis$startW[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="2"],runAnalysis$inputSet[runAnalysis$nLexCs=="2"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="2"],runAnalysis$pChange[runAnalysis$nLexCs=="2"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="2"],runAnalysis$startW[runAnalysis$nLexCs=="2"])

t =table(runAnalysis$r_spr[runAnalysis$nLexCs=="24"],runAnalysis$inputSet[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$r_spr[runAnalysis$nLexCs=="24"],runAnalysis$pChange[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$r_spr[runAnalysis$nLexCs=="24"],runAnalysis$startW[runAnalysis$nLexCs=="24"])
t =table(runAnalysis$r_spr[runAnalysis$nLexCs=="2"],runAnalysis$inputSet[runAnalysis$nLexCs=="2"])
t =table(runAnalysis$r_spr[runAnalysis$nLexCs=="2"],runAnalysis$pChange[runAnalysis$nLexCs=="2"])
t =table(runAnalysis$ex_spr[runAnalysis$nLexCs=="2"],runAnalysis$startW[runAnalysis$nLexCs=="2"])

pers = t[1,]/colSums(t)
pers

sdfga



sagf


nLexCs = 2
pChange = 0.01
startW = 1
runNo = 40
inpt = "37pt5_diffMorph"
filenameBase = paste(
                 as.character(nLexCs),
                 "_",as.character(startW),
                 "_",gsub("\\.","",as.character(pChange)),
                 "_",inpt,"___",
                 as.character(runNo),
                 "_0.txt",sep="")
w = read.table(paste("weights_",filenameBase,sep=""))
ind = read.table(paste("indexes_",filenameBase,sep=""),header=TRUE)
err = read.table(paste("errRates_",filenameBase,sep=""),header=TRUE)

par(family="Times New Roman")
trueW_ku = w$V1#+ind$pl_ku_w[2:501]
plot(seq(1,300),trueW_ku,type="l",ylim=c(0,10),xlim=c(1,500),axes=FALSE
     ,ylab="weight",xlab="learning epoch")
#text(50,7,"be -ku")
trueW_fi = w$V2#+ind$pl_fi_w[2:501]
points(seq(1,300),trueW_fi,col="grey",type="l")
#text(41,6.5,"be -fi",col="grey")
p_fi = exp(-trueW_ku[300])/(exp(-trueW_fi[300])+exp(-trueW_ku[300]))
text(480,trueW_ku[300]-.5,"p(-fi)")
text(480,trueW_ku[300]-1,round(p_fi,2))
legend(10,8,c("Bᴇ ᴋᴜ","Bᴇ ꜰɪ",""),col=c("black","grey"),lwd=1,bty="n")
exceptions_37pt5 = c("lugat","fudki","freglu","tikle","gazal","flebon","dosid","zakta","gragol")

#plot(seq(1,501),ind$lugat_fi_w,type="l",col="red",xlim=c(0,500))
points(seq(1,301),ind$fudki_fi_w,type="l",col="red")  #zakta, 37pt5, 2,.01,1,run#1
points(seq(1,301),ind$dosid_fi_w,type="l",col="red")
points(seq(1,501),ind$krakle_fi_w,type="l",col="red")  #zakta, 37pt5, 2,.01,1,run#1
points(seq(1,501),ind$marel_fi_w,type="l",col="red")
points(seq(1,501),ind$drokra_fi_w,type="l",col="red")  #zakta, 37pt5, 2,.01,1,run#1

for (row in seq(2,301)){
  if (ind$fudki_fi_i[row]!=ind$fudki_fi_i[row-1]){
    points(row,ind$fudki_fi_w[row],col="red",pch=20,cex=0.7)
  }
}
exceptions_25 = c("lugat","fudki","freglu","tikle","gazal","flebon")
exceptions_opposing = c("lugat","fudki","dosid","krakle","marel","drokra")


points(seq(1,501),ind$drokra_ku_w,type="l",col="blue")
for (row in seq(2,501)){
  if (ind$drokra_ku_i[row]!=ind$drokra_ku_i[row-1]){
    points(row,ind$drokra_ku_w[row],col="blue",pch=20,cex=0.7)
  }
}
points(err$errorRate*10,col="green",pch=20,cex=0.2)
axis(1)
axis(2)
