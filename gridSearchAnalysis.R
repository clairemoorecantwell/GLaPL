#library(plotrix)
runs = read.table("gridSearch_clean_diffMorph.txt",sep="\t",header=TRUE,comment.char = "#")
table(runs$inputSet,runs$lexCstartW,runs$pChangeIndexation,runs$nlexCs)
summary(runs)
par(family="Times New Roman")


#runs[runs$inputSet=="typeTokenInput_37pt5"&runs$lexCstartW==10&runs$pChangeIndexation==0.01&runs$nlexCs==2,]


hist(runs$likelihood[runs$likelihood>-0.02],breaks=1000)
hist(runs$likelihood[runs$likelihood>-0.002],breaks=1000)

hist(runs$SSE)
hist(runs$SSE[runs$SSE<0.0000005],breaks=1000)
hist(runs$SSE[runs$SSE<0.00000001],breaks=1000)

# let's look at median likelihoods then, and see what configuration is best
# then we can do SSE - also medians

# want: four lines, x axis is pChangeIndexation, lines are start W, two graphs for 2 and 24 indexations
# y axis is median likelihood, OR SSE

l= as.data.frame(as.table(tapply(runs$likelihood,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="median")))
sse = as.data.frame(as.table(tapply(runs$SSE,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="median")))
l$Var2 = as.numeric(as.character(l$Var2))
###### SKIP TO GRAPH

# calculate match to the experiment:
#sums
runs$exp_likelihood = log(runs$predicted_p_fi_wug)*runs$experiment_p_fi
runs$exp_likelihood_inverse = log(1-runs$predicted_p_fi_wug)*(1-runs$experiment_p_fi)
runs$exp_sse = (runs$predicted_p_fi_wug-runs$experiment_p_fi)^2
runs$exp_sse_inverse = ((1-runs$predicted_p_fi_wug)-(1-runs$experiment_p_fi))^2

