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

save_formula_csv(response, predictors, sprintf("mars_formula_%s", file_name))
save_model(model, sprintf("mars_%s", gsub(".csv", ".rds", file_name)))