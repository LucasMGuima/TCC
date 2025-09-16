library(Metrics)
library(mgcv)

score_continuo <- function(model, data_test){
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

  # Calcula o RMSE
  mse <- mean(erros^2)
  rmse <- sqrt(mse)

  return(mae, rmse)
}