l = as.data.frame(as.table(tapply(runs$exp_likelihood,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="sum")))
l_inv = as.data.frame(as.table(tapply(runs$exp_likelihood_inverse,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="sum")))
l$Freq = l$Freq+l_inv$Freq
l$Var4 = "all"
l_byDataset = as.data.frame(as.table(tapply(runs$exp_likelihood,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="sum")))
l_byDataset_inv = as.data.frame(as.table(tapply(runs$exp_likelihood_inverse,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="sum")))
l_byDataset$Freq = l_byDataset$Freq+l_byDataset_inv$Freq
l_mismatch =as.data.frame(as.table(tapply(runs$exp_likelihood[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
l_mismatch_inv =as.data.frame(as.table(tapply(runs$exp_likelihood_inverse[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
l_mismatch$Freq = l_mismatch$Freq+l_mismatch_inv$Freq

l_mismatch$Var4 = "all"

l_match =as.data.frame(as.table(tapply(runs$exp_likelihood[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
l_match_inv =as.data.frame(as.table(tapply(runs$exp_likelihood_inverse[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
l_match$Freq = l_match$Freq+l_match_inv$Freq

l_match$Var4 = "all"

sse = as.data.frame(as.table(tapply(runs$exp_sse,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="sum")))
sse_inv =as.data.frame(as.table(tapply(runs$exp_sse_inverse,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW),FUN="sum")))
sse$Freq = sse$Freq+sse_inv$Freq
sse$Var4 = "all"

#match only
sse_match =as.data.frame(as.table(tapply(runs$exp_sse[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
sse_match_inv =as.data.frame(as.table(tapply(runs$exp_sse_inverse[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[!runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
sse_match$Freq = sse_match$Freq+sse_match_inv$Freq

sse_match$Var4 = "all"


#mismatch only
sse_mismatch =as.data.frame(as.table(tapply(runs$exp_sse[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
sse_mismatch_inv =as.data.frame(as.table(tapply(runs$exp_sse_inverse[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],list(runs$nlexCs[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$pChangeIndexation[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")],runs$lexCstartW[runs$inputSet %in% c("typeTokenInput_opposing_diffMorph","typeTokenInput_exaggerated_diffMorph")]),FUN="sum")))
sse_mismatch$Freq = sse_mismatch$Freq+sse_mismatch_inv$Freq

sse_mismatch$Var4 = "all"


l=sse
# ok, now graph the sum things
l=l_mismatch
l$Var2 = as.numeric(as.character(l$Var2))


##################
#### GRAPH BEGINS HERE
#### !! check that the comments are correct !!
##################
inpt = c("all")#typeTokenInput_50_diffMorph","typeTokenInput_37pt5_diffMorph","typeTokenInput_25_diffMorph","typeTokenInput_12pt5_diffMorph","typeTokenInput_4pt7_diffMorph")
cols2 = hcl.colors(5,palette="Dark Mint")
cols24 = hcl.colors(5,palette="Oranges")
nLexCs = 2
startW = 1
plot(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
     #,ylim=c(-0.2,0),axes=FALSE
     #,ylab="Log Likelihood of training data"
     ,ylim = c(-800,-300),axes=FALSE
     ,ylab="Log Likelihood of experimental results"
     #,ylim = c(0,150),axes=FALSE
     #,ylab="SSE (experiment)"
     ,xlab=expression("p"["change"])
     ,col=cols2[4],lwd=1,cex=0.6)
axis(1,at=c(0.01,0.05,0.1,0.25,0.5,0.75,0.99)
     ,cex.axis=0.6)
mtext("0.05",side=1,line=1.7,at=0.05,cex=0.6)
axis(2,cex.axis=0.6)
startW = 2.5
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols2[3],lwd=1,cex=0.6)
startW = 5
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols2[2],lwd=1,cex=0.6)
startW = 10
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols2[1],lwd=1,cex=0.6)

nLexCs = 24
startW = 1
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols24[4],lwd=1,cex=0.6)
startW = 2
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols24[3],lwd=1,cex=0.6)
startW = 5
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols24[2],lwd=1,cex=0.6)
startW = 10
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt]),l$Freq[l$Var3==startW&l$Var1==nLexCs&l$Var4 %in% inpt],type="b",pch=20
       ,col=cols24[1],lwd=1,cex=0.6)
#points(c(0.8,0.8,0.8,0.8,0.85,0.85,0.85,0.85),c(-0.19,-0.18,-0.17,-0.16,-0.19,-0.18,-0.17,-0.16)
#       ,col=c(cols2[1],cols2[2],cols2[3],cols2[4],cols24[1],cols24[2],cols24[3],cols24[4])
#       ,pch=20,cex=0.6)
#text(c(0.9,0.9,0.9,0.9,0.935),c(-0.19,-0.18,-0.17,-0.16,-0.145),c("10","5","2","1","start w")
#     ,col=c(grey(0.1),grey(0.3),grey(0.45),grey(0.6)),cex=0.7)
#text(c(0.71,0.8,0.85),c(-0.145,-0.145,-0.145),c("nLexCs","2","24"),col=c("black",cols2[1],cols24[1]),cex=0.7)

points(c(0.45,0.45,0.45,0.45,0.5,0.5,0.5,0.5),c(-540,-530,-520,-510,-540,-530,-520,-510)
       ,col=c(cols2[1],cols2[2],cols2[3],cols2[4],cols24[1],cols24[2],cols24[3],cols24[4])
       ,pch=20,cex=0.6)
text(c(0.55,0.55,0.55,0.55,0.58),c(-540,-530,-520,-510,-500),c("10","5","2","1","start w")
     ,col=c(grey(0.1),grey(0.3),grey(0.45),grey(0.6)),cex=0.7)
text(c(0.37,0.45,0.5),c(-500,-500,-500),c("nLexCs","2","24"),col=c("black",cols2[1],cols24[1]),cex=0.7)


points(c(0.45,0.45,0.45,0.45,0.5,0.5,0.5,0.5),c(-540,-530,-520,-510,-540,-530,-520,-510)
       ,col=c(cols2[1],cols2[2],cols2[3],cols2[4],cols24[1],cols24[2],cols24[3],cols24[4])
       ,pch=20,cex=0.6)
text(c(0.55,0.55,0.55,0.55,0.58),c(-540,-530,-520,-510,-500),c("10","5","2","1","start w")
     ,col=c(grey(0.1),grey(0.3),grey(0.45),grey(0.6)),cex=0.7)
text(c(0.37,0.45,0.5),c(-500,-500,-500),c("nLexCs","2","24"),col=c("black",cols2[1],cols24[1]),cex=0.7)

l[l$Freq==min(l$Freq),]

#############
## GRAPH ONE SET OF PARAMETERS
#############

barscol=cols2[5]
bordercol = cols2[4]#"white"#hcl.colors(10,palette="SunsetDark")[8]
modelcol = cols2[1]
typecol=cols24[1]
tokencol=cols24[2]
expcol=cols24[3]
#par(mar=c(3.2,1.8,1,),xpd=TRUE)

cairo_pdf(filename="expMatchHistograms.pdf",
      family="Times New Roman",
      width=10, 
      height=8, 
      pointsize=12)

n=2
pch=0.1
sw=1
inpt = "typeTokenInput_50_diffMorph"
par(mfrow=c(2,4),mar=c(0.5,0.8,0.8,1),oma=c(3,3,1,1),xpd=TRUE)
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
m = mean(plotdata)
hist(plotdata
     ,xlim=c(0,.7)
     ,main="50%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
axis(2)
mtext("Frequency",side=2,line=2.5,cex=0.9)
points(c(0.5,0.5),c(0,60),type='l',col=typecol)
text(0.45,60,"type 0.5",pos=4,cex=0.8,col=typecol)
text(0.45,57,"token 0.5",pos=4,cex=0.8,col=tokencol)
text(0.45,54,"exp. 0.5",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
#legend(model_est+0.09,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)

#mtext("p(fi)",1,line=2,cex=0.8)
#par(xpd=FALSE)

inpt = "typeTokenInput_37pt5_diffMorph"
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,0.7)
     ,main="37.5%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=10
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.375,0.375),c(0,60),type='l',lty=2,col=typecol)
text(0.32,60,"type 0.375",pos=4,cex=0.8,col=typecol)
text(0.32,57,"token 0.375",pos=4,cex=0.8,col=tokencol)
points(c(0.45,0.45),c(0,55),type='l',col=expcol)
text(0.4,54,"exp. 0.45",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.06,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
#legend(model_est+0.06,39,legend="                                       ",cex=0.35,bg="white",box.col="white")
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)


inpt = "typeTokenInput_25_diffMorph"
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,.7)
     ,main="25%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.25,0.25),c(0,60),type='l',lty=2,col=typecol)
text(0.2,60,"type 0.25",pos=4,cex=0.8,col=typecol)
text(0.2,57,"token 0.25",pos=4,cex=0.8,col=tokencol)
points(c(0.3,0.3),c(0,55),type='l',col=expcol)
text(0.25,54,"exp. 0.3",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.05,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
#legend(model_est+0.05,39,legend="                                       ",cex=0.35,bg="white",box.col="white")
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)


inpt = "typeTokenInput_12pt5_diffMorph"
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,0.7)
     ,main="12.5%"
     ,xlab="predicted p(fi)"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.125,0.125),c(0,60),type='l',lty=2,col=typecol)
text(0.1,60,"type 0.125",pos=4,cex=0.8,col=typecol)
text(0.1,57,"token 0.125",pos=4,cex=0.8,col=tokencol)
points(c(0.11,0.11),c(0,55),type='l',col=expcol)
legend(0.15,55,legend="        ",cex=0.35,bg="white",box.col="white")

text(0.08,54,"exp. 0.11",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.09,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)


mtext("p(fi)",1,line=2.3,cex=0.8)

inpt = "typeTokenInput_4pt7_diffMorph"
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,0.7)
     ,main="4.7%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.047,0.047),c(0,60),type='l',lty=2,lwd=2,col=typecol)
text(0.01,60,"type 0.047",pos=4,cex=0.8,col=typecol)
legend(0.1,58,legend="        ",cex=0.35,bg="white",box.col="white")

text(0.01,57,"token 0.047",pos=4,cex=0.8,col=tokencol)
legend(0.1,55,legend="        ",cex=0.35,bg="white",box.col="white")

points(c(0.03,0.03),c(0,55),type='l',col=expcol)
text(0.01,54,"exp. 0.03",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.09,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)


inpt = "typeTokenInput_exaggerated_diffMorph"
plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,0.7)
     ,main="25%/ 7%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.25,0.25),c(0,60),type='l',lty=2,col=typecol)
text(0.2,60,"type 0.25",pos=4,cex=0.8,col=typecol)
points(c(0.07,0.07),c(0,60),type='l',lty=3,col=tokencol)
legend(0.08,58,legend="                                   ",cex=0.35,bg="white",box.col="white")
text(0.02,57,"token 0.07",pos=4,cex=0.8,col=tokencol)
points(c(0.22,0.22),c(0,55),type='l',col=expcol)
text(0.2,54,"exp. 0.22",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)

points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.06,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),col=modelcol,cex=0.8)
#legend(model_est+0.06,39,legend="                                       ",cex=0.35,bg="white",box.col="white")
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)



inpt = "typeTokenInput_opposing_diffMorph"

plotdata = runs$predicted_p_fi_wug[runs$nlexCs==n&runs$pChangeIndexation==pch&runs$inputSet==inpt&runs$lexCstartW==sw]
hist(plotdata
     ,xlim=c(0,0.7)
     ,main="25%/ 65%"
     ,axes=FALSE
     ,ylim=c(0,65)
     ,breaks=5
     ,col=barscol,border=bordercol
)
axis(1)
points(c(0.25,0.25),c(0,60),type='l',lty=2,cex=0.8,col=typecol)
text(0.2,60,"type 0.25",pos=4,cex=0.8,col=typecol)
points(c(0.65,0.65),c(0,60),type='l',lty=3,cex=0.8,col=tokencol)
text(0.6,57,"token 0.65",pos=4,cex=0.8,col=tokencol)
points(c(0.41,0.41),c(0,55),type='l',cex=0.8,col=expcol)
legend(0.26,55,legend="                          ",cex=0.35,bg="white",box.col="white")
text(0.35,54,"exp. 0.41",pos=4,cex=0.8,col=expcol)

model_est = mean(plotdata,na.rm=TRUE)
model_est = median(plotdata,na.rm=TRUE)
points(c(model_est,model_est),c(0,40),type='l',lwd=2,col=modelcol)
points(c(model_est),c(40),pch=20,cex=1.3,col=modelcol)
legend(model_est+0.09,41,legend="        ",cex=0.35,bg="white",box.col="white")
text(model_est+0.15,40,round(model_est,2),cex=0.8,col=modelcol)
#legend(model_est+0.06,39,legend="                                       ",cex=0.35,bg="white",box.col="white")
#text(model_est+0.38,38,"model prediction",col=modelcol,cex=0.7)
################# STOP
dev.off()


######################################
####### SCRAPS BELOW

# first, thin cells with too many runs in them:
#thinnedRuns = runs[runs$inputSet=="na",]
#for (p in c(0.01,0.05,0.1,0.25,0.5,0.75,0.99)){
#  for (w in c(1,2,5,10)){
#    for (n in c(2,24)){
#      for (i in c("typeTokenInput_50","typeTokenInput_37pt5","typeTokenInput_25","typeTokenInput_12pt5","typeTokenInput_4pt7","typeTokenInput_opposing","typeTokenInput_exaggerated")){
#        subdat = runs[runs$nlexCs==n&runs$pChangeIndexation==p&runs$lexCstartW==w&runs$inputSet==i,]
#        endpoint = min(100,length(subdat$filetag))
#        print(endpoint)
#        for (j in c(1:endpoint)){
#          thinnedRuns = rbind(thinnedRuns,subdat[j,])
#        } 
#      }
#    }
#  }
#}
#table(thinnedRuns$inputSet,thinnedRuns$lexCstartW,thinnedRuns$pChangeIndexation,thinnedRuns$nlexCs)
#ok we did it
#runs = thinnedRuns

# done thinning, now we calculate sums of things
min = min(l$Freq)
max = max(l$Freq)
nLexCs = 2
startW = 1
plot(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l",ylim=c(min-0.01,max+0.01))
startW = 2
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l")
startW = 5
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l")
startW = 10
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l")

nLexCs = 24
startW = 1
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l",col="grey")
startW = 2
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l",col="grey")
startW = 5
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l",col="grey")
startW = 10
points(as.numeric(l$Var2[l$Var3==startW&l$Var1==nLexCs]),l$Freq[l$Var3==startW&l$Var1==nLexCs],type="l",col="grey")
points(2,min)
#sse: 24, 0.05,5

#match to experiment: means & medians (of probabilities)
# For each cell, take the mean/median predicted prob
# use those to calculate error vs the experiment




#overall best - SSE's of SSE's across datasets
avg = as.data.frame(as.table(tapply(runs$predicted_p_fi_wug,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="mean")))
median = as.data.frame(as.table(tapply(runs$predicted_p_fi_wug,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="median")))
sd = as.data.frame(as.table(tapply(runs$predicted_p_fi_wug,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="sd")))

avg_exp = as.data.frame(as.table(tapply(runs$experiment_p_fi,list(runs$nlexCs,runs$pChangeIndexation,runs$lexCstartW,runs$inputSet),FUN="mean")))
avg = cbind(avg,median$Freq,sd$Freq,avg_exp$Freq)
colnames(avg) = c("nLexCs","pChangeIndexation","startW","inputSet","mean","median","sd","exp")

avg$sqE_mean = (avg$mean-avg$exp)^2
avg$sqE_med = (avg$median-avg$exp)^2

avg$lik_med = log(avg$median)*avg$exp
avg$lik_mean = log(avg$mean)*avg$exp

sse_mean = as.data.frame(as.table(tapply(avg$sqE_mean,list(avg$nLexCs,avg$pChangeIndexation,avg$startW),FUN="sum")))
sse_med = as.data.frame(as.table(tapply(avg$sqE_med,list(avg$nLexCs,avg$pChangeIndexation,avg$startW),FUN="sum")))
l_mean = as.data.frame(as.table(tapply(avg$lik_mean,list(avg$nLexCs,avg$pChangeIndexation,avg$startW),FUN="sum")))
l_med = as.data.frame(as.table(tapply(avg$lik_med,list(avg$nLexCs,avg$pChangeIndexation,avg$startW),FUN="sum")))


dataset = l_med
min = min(dataset$Freq)
max = max(dataset$Freq)
minParams = dataset[dataset$Freq==min,]
maxParams = dataset[dataset$Freq==max,]
nLexCs = 2
startW = 1
plot(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l",ylim=c(min-0.01,max+0.01))
startW = 2
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l")
startW = 5
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l")
startW = 10
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l")

nLexCs = 24
startW = 1
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l",col="grey")
startW = 2
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l",col="grey")
startW = 5
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l",col="grey")
startW = 10
points(as.numeric(dataset$Var2[dataset$Var3==startW&dataset$Var1==nLexCs]),dataset$Freq[dataset$Var3==startW&dataset$Var1==nLexCs],type="l",col="grey")
print(minParams)
print(maxParams)

#2, 0.05, 10
# with likelihood, do we get the same thing?
# not at all: 2, 0.99, 10

# k, graph both then:



