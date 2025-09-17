import streamlit as st
from data_service import load_file
from redis_config.redis_utils import redis_config


def show_ui():
    red= redis_config()
    df=red.load_churn_data()
    if df is None:
        st.error("Data Not avialble")
    else:    
        st.subheader("Data Preview")
        st.table(df.head())
        return df
    