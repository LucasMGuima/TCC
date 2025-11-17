# Configurar caminggeho da biblioteca do usuário
.libPaths(c(file.path(Sys.getenv("HOME"), "R", "library"), .libPaths()))

library(mgcv)
library(readr)

source("models/model_utils.r")

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3){
  stop("O argumento passado não é valido.", call. = FALSE)
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))
names(data) <- make.names(names(data))

# Keep original response and predictor names for display
response_original <- response
predictors_original <- predictors

# Ensure response and predictors match sanitized column names
response <- make.names(response)
predictors <- make.names(predictors)

# Identificar os tipos dos dados dos preditores
# Gerar a formula dinamicamente com base nisso

# Parâmetros para construção automática dos smooths
default_k <- 10L        # k máximo por smooth
min_uniques_for_s <- 8  # mínimo de valores únicos para considerar s()

# garantir que todos os preditores existem nos dados
present_preds <- predictors[predictors %in% names(data)]
missing_preds <- setdiff(predictors, present_preds)
if (length(missing_preds) > 0) {
  warning("Os seguintes preditores não foram encontrados nos dados e serão ignorados: ", paste(missing_preds, collapse = ", "))
}
predictors <- present_preds

# construir termos: usar s() apenas quando apropriado
smoth_terms <- lapply(predictors, function(pred) {
  col <- data[[pred]]
  uniq <- length(unique(na.omit(col)))
  # se for fator ou character -> incluir como factor (sem s)
  if (is.factor(col) || is.character(col)) {
    paste0("factor(", pred, ")")
  } else if (!is.numeric(col)) {
    # tentar converter strings numéricas sujas para numeric e reavaliar
    col_num <- suppressWarnings(as.numeric(gsub(",", ".", as.character(col))))
    if (all(is.na(col_num))) {
      paste0("factor(", pred, ")")
    } else {
      uniq_num <- length(unique(na.omit(col_num)))
      if (uniq_num >= min_uniques_for_s) {
        kk <- max(3L, min(default_k, uniq_num))
        paste0("s(", pred, ", k = ", kk, ")")
      } else {
        pred
      }
    }
  } else {
    # coluna numeric
    if (uniq >= min_uniques_for_s) {
      kk <- max(3L, min(default_k, uniq))
      paste0("s(", pred, ", k = ", kk, ")")
    } else {
      pred
    }
  }
})

if (length(smoth_terms) == 0) {
  stop("Nenhum preditor válido encontrado para construir a fórmula.", call. = FALSE)
}

string <- paste(response, "~", paste0(unlist(smoth_terms), collapse = " + "))
formula <- as.formula(string)

model <- gam(formula, data = data)
summary(model)

model_name <- gsub("train_", "gam_", file_name)
model_name <- gsub(".csv", ".rds", model_name)
model_path <- save_model(model, model_name)

data_path <- file.path("data", file_name)
data_path <- gsub("train_", "test_", data_path)

save_json(response, predictors, data_path, model_path)