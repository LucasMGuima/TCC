library(jsonlite)

source("src/score_categorico.r")
source("src/score_continuo.r")

## Pega os argumentos modelo e dados

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  stop("O argumento passado não é valido.", call. = FALSE)
}

# Carrega o JSON
json_file <- args[1]
json_dado <- fromJSON(json_file)

model <- readRDS(json_dado$model) # Carrega o modelo
data_test <- read.csv(json_dado$data_name) # Carrega os dados de test

## Verifica o dado alvo
# Chama o script correspondendo para categorico ou continuo

response_col_name <- json_dado$response_name
val_response <- data_test[response_col_name]

unic_values <- length(unique(val_response)) # Qtd de valores unicos
all_values <- length(val_response) # Qtd geral de valores

percent_unic <- (unic_values * 100) / all_values

col_class <- class(val_response)

if ((col_class == "factor" || col_class == "character") &&  percent_unic < 10){
  score_categorico(model, data_test) # O dado é categorico
}else {
  score_continuo(model, data_test, json_dado) # O dado é continuo
}