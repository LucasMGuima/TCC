import utils.database as database
import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data(file, nrows=100):
    if file is not None:
        if '.csv' in file.name:
            return pd.read_csv(file, nrows=nrows)
        elif '.xlsx' in file.name:
            return pd.read_excel(file, nrows=nrows)
        else:
            return None
    return None

st.title("File Upload")

file = st.file_uploader("Carregar arquivo: ", type=["csv", "xlsx"])
bucket_name = 'data'

db = database.Conection()
print(f"ID da conexão: {id(db)}")

if st.button("Carregar"):
    if file is not None:
        try:
            response = db.supabase.storage.from_(bucket_name).upload(
                path=file.name,
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

        