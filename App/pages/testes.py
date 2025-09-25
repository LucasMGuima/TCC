import utils.widgets as wdg
import src.call_model
import streamlit as st
import re
import pandas as pd

db_avaliableModels = wdg.creat_multselect(
    wdg.contentIn_folder('modelos'),
    'Selecione um ou mais modelo(s) disponivel(is)'
)

if st.button("Cacular Metricas"):
    resp = []
    for avaliableModel in db_avaliableModels:
        model = f"modelos/{avaliableModel}"

        resp.append(src.call_model.run_teste(model))
    print(resp)