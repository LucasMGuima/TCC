library(mgcv)

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
    Metrica = c("Acuracia", "Precisao", "Recall", "TP", "TN", "FP", "FN"),
    Valor = c(accuracy, precision, recall, tp, tn, fp, fn)
  )

  metrics
}

score_categorico <- function(model, data_test){
  # Extrai o nome da coluan de resposta
  response_col_name <- all.vars(formula(model))[1]

  # Previsão
  y_pred <- predict(model, type = "response", newdata = data_test)

  y_actual <- data_test[[response_col_name]]
  cm <- table(y_actual, y_pred)

  metrics_df <- err_metric(cm)
  return(metrics_df)
}