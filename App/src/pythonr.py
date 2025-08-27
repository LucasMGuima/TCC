import subprocess

# Caminho para o seu script R
r_script_path = "models/gam.r"

file_name = "pisasci2006.csv"

# Comando para rodar o script R
# 'Rscript' é o executável que roda scripts R a partir da linha de comando
comando = ["Rscript", r_script_path, file_name]

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