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

            # Cria a instancia da classe
            cls._instance.supabase = start_conection(url, key)

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
