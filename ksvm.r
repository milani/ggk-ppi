library(kernlab)
library(caret)

getValues <- function(dataset,kernel) {
  f <- function(row) { kernel[row[1],row[2]] }
  values <- apply(dataset,1,f)
}

graphletCounts <- function(path) {
  filenames = list.files(path,full.names=TRUE)
  labels = unlist(strsplit(basename(filenames),'.edges'))
  counts <- matrix(unlist(lapply(filenames,read.table,header=FALSE)),ncol=30,byrow=TRUE)
  colnames(counts) <- mapply(paste,rep("G",30),c(0:29),sep="")
  rownames(counts) <- labels
  return(counts)
}
counts <- graphletCounts("counts/")
interactions <- read.table("DIP-Scere20100614CR.pdbs")
noninteractions <- read.table("DIP-Scere20100614CR-noninteractions.pdbs")

labels <- c(rep(1,nrow(interactions)),rep(2,nrow(noninteractions)))
ppi.dataset <- rbind(interactions,noninteractions)

ppi.values <- data.frame(G1=counts[ppi.dataset[,1],],G2=counts[ppi.dataset[,2],],data.frame(L=factor(labels)))
#ppi.values <- data.frame(V=getValues(ppi.dataset,kernel),L=factor(labels))

inTrain <- createDataPartition(y=ppi.values[,2],p=0.7,list=FALSE)
trainSet <- ppi.values[inTrain,]
testSet <- ppi.values[-inTrain,]




rbf <- rbfdot(2)

k <- kernelMatrix(rbf,trainSet[,-2])
trainPoints <- cmdscale(k,k=3)
trainPoints <- trainPoints*10^7
k <- kernelMatrix(rbf,testSet[,-2])
testPoints <- cmdscale(k,k=3)
testPoints <- testPoints*10^7

f<-function(x,y) {x<-x+0.1;-0.7^(-20*(3*crossprod(x,y) - crossprod(x) - crossprod(y)))+0.9}
kernel <- kernelMatrix(f,trainPoints)
model <- ksvm(kernel,y=trainSet[,2],scaled=FALSE,C=10)
supports <- SVindex(model)
kTest <- kernelMatrix(f,trainPoints[supports,],testPoints)
pred = predict(model,t(kTest))
confusionMatrix(table(pred=pred,true=testSet[,2]))

