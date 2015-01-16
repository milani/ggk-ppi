prm <- data.frame(parameter = c("C", "sigma"),
                  class = rep("numeric", 2),
                  label = c("Cost", "Sigma"))

svmGrid <- function(x, y, len = NULL) {
  library(kernlab)
  sigmas <- sigest(as.matrix(x[,1:30]), na.action = na.omit, scaled = FALSE)
  expand.grid(sigma = mean(as.vector(sigmas[-2])),
              C = 2 ^((1:len) - 3))
}

svmFit <- function(x, y, wts, param, lev, last, classProbs, ...) {
  rbf <- rbfdot(param$sigma)
  f <- function(x) {
    k1 <- kernelMatrix(rbf,as.matrix(x[,1:30]))
    k2 <- kernelMatrix(rbf,as.matrix(x[,31:60]))
    #k3 <- kernelMatrix(rbf,as.matrix(x[,1:30]),as.matrix(x[,31:60]))
    #direct = 2*k1*k2/(k1+k2)
    direct = k1+k2
    return(direct)
    #indirect = 2*k3*t(k3)/(k3+t(k3))
    #pmax(direct,indirect)
  }
  kernel <- f(x)
  model = ksvm(as.kernelMatrix(kernel),y,
       C = param$C,
       prob.model = classProbs,
       ...)
  model@xmatrix = list(x=x,param=param)
  return(model)
}

svmPred <- function(modelFit, newdata, preProc = NULL, submodels = NULL){
  settings = modelFit@xmatrix
  trainSet = settings$x
  param = settings$param
  supports = trainSet[SVindex(modelFit),]
  rbf <- rbfdot(param$sigma)
  f2 <- function(x,y) {
    k1 <- kernelMatrix(rbf,as.matrix(x[,1:30]),as.matrix(y[,1:30]))
    k2 <- kernelMatrix(rbf,as.matrix(x[,31:60]),as.matrix(y[,31:60]))
    #k3 <- kernelMatrix(rbf,as.matrix(x[,1:30]),as.matrix(y[,31:60]))
    #k4 <- kernelMatrix(rbf,as.matrix(y[,1:30]),as.matrix(x[,31:60]))
    #direct = 2*k1*k2/(k1+k2)
    #indirect = 2*k3*t(k4)/(k3+t(k4))
    #pmax(direct,indirect)
    direct = k1+k2
    return(direct)
  }
  k <- f2(supports,newdata)
  predict(modelFit, as.kernelMatrix(t(k)))
}
  

svmProb <- function(modelFit, newdata, preProc = NULL, submodels = NULL){
  print("called")
  predict(modelFit, newdata, type="probabilities")
}
  

cKernel <- list(type="Classification",library=c("kernlab"),loop=NULL,parameters=prm,grid=grid,fit=svmFit,predict=svmPred,prob=svmProb)
cKernel$levels <- function(x) lev(x)
