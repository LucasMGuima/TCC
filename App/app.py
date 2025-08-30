import streamlit as st
import pandas as pd
import os, io
import src.call_model
import requests

# Upload em uma pagina propria ?
# Paginas para configurações ?

def contentIn_folder(folder: str) -> list|None:
    if os.path.exists(folder) and os.path.isdir(folder):
        return os.listdir(folder)
    else:
        return None

def creat_selectbox(list: list, label: str|None):
    return st.selectbox(label, list)

def creat_multselect(list: list, label: str|None):
    return st.multiselect(label, list)

st.title("App")

db_models = creat_selectbox(
    contentIn_folder('models'),
    'Selecione um modelo:'
)
db_data = creat_selectbox(
    contentIn_folder('data'),
    'Selecione um dataset'
)

if db_data:
    path = f"data/{db_data}"
    lst_param = pd.read_csv(path).columns.to_list()
    sb_response = creat_selectbox(
        lst_param,
        'Selecione o parametro de resposta'
    )
    sb_predictor = creat_multselect(
        lst_param,
        'Selecione um ou mais preditores'
    )

if st.button("Rodar"): 
    src.call_model.run_model(db_data, db_models, sb_response, sb_predictor)
   