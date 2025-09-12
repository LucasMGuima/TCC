library(Metrics)
library(mgcv)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("O argumento passado não é valido.", call. = FALSE)
}

model_file <- args[1]
data_test_file <- args[2]

model <- readRDS(model_file) # Carrega o modelo
data_test <- read.csv(data_test_file) # Carrega os dados de test

# Remove todas as linhas do data_test que contêm valores NA
data_test_limpo <- na.omit(data_test)

# Extrai o nome da coluan de resposta
response_col_name <- all.vars(formula(model))[1]

y_pred <- predict(model, newdata = data_test_limpo) # Previsão
y_actual <- data_test_limpo[[response_col_name]] # Valor real

# Calcula o MAE manual
erros <- y_actual - y_pred
erros_abs <- abs(erros)
mae <- mean(erros_abs)

mae