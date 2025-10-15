# Configurar caminho da biblioteca do usuário
.libPaths(c(file.path(Sys.getenv("HOME"), "R", "library"), .libPaths()))

library(mgcv)
library(readr)

source("models/model_utils.r")

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3){
  stop("O argumento passado não é valido.", call. = FALSE)
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))
names(data) <- make.names(names(data))

# Ensure response and predictors match sanitized column names
response <- make.names(response)
predictors <- make.names(predictors)

# Identificar os tipos dos dados dos preditores
# Gerar a formula dinamicamento com base nisso

smoth_predictors <- paste0("s(", predictors, ")")
string <- paste(response, "~", paste0(smoth_predictors, collapse = " + "))
formula <- as.formula(string)

model <- gam(formula, data = data)