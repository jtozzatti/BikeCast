import streamlit as st

def init_language():
    st.session_state.setdefault('language', 'en')

def tr(en, pt):
    return pt if st.session_state.get('language') == 'pt' else en

PAGES = {'overview': ('Overview','Visão geral'), 'insights': ('Key Insights','Principais descobertas'), 'analytics': ('Data Analytics','Análise de dados'), 'simulator': ('Demand Simulator','Simulador de demanda'), 'performance': ('Model Performance','Desempenho do modelo')}

def t(key):
    return tr(*PAGES[key]) if key in PAGES else key

def format_number(value, decimals=0):
    s = f'{value:,.{decimals}f}'
    return tr(s, s.translate(str.maketrans(',.','.,')))
