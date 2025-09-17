import streamlit as st
from components.ui import show_ui
from data_service import load_file
from llm_service import get_sdf
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.set_page_config(page_title="PandasAI Streamlit Dashboard", layout="wide")
    st.title("📊 PandasAI Dashboard")
    df = show_ui()
    sdf = get_sdf(df=df)
    if df is not None:
        user_prompt = st.text_input("Ask a question about the data:")
        if st.button("Run Query") and user_prompt:
            try:
                answer = sdf.run(user_prompt)
                st.subheader("Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()