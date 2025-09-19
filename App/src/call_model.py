import subprocess
import pandas as pd
import utils.database as database
from sklearn.model_selection import train_test_split
import os

# Separa a data com base na porcentagem entrada para
# a data de teste, retorna o dataset de teste e
# treino
def split_data(test_data_percent: int, data: pd.DataFrame, target_columns: str):
    test_size_frac = test_data_percent / 100

    # Conte o número de valores ausentes
    valores_ausentes = data[target_columns].isnull().sum()
    print(f"Número de valores NaN na coluna de resposta: {valores_ausentes}")

    data.dropna(subset=[target_columns], inplace=True)

    test = data.sample(
        frac=test_size_frac,
        random_state=42
    )
    train = data.drop(test.index)

    return test, train

def run_model(data_name: str, data: pd.DataFrame, model: str, response: str, predictors: str|list):
    # Caminho para o script R
    r_script_path = f"models/{model}"

    # Salva os dataset de treino e teste, se n existir
    data_name = data_name.replace("data\\", "")
    path_test = os.path.join("data", f"test_{data_name}")
    path_train = os.path.join("data", f"train_{data_name}")

    if(not os.path.isfile(path_test) and not os.path.isfile(path_train)):
        # Separa o dataset em treino e teste
        test, train = split_data(20, data, response)

        with open(path_test, 'w') as f: 
            f.write(test.to_csv())
        # database.upload_content(database.Conection(), 'data', path_test)

        with open(path_train, 'w') as f: 
            f.write(train.to_csv())
        # database.upload_content(database.Conection(), 'data', path_train)

    comando = ["Rscript", r_script_path, path_train.replace("data\\", ""), response]
    for p in predictors:
        comando.append(p)

    # Executa o comando e captura a saída
    try:
        # Pega a saída (stdout), erros (stderr) e decodifica para texto
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        return resultado.stdout

    except subprocess.CalledProcessError as e:
        # Trata erros de execução do R
        print("Erro ao executar o script R para treino do modelo:")
        print(e.stderr)

def run_teste(model: str, data_test: str):
    src_path = "src/score.r"
    comando = ["Rscript", src_path, model, data_test]
    print(f"Comando: {comando}")

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        return resultado.stdout
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script R para calculo de metricas para o modelo {model}:")
        print(e.stderr)