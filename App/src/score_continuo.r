library(Metrics)
library(mgcv)
library(mda)
score_continuo <- function(model, data_test, json){

  # Substitui valores infinitos por NA
  data_test[sapply(data_test, is.infinite)] <- NA
  # Substitui valores indefinidos por NA
  data_test[sapply(data_test, is.nan)] <- NA
  # Remove todas as linhas do data_test que contêm valores NA
  data_test_limpo <- na.omit(data_test)

  # Remove NULL
  data_test_limpo |> subset(!mapply(is.null, data_test_limpo))

  # Extrai o nome da coluan de resposta
  response_col_name <- json$response_name

  predict_col_name <- json$predictors_name
  data_predict <-  data_test_limpo[predict_col_name]

  y_pred <- predict(model, newdata = data_predict) # Previsão
  y_actual <- data_test_limpo[[response_col_name]] # Valor real

  # Calcula o MAE manual
  erros <- y_actual - y_pred
  erros_abs <- abs(erros)
  val_mae <- mean(erros_abs)

  # Calcula o RMSE
  mse <- mean(erros^2)
  val_rmse <- sqrt(mse)

  # Cria a lista de retorno
  result <- list(mae = val_mae, rmse = val_rmse)
  result
}