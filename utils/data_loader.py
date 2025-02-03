import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    data = pd.read_csv("hots_cleaned_data_modified.csv")
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    return data
