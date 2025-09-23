library(readr)

source("models/model_utils.r")

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3){
    stop(
        "O argumento passado não é valido.",
        call. = FALSE
        )
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))

string <- paste(response, "~", paste0(predictors, collapse = "+"))
formula <- as.formula(string)

model <- glm(formula, data = data)

save_formula_csv(response, predictors, sprintf("glm_formula_%s", file_name))
save_model(model, sprintf("glm_%s", gsub(".csv", ".rds", file_name)))