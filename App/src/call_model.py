import subprocess

def run_model(file_name: str, model: str, response: str, predictors: str|list):
    # Caminho para o seu script R
    r_script_path = f"models/{model}"

    comando = ["Rscript", r_script_path, file_name, response]
    for p in predictors:
        comando.append(p)

    # Executa o comando e captura a saída
    try:
        # Pega a saída (stdout), erros (stderr) e decodifica para texto
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        # Imprime a saída do script R
        print("Saída do script R:")
        print(resultado.stdout)

    except subprocess.CalledProcessError as e:
        # Trata erros de execução do R
        print("Erro ao executar o script R:")
        print(e.stderr)