library(mgcv)
library(readr)

pisa <- read_csv(file.path("models/data", "pisasci2006.csv"))

model <- gam(Overall ~ Income, data = pisa)
summary(model)