import os
import streamlit as st
from src.agent import answer_question

st.title("Agentic Data Analyst")
question = st.text_input("Ask a business question")
if question and st.button("Run"):
    try:
        result = answer_question(question, os.environ["DATABASE_URL"], docs=[])
        st.code(result.sql, language="sql")
        st.dataframe(result.rows)
    except Exception as exc:
        st.error(str(exc))
