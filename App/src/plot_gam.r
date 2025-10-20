  library(mgcv)

  args <- commandArgs(trailingOnly = TRUE)

  if (length(args) == 0){
    stop("O argumento passado não é valido.", call. = FALSE)
  }

  modelo_nome <- args[1]

  # Carrega o modelo especifico
  model <- readRDS(file.path(modelo_nome))
  modelo_nome

  # Plota e captura o retorno, sem gerar um pdf
  plot_data <- {
      pdf(NULL)
      res <- plot(model)
      invisible(dev.off())
      res
  }
  # plot_data: contem as informações usadas para plotar o gráfico

  plot_data[[1]]