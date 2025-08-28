import streamlit as st
import pandas as pd
import os
import call_model

def creat_models_dropbox():
    model_folder = "models"

    if os.path.exists(model_folder) and os.path.isdir(model_folder):
        models = os.listdir(model_folder)

        return st.selectbox(
            'Selecione um modelo:',
            models
        )

def creat_data_dropbox():
    data_folder = "data"

    if os.path.exists(data_folder) and os.path.isdir(data_folder):
        data = os.listdir(data_folder)

        return st.selectbox(
            'Selecione um modelo:',
            data
        )

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

st.title("App")
file = st.file_uploader("Carregar Arquivo CSV.", type=["csv", "xlsx"])
data = load_data(file)
if data is not None:
    path = os.path.join("data", file.name)
    with open(path, 'w') as f:
        f.write(data.to_csv())

db_models = creat_models_dropbox()
db_data = creat_data_dropbox()

if st.button("Rodar"): 
    call_model.run_model(db_data, db_models)
   