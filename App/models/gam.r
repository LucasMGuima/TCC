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

model_name <- gsub("train_", "gam_", file_name)
model_name <- gsub(".csv", ".rds", model_name)
model_path <- save_model(model, model_name)

data_path <- file.path("data", file_name)
data_path <- gsub("train_", "test_", data_path)

save_json(response, predictors, data_path, model_path)