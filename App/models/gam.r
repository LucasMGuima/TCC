library(mgcv)
library(readr)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0){
  stop("O argumento passado não é valido.", call. = FALSE)
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))

# Identificar os tipos dos dados dos preditores
# Gerar a formula dinamicamento com base nisso

string <- paste(response, "~", paste0(predictors, collapse = " + "))
formula <- as.formula(string)

model <- gam(formula, data = data)
summary(model)