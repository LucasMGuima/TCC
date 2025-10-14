# Configurar caminho da biblioteca do usuário
.libPaths(c(file.path(Sys.getenv("HOME"), "R", "library"), .libPaths()))

library(mda)
library(readr)

source("models/model_utils.r")

args <- commandArgs(trailingOnly = TRUE)

if(length(args) < 3){
    stop(
        "O argumento passado não é valido.",
        call. = FALSE
    )
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))

# Trata os dados
data[sapply(data, is.infinite)] <- NA # Substitui valores infinitos por NA
data[sapply(data, is.nan)] <- NA # Substitui valores indefinidos por NA
data_limpa <- na.omit(data) # Remove as linhas com NA em qualquer coluna

# Transforma os preditores em uma matris
# Pega os valores numericos das colunas
x_predictors <- as.matrix(data_limpa[predictors])

# Transforma a coluna de resposta em um vetor
y_response <- data_limpa[[response]]

model <- mars(x_predictors, y_response)
summary(model)

model_name <- gsub("train_", "mars_", file_name)
model_name <- gsub(".csv", ".rds", model_name)
model_path <- save_model(model, model_name)

data_path <- file.path("data", file_name)
data_path <- gsub("train_", "test_", data_path)

save_json(response, predictors, data_path, model_path)