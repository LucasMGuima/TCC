library(caTools)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2){
  stop("O argumento passado não é valido.", call. = FALSE)
}

model_file <- args[1]
data_test_file <- args[2]

# Extrai o nome da coluan de resposta
response_col_name <- all.vars(formula(model))[1]

model <- load(model_file) # Carrega o modelo
data_test <- read.csv(data_test_file) # Carrega os dados de teste

# Previsão
pred <- predict(model, type = "response", newdata = data_test)

y_actual <- data_test$response_col_name
cm <- table(y_actual, y_pred)

# Função que calcula as metricas
err_metric <- function(confusion_matrix){
  # Extrai os valores da matriz de confusao
  tp <- confusion_matrix[2, 1]
  tn <- confusion_matrix[1, 1]
  fp <- confusion_matrix[1, 2]
  fn <- confusion_matrix[2, 1]

  # Calcula as metricas
  accuracy <- (tp + tn) / sum(confusion_matrix)
  precision <- tp / (tp + fp)
  recall <- tp / (tp + fn)

  metrics <- data.frame(
    Métrica = c("Acurácia", "Precisão", "Recall"),
    Valor = c(accuracy, precision, recall)
  )

  metrics
}

metrics_df <- err_metric(cm)
metrics_df