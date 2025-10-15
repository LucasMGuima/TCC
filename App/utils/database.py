import os

from supabase import create_client, Client
from dotenv import load_dotenv

class Conection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Conection, cls).__new__(cls)

            # Carrega as variaveis de ambiente
            load_dotenv()

            # Pega os dados para a conexão
            url: str = os.getenv("SUPABASE_URL")
            key: str = os.getenv("SUPABASE_ANON_KEY")

            # Verifica se as credenciais estão configuradas
            if not url or not key or url == "https://your-project.supabase.co" or key == "your-anon-key-here":
                print("⚠️  Credenciais do Supabase não configuradas. Executando em modo offline.")
                cls._instance.supabase = None
                cls._instance.offline_mode = True
            else:
                # Cria a instancia da classe
                cls._instance.supabase = start_conection(url, key)
                cls._instance.offline_mode = cls._instance.supabase is None

        return cls._instance

def start_conection(url: str, key: str) -> Client:
    try:
        cliente: Client = create_client(url, key)
        print("Cliente criado com sucesso.")
        return cliente
    except ValueError as e:
        print(f"Erro ao criar o cliente Supabase: Missing or invalid URL/Key - {e}")
        return None
    except ModuleNotFoundError as e:
        print(f"Erro ao criar o cliente Supabase: Missing dependency - {e}")
        return None
    except Exception as e:
        print(f"Um erro não experado ocorreu durante a criação do cliente Supabase: {e}")
        return None
    
def contentIn_bucket(conection: Conection, folder: str) -> list:
    print(f"ID da conexão: {id(conection)}")
    
    # Se estiver em modo offline ou sem conexão, lista arquivos locais
    if conection.offline_mode or conection.supabase is None:
        print(f"📁 Listando arquivos locais da pasta: {folder}")
        return list_local_files(folder)
    
    try:
        response = conection.supabase.storage.from_("data").list(folder,{
            "limit": 100,
            "offset": 0,
            "sortBy": {"column": "name", "order": "desc"},
        })

        content = []
        for item in response:
            name = item["name"]
            content.append(name)
        return content
    except Exception as e:
        print(f"⚠️  Erro ao acessar Supabase: {e}. Usando arquivos locais.")
        return list_local_files(folder)

def list_local_files(folder: str) -> list:
    """Lista arquivos na pasta local quando o Supabase não está disponível"""
    local_path = os.path.join("data", folder) if folder != "data" else "data"
    
    if not os.path.exists(local_path):
        print(f"📁 Criando pasta: {local_path}")
        os.makedirs(local_path, exist_ok=True)
        return []
    
    try:
        files = [f for f in os.listdir(local_path) if os.path.isfile(os.path.join(local_path, f))]
        print(f"📁 Encontrados {len(files)} arquivos em {local_path}")
        return files
    except Exception as e:
        print(f"⚠️  Erro ao listar arquivos locais: {e}")
        return []

def upload_content(conection: Conection, bucket_name: str, file) -> None:
    try:
        response = conection.supabase.storage.from_(bucket_name).upload(
            path=f"dados/{file.name}",
            file=file.read(),
            file_options={
                "cache-control": "3600",
                "upsert": "false"  # Set to "true" to replace an existing file
            }
        )
        print(f"Arquivo '{file}' armazenado com sucesso em '{bucket_name}/{file.name}'.")
        # The response object can contain useful information, but it's often empty on success
        print("Resposta do Supabase:", response.data)
    except Exception as e:
        print(f"Erro ao armazenar arquivo: {e}")
