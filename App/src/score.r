source("src/score_categorico.r")
source("src/score_continuo.r")

## Pega os argumentos modelo e dados

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("O argumento passado não é valido.", call. = FALSE)
}

model_file <- args[1]
data_test_file <- args[2]

model <- readRDS(model_file) # Carrega o modelo
data_test <- read.csv(data_test_file) # Carrega os dados de test

## Verifica o dado alvo
# Chama o script correspondendo para categorico ou continuo

response_col_name <- all.vars(formula(model))[1] # Pega a col. de resposta
unic_values <- length(unique(data_test[response_col_name])) # Qtd de valores unicos
all_values <- length(data_test[response_col_name]) # Qtd geral de valores

percent_unic <- (unic_values*100)/all_values

col_class <- class(data_test[response_col_name]) 

if((col_class == 'factor' || col_class == 'character') &&  percent_unic < 10){
    score_categorico(model, data_test) # O dado é categorico
}else{
    score_continuo(model, data_test) # O dado é continuo
}