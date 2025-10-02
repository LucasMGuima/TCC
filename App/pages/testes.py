import utils.widgets as wdg
import src.call_model
import streamlit as st
import re
import pandas as pd

modelos_disponiveis = filter(lambda x: ".json" in x,  wdg.contentIn_folder('modelos'))


db_avaliableModels = wdg.creat_multselect(
    modelos_disponiveis,
    'Selecione um ou mais modelo(s) disponivel(is)'
)

if st.button("Cacular Metricas"):
    resp = []
    for avaliableModel in db_avaliableModels:
        model = f"modelos/{avaliableModel}"

        resp.append(src.call_model.run_teste(model))
    for r in resp:
        st.write(f"{r}\n")