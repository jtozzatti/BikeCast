from pathlib import Path
import streamlit as st
from dashboard.i18n import tr,t,PAGES

def render_sidebar():
    with st.sidebar:
        st.image((Path(__file__).resolve().parents[1]/'assets/logo.svg').read_text(encoding='utf-8'),width=58)
        st.header('BikeCast')
        st.caption(tr('URBAN MOBILITY INTELLIGENCE','INTELIGÊNCIA EM MOBILIDADE URBANA'))
        st.divider()
        st.caption(tr('WORKSPACE','NAVEGAÇÃO'))
        page=st.radio('Navigation',list(PAGES),format_func=t,key='navigation',label_visibility='collapsed')
        st.divider()
        st.caption(tr('Historical dataset · 2011–2012','Dados históricos · 2011–2012'))
        st.markdown(f'[{tr("GitHub Repository","Repositório GitHub")}](https://github.com/jtozzatti/BikeCast)')
    return page
