import subprocess
import pandas as pd
from utils import database
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
    """Executa um modelo R com os dados fornecidos"""
    
    # Validações de entrada
    if not data_name or not model or not response or not predictors:
        raise ValueError("Todos os parâmetros são obrigatórios")
    
    if isinstance(predictors, str):
        predictors = [predictors]
    
    if not predictors:
        raise ValueError("Pelo menos um preditor deve ser fornecido")
    
    # Verifica se as colunas existem no dataset
    missing_cols = [col for col in [response] + predictors if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Colunas não encontradas no dataset: {missing_cols}")
    
    # Caminho para o script R
    r_script_path = os.path.join("models", model)
    
    if not os.path.exists(r_script_path):
        raise FileNotFoundError(f"Script R não encontrado: {r_script_path}")

    # Normaliza o nome do arquivo
    data_name = os.path.basename(data_name.replace("\\", "/"))
    path_test = os.path.join("data", f"test_{data_name}")
    path_train = os.path.join("data", f"train_{data_name}")

    # Cria a pasta data se não existir
    os.makedirs("data", exist_ok=True)
    os.makedirs("modelos", exist_ok=True)

    if not os.path.isfile(path_test) or not os.path.isfile(path_train):
        print(f"📊 Criando datasets de treino e teste para {data_name}")
        # Separa o dataset em treino e teste
        test, train = split_data(20, data, response)

        # Salva os arquivos CSV corretamente
        test.to_csv(path_test, index=False, encoding='utf-8')
        train.to_csv(path_train, index=False, encoding='utf-8')
        
        print(f"✅ Datasets salvos: {path_train} ({len(train)} amostras), {path_test} ({len(test)} amostras)")
    else:
        print(f"📁 Usando datasets existentes: {path_train}, {path_test}")

    # Prepara o comando para execução do R
    train_filename = os.path.basename(path_train)
    comando = ["Rscript", r_script_path, train_filename, response] + predictors

    # Executa o comando e captura a saída
    try:
        # Pega a saída (stdout), erros (stderr) e decodifica para texto
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        return resultado.stdout

    except subprocess.CalledProcessError as e:
        # Trata erros de execução do R
        print("Erro ao executar o script R para treino do modelo:")
        print(e.stderr)

def run_teste(json: str):
    src_path = "src/score.r"
    comando = ["Rscript", src_path, json]
    print(f"Comando: {comando}")

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        return resultado.stdout
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script R para calculo de metricas para o modelo {json}:")
        print(e.stderr)
