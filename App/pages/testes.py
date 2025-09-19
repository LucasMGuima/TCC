import utils.widgets as wdg
import src.call_model
import streamlit as st
import re

db_avaliableModels = wdg.creat_multselect(
    wdg.contentIn_folder('modelos'),
    'Selecione um ou mais modelo(s) disponivel(is)'
)

if st.button("Cacular Metricas"):
    resp = []
    for avaliableModel in db_avaliableModels:
        # Encontra o data set de teste
        file_name = re.search("[a-zA-Z0-9]+.rds", avaliableModel).group().replace('.rds', '')
        data_test = f"data/test_{file_name}.csv"

        model = f"modelos/{avaliableModel}"

        resp.append(src.call_model.run_teste(model, data_test))
    st.text(resp)