save_formula_csv <- function(response, predictors, file_name){
  file <- sprintf("data/%s", file_name)
  lst_predictors <- paste(predictors, collapse = "|")
  content <- sprintf("Response, Preditors\n%s, %s", response, lst_predictors)
  cat(content, file = file, append = FALSE)
}

save_model <- function(model, file_name){
  file_name <- sprintf("modelos/%s", file_name)
  saveRDS(model, file = file_name)
}