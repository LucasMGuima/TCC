from __future__ import annotations

import pandas as pd


def load_data(file, nrows: int = 100):
    """Lê arquivo CSV/XLSX limitado a nrows (sem dependência do Streamlit).

    Retorna um DataFrame do pandas ou None se extensão não suportada ou file None.
    """
    if file is None:
        return None

    name = getattr(file, "name", "")
    if ".csv" in name:
        return pd.read_csv(file, nrows=nrows)
    if ".xlsx" in name:
        return pd.read_excel(file, nrows=nrows)
    return None


def perform_upload(conection, bucket_name: str, file) -> None:
    """Envia o arquivo para o bucket usando abstração de database.

    Essa função é fina e orquestra upload sem acessar Streamlit diretamente.
    """
    from utils import database

    if file is None:
        return None
    return database.upload_content(conection, bucket_name, file)

