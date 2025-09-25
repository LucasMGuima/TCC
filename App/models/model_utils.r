library(jsonlite)

save_json <- function(response, predictors, data_path, model_path){

  lst_predictors <- paste(predictors, collapse = "|")

  df <- data.frame(
    model = model_path,
    reposnse_name = response,
    predictors_name = lst_predictors,
    data_name = data_path
  )

  json_content <- toJSON(df, pretty = TRUE)

  json_name <- gsub("models", "data", model_path)
  json_name <- gsub(".rds", ".json", json_name)

  write(json_content, json_name)
}

save_formula_csv <- function(response, predictors, file_name){
  file <- sprintf("data/%s", file_name)
  lst_predictors <- paste(predictors, collapse = "|")
  content <- sprintf("Response, Preditors\n%s, %s", response, lst_predictors)
  cat(content, file = file, append = FALSE)
  file
}

save_model <- function(model, file_name){
  file_name <- sprintf("modelos/%s", file_name)
  saveRDS(model, file = file_name)

  file_name
}
