# Configurar caminho da biblioteca do usuário
.libPaths(c(file.path(Sys.getenv("HOME"), "R", "library"), .libPaths()))

library(readr)

source("models/model_utils.r")

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3){
    stop(
        "O argumento passado não é valido.",
        call. = FALSE
        )
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))

string <- paste(response, "~", paste0(predictors, collapse = "+"))
formula <- as.formula(string)

model <- glm(formula, data = data)
summary(model)

model_name <- gsub("train_", "glm_", file_name)
model_name <- gsub(".csv", ".rds", model_name)
model_path <- save_model(model, model_name)

data_path <- file.path("data", file_name)
data_path <- gsub("train_", "test_", data_path)

save_json(response, predictors, data_path, model_path)