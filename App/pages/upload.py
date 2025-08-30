import streamlit as st
import pandas as pd
import os
import src.call_model as call

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

if st.button("Carregar"):
    data = load_data(file)

    if data is not None:
        path = os.path.join("data", file.name)
        with open(path, 'w') as f:
            if f.write(data.to_csv()):
                st.success("Upload Succes")