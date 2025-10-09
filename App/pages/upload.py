from utils import database
from services.upload_service import load_data as _load_data, perform_upload
import streamlit as st


# UI apenas: decora a função pura para cache
load_data = st.cache_data(_load_data)

st.title("File Upload")

file = st.file_uploader("Carregar arquivo: ", type=["csv", "xlsx"])
bucket_name = "data"

db = database.Conection()
print(f"ID da conexão: {id(db)}")

if st.button("Carregar"):
    if file is not None:
        perform_upload(db, bucket_name, file)
