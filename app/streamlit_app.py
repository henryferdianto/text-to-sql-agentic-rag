import streamlit as st
from src.agent import answer_question
from src.db import build

st.title("Agentic Data Analyst")
build()
question = st.text_input("Ask a business question")
if question and st.button("Run"):
    answer = answer_question(question)
    st.code(answer.sql, language="sql")
    st.dataframe(answer.rows)
