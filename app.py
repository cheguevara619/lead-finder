import streamlit as st

st.title("Teste")

def fetch_leads():
    leads = []
    leads.append("Funciona!")
    return leads

if st.button("Testar"):
    results = fetch_leads()
    for r in results:
        st.write(r)
