def cria_matrizConfusao(model):
    return 0

# Calcula o F1-score apartir da matriz de confusao
def f1_score(matriz) -> float:
    f1_score = (precisao(matriz) * recall(matriz)) / (precisao(matriz) + recall(matriz))
    return f1_score

# Calcula o recall apartir da matriz de confusao
def recall() -> float:
    # formula do recall
    return 0

# Calucla a precisao apartir da matriz de confusao
def precisao() -> float:
    # formula da precisao
    return 0