label = "gramm_only"
label = "uselisted"
label = "2_1_10"
label = "2_pt5_10"
label = "2_pt1_2"
label = "2_pt1_10_noDecay"
label = "2_pt01_10_noDecay"
label = "2_pt01_2_noDecay"
label = "1_pt01_2_noDecay"

label = "3_pt01_2_noDecay_long"
label = "3_pt05_2_noDecay_long"
label = "3_pt1_2_noDecay_long"



par(mfrow=c(1,5),mar=c(2,1,1,1))
runsumm = read.table(paste("runSummary_",label,"_50.txt",sep=""),header=TRUE)
plku = c()
plfi = c()
for (n in 0:99){
  l = read.table(paste("lexCs_",label,"_50_",n,".txt",sep=""),sep="\t",fill=TRUE)
  kufi = "no"
  kuZero = TRUE
  fiZero = TRUE
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
runsumm = cbind(runsumm,plku,plfi)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
runsumm$pred_ku = exp(-(runsumm$fi+runsumm$plfi))/(exp(-(runsumm$fi+runsumm$plfi))+exp(-(runsumm$ku+runsumm$plku)))

hist(runsumm$pred_ku,xlim=c(0,1),breaks=20,ylim=c(0,40),main="")
abline(v=0.5)
abline(v=mean(runsumm$pred_ku),col="blue")

# who are the exceptions?  (fi guys)
figuys = c("lugat","fudki","freglu","tikle","gazal","flebon","dosid","zakta","gragol","krakle","tazku","brugan")
kuguys = c("marel","drokra","pisfu","glakod","mafdi","blezan","trapla","vidfo","same","truvit","kisal","tutun")

#plot(runsumm$errorRate,runsumm$logLikelihood)




runsumm = read.table(paste("runSummary_",label,"_87.txt",sep=""),header=TRUE)
plku = c()
plfi = c()
for (n in 0:99){
  l = read.table(paste("lexCs_",label,"_87_",n,".txt",sep=""),sep="\t",fill=TRUE)
  kufi = "no"
  kuZero = TRUE
  fiZero = TRUE
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
runsumm = cbind(runsumm,plku,plfi)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
runsumm$pred_ku = exp(-(runsumm$fi+runsumm$plfi))/(exp(-(runsumm$fi+runsumm$plfi))+exp(-(runsumm$ku+runsumm$plku)))

hist(runsumm$pred_ku,xlim=c(0,1),breaks=20,ylim=c(0,40),main="")
abline(v=0.87)
abline(v=mean(runsumm$pred_ku),col="blue")

# who are the exceptions?  (fi guys)
figuys = c("freglu","dosid","zakta")
kuguys = c("lugat","fudki","tikle","gazal","flebon","gragol","krakle","tazku","brugan","marel","drokra","pisfu","glakod","mafdi","blezan","trapla","vidfo","same","truvit","kisal","tutun")



runsumm = read.table(paste("runSummary_",label,"_96.txt",sep=""),header=TRUE)
plku = c()
plfi = c()
for (n in 0:99){
  l = read.table(paste("lexCs_",label,"_96_",n,".txt",sep=""),sep="\t",fill=TRUE)
  kufi = "no"
  kuZero = TRUE
  fiZero = TRUE
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
runsumm = cbind(runsumm,plku,plfi)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
runsumm$pred_ku = exp(-(runsumm$fi+runsumm$plfi))/(exp(-(runsumm$fi+runsumm$plfi))+exp(-(runsumm$ku+runsumm$plku)))

hist(runsumm$pred_ku,xlim=c(0,1),breaks=20,ylim=c(0,40),main="")
abline(v=0.96)
abline(v=mean(runsumm$pred_ku),col="blue")

figuys = c("fudki")
kuguys = c("lugat","freglu","dosid","zakta","tikle","gazal","flebon","gragol","krakle","tazku","brugan","marel","drokra","pisfu","glakod","mafdi","blezan","trapla","vidfo","same","truvit","kisal","tutun")





runsumm = read.table(paste("runSummary_",label,"_highinput.txt",sep=""),header=TRUE)
plku = c()
plfi = c()
for (n in 0:99){
  l = read.table(paste("lexCs_",label,"_highinput_",n,".txt",sep=""),sep="\t",fill=TRUE)
  kufi = "no"
  kuZero = TRUE
  fiZero = TRUE
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
runsumm = cbind(runsumm,plku,plfi)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
runsumm$pred_ku = exp(-(runsumm$fi+runsumm$plfi))/(exp(-(runsumm$fi+runsumm$plfi))+exp(-(runsumm$ku+runsumm$plku)))

hist(runsumm$pred_ku,xlim=c(0,1),breaks=20,ylim=c(0,40),main="")
abline(v=0.93)
abline(v=0.78)
abline(v=0.75)
text(0.93,5,"token")
text(0.78,5,"participants")
text(0.75,5,"type")
abline(v=mean(runsumm$pred_ku),col="blue")

points(c(0.78,0.78),c(0,38),type="l",lty=1)
legend(0.78,28,"participants",bg="white",box.col="white",xjust=0.6)

points(c(0.93,0.93),c(0,38),type="l",lty=2)
legend(0.93,30,"token",bg="white",box.col="white",xjust=0.3)

points(c(0.75,0.75),c(0,38),type="l",lty=3)
legend(0.75,32,"type",bg="white",box.col="white",xjust=0.65)

m=mean(runsumm$pred_ku)
points(c(m,m),c(0,24),col="blue",type="l",lwd=2)
points(m,24,col="blue",pch=20)
legend(m,21,"mean model pred.",bg="white",box.col="white",xjust=0.31,text.col="blue")





runsumm = read.table(paste("runSummary_",label,"_lowinput.txt",sep=""),header=TRUE)
plku = c()
plfi = c()
for (n in 0:99){
  l = read.table(paste("lexCs_",label,"_lowinput_",n,".txt",sep=""),sep="\t",fill=TRUE)
  kufi = "no"
  kuZero = TRUE
  fiZero = TRUE
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
runsumm = cbind(runsumm,plku,plfi)
runsumm$pred_ku = exp(-runsumm$fi)/(exp(-runsumm$fi)+exp(-runsumm$ku))
runsumm$pred_ku = exp(-(runsumm$fi+runsumm$plfi))/(exp(-(runsumm$fi+runsumm$plfi))+exp(-(runsumm$ku+runsumm$plku)))
hist(runsumm$pred_ku,xlim=c(0,1),breaks=20,ylim=c(0,40),main="")
points(c(0.59,0.59),c(0,38),type="l",lty=1)
#legend(0.59,28,"participants",bg="white",box.col="white",xjust=0.6)

points(c(0.35,0.35),c(0,38),type="l",lty=2)
#legend(0.27,30,"token",bg="white",box.col="white",xjust=0.3)

points(c(0.75,0.75),c(0,38),type="l",lty=3)
#legend(0.75,32,"type",bg="white",box.col="white",xjust=0.65)

m=mean(runsumm$pred_ku)
points(c(m,m),c(0,24),col="blue",type="l",lwd=2)
points(m,24,col="blue",pch=20)
#legend(m,21,"mean model pred.",bg="white",box.col="white",xjust=0.31,text.col="blue")

