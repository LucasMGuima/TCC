import subprocess

def plot(modelo: str):
    # Prepara as partes do comando
    modelo_path = f"modelos/{modelo}"
    r_script = f"src/plot_model.r"
    # Prepara o comando
    comando = ["Rscript", r_script, modelo_path]

    # Executa o comando e captura a saída
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        print("Saída do script R:")
        print(resultado.stdout)
    
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o script R:")
        print(e.stderr)