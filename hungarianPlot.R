h = read.table("hungarianInput",header=TRUE)
h$input = as.factor(h$input)

nak_rates = c()
logFs = c()
for (inpt in levels(h$input)){
  total = sum(h$obs.prob[h$input==inpt])
  nak = h$obs.prob[h$input==inpt][1]
  nak_rate = nak/total
  logF = log(total)
  nak_rates = c(nak_rates,nak_rate)
  logFs = c(logFs,logF)
}


plot(logFs,nak_rates,pch=20,cex=0.8,xlab="Log frequency of noun",ylab="% 'nak' in genetive")

f = read.table("racineData",header=TRUE)
plot(log(f$Frequ_films),f$AE.SE_FR,xlab="log frequency in films",ylab="Rating difference (with-without)",pch=20,cex=0.8)
