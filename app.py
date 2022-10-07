import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import joblib

st.set_page_config(page_title="", page_icon="./Graficas/stockfish.png", layout="centered", initial_sidebar_state="auto")



def load_data():
    
    data = joblib.load("DataPrincipal.pkl")

    return data


######## DATAFRAME PRINCIPAL #########
df_data = load_data()
##################################

########### SIDEBAR ##########
with st.sidebar:

    
#############################