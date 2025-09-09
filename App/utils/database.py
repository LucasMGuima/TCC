import os
from supabase import create_client, Client

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