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

# Identificar os tipos dos dados dos preditores
# Gerar a formula dinamicamento com base nisso

smoth_predictors <- paste0("s(", predictors, ")")
string <- paste(response, "~", paste0(smoth_predictors, collapse = " + "))
formula <- as.formula(string)

model <- gam(formula, data = data)
summary(model)

save_formula_csv(response, predictors, sprintf("gam_formula_%s", file_name))
save_model(model, sprintf("gam_%s", gsub(".csv", ".rds", file_name)))