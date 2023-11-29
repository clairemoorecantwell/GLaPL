runs = read.table("gridSearchOutput.txt",sep="\t",header=TRUE,comment.char = "#")
table(runs$inputSet,runs$lexCstartW,runs$pChangeIndexation,runs$nlexCs)
summary(runs)
runs$predP_fi_withLexCFor_pl = exp(-(runs$w_fi+runs$w_fi_pl))/(exp(-(runs$w_fi+runs$w_fi_pl))+exp(-(runs$w_ku+runs$w_ku_pl)))

plot(runs$nlexCs,runs$likelihood,ylim=c(-0.02,0))
plot(jitter(runs$experiment_p_fi,1),runs$predP_fi_withLexCFor_pl,cex=0.01)

plot(jitter(runs$experiment_p_fi[runs$nlexCs==2&runs$lexCstartW==1&runs$pChangeIndexation==0.01],1),runs$predP_fi_withLexCFor_pl[runs$nlexCs==2&runs$lexCstartW==1&runs$pChangeIndexation==0.01],cex=0.01)
abline(0,1)
plot(runs$w_fi_pl,runs$predicted_p_fi_wug)

plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_4pt7"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_4pt7"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_12pt5"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_12pt5"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_25"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_25"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_37pt5"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_37pt5"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_50"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_50"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_exaggerated"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_exaggerated"])
plot(runs$w_ku_pl[runs$inputSet=="typeTokenInput_opposing"],runs$w_fi_pl[runs$inputSet=="typeTokenInput_opposing"])


plot(runs$w_ku_pl[runs$nlexCs==24],runs$w_fi_pl[runs$nlexCs==24])
plot(runs$w_ku_pl[runs$nlexCs==2],runs$w_fi_pl[runs$nlexCs==2])
plot(runs$w_ku_pl[runs$nlexCs==24],runs$w_fi_pl[runs$nlexCs==24])
plot(runs$w_ku_pl[runs$pChangeIndexation==.01],runs$w_fi_pl[runs$pChangeIndexation==.01])
plot(runs$w_ku_pl[runs$pChangeIndexation==.99],runs$w_fi_pl[runs$pChangeIndexation==.99])
plot(runs$w_ku_pl[runs$pChangeIndexation==.5],runs$w_fi_pl[runs$pChangeIndexation==.5])

hist(runs$SSE,breaks=100000,xlim=c(0,.0003))
hist(runs$SSE[runs$pChangeIndexation==.99],breaks=1000,xlim=c(0,.0003))
hist(runs$SSE[runs$pChangeIndexation==.01],breaks=1000,xlim=c(0,.0003))
hist(runs$SSE[runs$inputSet=="typeTokenInput_4pt7"],breaks=10000,xlim=c(0,.0003))

hist(runs$SSE[runs$lexCstartW==2],breaks=10000,xlim=c(0,.0003))
