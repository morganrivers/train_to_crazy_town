

# This file contains helper functions for monte carlo simulations
# - Statistical distributions (uniform, beta, gamma) using a mean and standard deviation
# - Plot functions to visualise distributions or a vector of values
# - Functions to check moments of a distribution

##############################################################################
############ SEED & DEFAULT NUMBER OF SIMULATIONS#############################
##############################################################################

set.seed(123456)
sims <- 10000

##############################################################################
############ DISTRIBUTION HELPERS - MEAN & SD ################################
##############################################################################

#Define function to run a uniform distribution 'sims' times given a max and min
runi <- function(min,max) {
  runif(sims,min,max)  
}

#Gamma distribution as a function of mean and standard deviation (greater than 0)
rgam <- function(mean,sd) {
  rgamma(
    sims,
    shape=(mean^2)/(sd^2),
    scale=(sd^2)/(mean)
  )
}

#Beta distribution (bounded between 1 and 0)
rbet <- function(mean,sd) {
  var_beta <- sd^2
  coeff <- mean*(1-mean)/var_beta-1
  shape_1 <- mean*coeff
  shape_2 <- (1-mean)*coeff
  return (
    rbeta(sims,shape_1,shape_2))
}


##############################################################################
############ DISTRIBUTION HELPERS - CONFIDENCE INTERVAL ######################
##############################################################################

# Generalised function that estimates distribution parameters via an optimisation problem. 

dist_ci <- function(pdist,rdist,x1,x2,ci=0.90) {

  in_1<- 0.5
  in_2<- 0.25
  p1 <- 0+(1-ci)/2
  p2 <- 1-(1-ci)/2
  
  errorFn <- function(params) {
    (pdist(x1,params[1],params[2])-p1)^2+
      (pdist(x2,params[1],params[2])-p2)^2  
  }
  temp_output<- optim(c(in_1,in_2),errorFn)
  return(
    rdist(sims,temp_output$par[1],temp_output$par[2])
  ) 
}

# Define lognormal
rlognorm_ci <- function(x1,x2,ci=0.9) {
  if (x1<=0) {
    stop("values outside function range")
  }
  else dist_ci(plnorm,rlnorm,x1,x2,ci)
}

# Define beta
rbeta_ci <- function(x1,x2,ci=0.9) {
  if (x1<=0 | x2>=1 ) {
    stop("values outside function range")
  }
  else dist_ci(pbeta,rbeta,x1,x2,ci)
}

# Define gamma
rgamma_ci <- function(x1,x2,ci=0.9) {
  if (x1<=0) {
    stop("values outside function range")
  }
  else dist_ci(pgamma,rgamma,x1,x2,ci)
}

# Define normal
rnorm_ci <- function(x1,x2,ci=0.9)  (dist_ci(pnorm,rnorm,x1,x2,ci))


##############################################################################
############ VISUALISE DISTRIBUTIONS #########################################
##############################################################################

#Density plot to check how a chart looks
densplot <- function(fun,mean,sd) {
  data.frame(x=fun(mean,sd)) %>%
    ggplot(aes(x=x)) + geom_density()
}

#Density plot creator
densplotv<- function(vector) {
  tit <- rlang::englue("Density plot of {{vector}}")
  xlab <- rlang::englue("{{vector}}")
  
  data.frame(vector) %>%
    ggplot(aes(x= {{ vector }} )) + 
    geom_density() +
    theme_light() +
    labs(
      title=tit,
      y="",
      x=xlab)
}


##############################################################################
############ EXTRACT DATA FROM DISTRIBUTION###################################
##############################################################################

#Set quartiles to show
qtls=c(0.05,0.1,0.25,0.75,0.9,0.95)

#Show those quantiles
quantile_output <- function(x) {
  quantile(x,probs=qtls)
}

#Function to extract mean, sd, median and selected quartiles from a vector
moments_detailed<- function(x) {
  output<- c(mean(x),sd(x),median(x),quantile_output(x))
  names(output)<-c("mean","sd","median",str_c("p",100*qtls))
  return(output)
}

#Function to print a formatted html table with summary statistics for a list of vectors
summarystats <- function(...) {
  bind_cols(
    statistic=c("mean","sd","median",str_c("p",100*qtls)),
    tibble(...) %>%
      map(moments_detailed) %>%
      as_tibble())  %>%
    gt() %>%
    fmt_number(suffixing = TRUE, n_sigfig = 3) %>%
    return()
}

##############################################################################
############ EXTRACT DATA FROM DISTRIBUTION###################################
##############################################################################

obtain <- function(...) get(paste(...,sep="_"))

##############################################################################
############ CHART SAVING FUNCTION ###########################################
##############################################################################

save_chart <- function(name,plot_name) {
  plot_no_title <- plot_name+ labs(title=NULL,subtitle=NULL)
  ggsave(name,plot = plot_no_title,path ="../4_charts/", width = 6.7, height = 3.8,units = "in")
}

save_table <- function(tab_name,file_name) {
  gtsave(data=tab_name, filename=file_name, path = "../4_charts/")
}


