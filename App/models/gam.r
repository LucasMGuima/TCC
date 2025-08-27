library(mgcv)
library(readr)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0){
  stop("O argumento passado não é valido.", call. = FALSE)
}

file_name <- args[1]

pisa <- read_csv(file.path("data", file_name))

model <- gam(Overall ~ Income, data = pisa)
summary(model)