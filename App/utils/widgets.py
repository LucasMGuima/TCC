import streamlit as st
import os

def contentIn_folder(folder: str) -> list|None:
    if os.path.exists(folder) and os.path.isdir(folder):
        return os.listdir(folder)
    else:
        return None

def creat_selectbox(list: list, label: str|None):
    return st.selectbox(label, list)

def creat_multselect(list: list, label: str|None):
    return st.multiselect(label, list)