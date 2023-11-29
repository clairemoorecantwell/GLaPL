
label = "gramm_only"
# weights
cols = rainbow(100)
n=0
w = read.table(paste("weights_",label,"_",n,".txt",sep=""))
plot(w$V1,type='l',col=cols[1],ylim=c(0,11))
for (n in 1:99){
  w = read.table(paste("weights_",label,"_",n,".txt",sep=""))
  points(w$V1,type='l',col=cols[n+1])
}

runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,0.85),main=)
abline(v=0.35)
abline(v=0.59)
abline(v=0.75)


label = "gramm_only_short"

#--- conclusion, 100x100 iterations is enough.  sd of final weights is not smaller
label = "gramm_only"
label = "gramm_only_randomStart"
label = "listing"
label = "2_lexCs_induceFreely"
label = "48_lexCs_induceFreely"
label = "24_LexCs_induceFreely"
label = "48_lexCs_inducehalf"
label = "48_lexCs_induce25p"
label = "2_lexCs_induceFreely_10sw"
label = "2lexC_1_lowinput"
label = "2lexC_1_lowinput"  #<-- this one


label = "48_LexCs_induceFreely_highinput"
label = "2_LexCs_induce25_highinput"
label = "2_LexCs_induce25_highinput_r"
label = "2_LexCs_induceFreely_highinput"
label = "gramm_only_highinput"
label = "2lexC_1_highinput"  #<-- this one
label = "24lexC_1_highinput"


# same direction
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=20)
abline(v=0.93)
abline(v=0.78)
abline(v=0.75)
text(0.93,5,"token")
text(0.78,5,"participants")
text(0.75,5,"type")
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)

# contradictory
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=20)
abline(v=0.35)
abline(v=0.59)
abline(v=0.75)
text(0.35,5,"token")
text(0.59,5,"participants")
text(0.75,5,"type")
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)
abline(h=0.59)

label = "2lexC_1_50"

# 50%
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=20)
abline(v=0.5)
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)
abline(h=0.5)

label = "gramm_only_87"

# 87%
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=20)
abline(v=0.87)
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)
abline(h=0.87)

label = "2lexC_05_96"

# 96
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=20)
abline(v=0.96)
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)
abline(h=0.87)


label = "gramm_only_r_96"

# 96
runsumm = read.table(paste("runSummary_",label,".txt",sep=""),header=TRUE)
runsumm$pred_ku = exp(0)/(exp(0)+exp(-runsumm$ku))
hist(runsumm$pred_ku,xlim=c(0.15,1),breaks=10)
abline(v=0.96)
abline(v=mean(runsumm$pred_ku),col="blue")
hist(runsumm$logLikelihood)
plot(runsumm$logLikelihood,runsumm$pred_ku)
abline(h=0.96)


errRates = read.table("errRates_2_1_10_lowinput_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000))

errRates = read.table("errRates_2_1_10_lowinput_plastic_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,10000))

lexcws = read.table("lexCws_50_1_10_decayStatic_0.txt",header=TRUE)
plot(lexcws$ku48,type="l")

lexcws = read.table("lexCws_50_1_10_decayL1_0.txt",header=TRUE)
plot(lexcws$ku3,type="l")
errRates = read.table("errRates_50_1_10_decayL1_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000))

lexcws = read.table("lexCws_50_1_10_decayL2_0.txt",header=TRUE)
plot(lexcws$ku30,type="l")
errRates = read.table("errRates_50_1_10_decayL2_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000))


lexcws = read.table("lexCws_50_1_10_noDecay_0.txt",header=TRUE)
plot(lexcws$ku1,type="l")
errRates = read.table("errRates_50_1_10_noDecay_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000))


lexcws = read.table("lexCws_2_pt01_2_noDecay_lowinput_3.txt",header=TRUE)
plot(lexcws$ku1,type="l",col="blue",ylim=c(0,5))
points(lexcws$ku2,type="l",col="lightblue")
points(lexcws$fi1,type="l",col="black")
points(lexcws$fi2,type="l",col="grey")

errRates = read.table("errRates_2_pt01_10_noDecay_lowinput_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000))


errRates = read.table("errRates_3_pt01_2_noDecay_long_50_0.txt",header=TRUE)
plot(row.names(errRates),errRates$errorRate,type="l",xlim=c(0,1000),col="grey")


lexcws = read.table("lexCws_3_pt1_2_noDecay_long_50_0.txt",header=TRUE)

plot(lexcws$ku1,type="l",col="blue",ylim=c(0,8))
points(lexcws$fi1,type="l",col="lightblue")
points(lexcws$ku2,type="l",col="black",ylim=c(0,8))
points(lexcws$fi2,type="l",col="grey")
points(lexcws$ku3,type="l",col="lightgreen",ylim=c(0,8))
points(lexcws$fi3,type="l",col="green")
for (n in 0:99){
lexcws = read.table(paste("lexCws_3_pt1_2_noDecay_long_87_",n,".txt",sep=""),header=TRUE)

l = read.table(paste("lexCs_","3_pt1_2_noDecay_long_87_",n,".txt",sep=""),sep="\t",fill=TRUE)
kufi = "no"
for(i in 1:nrow(l)) {       # for-loop over rows
    if (l[i,1]=="ku"){
      kufi = "ku"
    } else if (l[i,1]=="fi"){
      kufi = "fi"
    }
    if ("pl" %in% l[i, ]){
      if (kufi=="ku"){
        plku = c(plku,as.numeric(l[i,1]))
        kuZero = FALSE
      } else if (kufi=="fi"){
        plfi = c(plfi,as.numeric(l[i,1]))
        fiZero = FALSE
      }
    }
  }
  if (kuZero){
    plku = c(plku,0)
  }
  if (fiZero){
    plfi = c(plfi,0)
  }
}

points(lexcws$ku1,type="l",col="blue",ylim=c(0,8))
points(lexcws$fi1,type="l",col="lightblue")
points(lexcws$ku2,type="l",col="black",ylim=c(0,8))
points(lexcws$fi2,type="l",col="grey")
points(lexcws$ku3,type="l",col="lightgreen",ylim=c(0,8))
points(lexcws$fi3,type="l",col="green")
}

indexes = read.table("indexes_3_pt01_2_noDecay_long_highinput_3.txt",header=TRUE)
plot(indexes$pl_ku_w,type="l")
points(indexes$pl_fi_w,type="l",col="blue")
plot(indexes$tikle_ku_w,type="l")
