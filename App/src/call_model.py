import subprocess
import pandas as pd
import os

# Separa a data com base na porcentagem entrada para
# a data de teste, retorna o dataset de teste e
# treino
def split_data(train_data_percent: int, data: pd.DataFrame):
    # Cria o data set de teste
    test = data.sample(frac=train_data_percent, random_state=42)
    # Remove o data set de teste do data set de treino
    train = data.drop(test.index)

    return test, train

def run_model(file_name: str, model: str, response: str, predictors: str|list):
    # Caminho para o script R
    r_script_path = f"models/{model}"

    # Separa o dataset em treino e teste
    data = pd.read_csv(f"data/{file_name}")
    test, train = split_data(20, data)

    # Salva os dataset de treino e teste
    path_test = os.path.join("data", f"test_{file_name}")
    path_train = os.path.join("data", f"train_{file_name}")
    
    with open(path_test, 'w') as f: f.write(test.to_csv())
    with open(path_train, 'w') as f: f.write(train.to_csv())

    comando = ["Rscript", r_script_path, path_train, response]
    for p in predictors:
        comando.append(p)

    # Executa o comando e captura a saída
    try:
        # Pega a saída (stdout), erros (stderr) e decodifica para texto
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        # Imprime a saída do script R
        print("Saída do script R:")
        print(resultado.stdout)
        return resultado.stdout

    except subprocess.CalledProcessError as e:
        # Trata erros de execução do R
        print("Erro ao executar o script R:")
        print(e.stderr)