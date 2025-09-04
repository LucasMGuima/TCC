library(readr)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0){
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

file_name <- sprintf("modelos/glm_%s.rds", gsub(".csv", "", file_name))
saveRDS(model, file = file_name)
