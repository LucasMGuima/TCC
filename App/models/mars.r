library(mda)
library(readr)

args <- commandArgs(trailingOnly = TRUE)

if(length(args) < 3){
    stop(
        "O argumento passado não é valido.",
        call. = FALSE
    )
}

file_name <- args[1]
response <- args[2]
predictors <- args[3:length(args)]

data <- read_csv(file.path("data", file_name))

# Transforma os preditores em uma matris
# Pega os valores numericos das colunas
x_predictors <- as.matrix(data[predictors])

# Transforma a coluna de resposta em um vetor
y_response <- data[[response]]

model <- mars(x_predictors, y_response)
summary(model)

file_name <- sprintf("modelos/mars_%s.rds", gsub(".csv", "", file_name))
saveRDS(model, file = file_name)