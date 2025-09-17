from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI


llm = OpenAI(api_key="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")

def get_sdf(df):
    return create_pandas_dataframe_agent(df=df, llm=llm,verbose=True,allow_dangerous_code=True)