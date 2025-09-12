import utils.widgets as wdg
import src.call_model
import streamlit as st
import re

db_avaliableModels = wdg.creat_selectbox(
    wdg.contentIn_folder('modelos'),
    'Selecione um modelo disponivel'
)

if st.button("Cacular Metricas"):
    # Encontra o data set de teste
    file_name = re.search("[a-zA-Z0-9]+.rds", db_avaliableModels).group().replace('.rds', '')
    data_test = f"data/test_{file_name}.csv"

    model = f"modelos/{db_avaliableModels}"

    resp = src.call_model.run_teste(model, data_test)
    print(resp)