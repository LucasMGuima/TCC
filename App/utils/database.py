import os
import pandas as pd
from supabase import create_client, Client

class Conection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Conection, cls).__new__(cls)

            # Pega os dados para a conexão
            db_keys = pd.read_csv("keys.csv")
            url: str = db_keys['NEXT_PUBLIC_SUPABASE_URL'][0]
            key: str = db_keys['NEXT_PUBLIC_SUPABASE_ANON_KEY'][0]

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
    
