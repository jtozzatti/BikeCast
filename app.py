from pathlib import Path
import streamlit as st
from dashboard.i18n import init_language,t,tr
from dashboard.components.sidebar import render_sidebar
from dashboard.views.overview import render_overview
from dashboard.views.insights import render_insights
from dashboard.views.analytics import render_analytics
from dashboard.views.simulator import render_simulator
from dashboard.views.performance import render_performance
st.set_page_config(page_title='BikeCast | Urban Intelligence',page_icon='🚲',layout='wide',initial_sidebar_state='expanded')
css=Path(__file__).resolve().parent/'dashboard/assets/styles.css'
st.markdown(f'<style>{css.read_text(encoding="utf-8")}</style>',unsafe_allow_html=True)
init_language()
_,right=st.columns([4,1])
with right:
    st.segmented_control('Language / Idioma',['pt','en'],format_func=lambda x: {'pt':'PT-BR','en':'EN-US'}[x],key='language',required=True,label_visibility='collapsed')
page=render_sidebar()
st.caption(f'BIKECAST / {t(page).upper()}')
try:
    {'overview':render_overview,'insights':render_insights,'analytics':render_analytics,'simulator':render_simulator,'performance':render_performance}[page]()
except (FileNotFoundError,KeyError,ValueError,RuntimeError) as exc:
    st.error(tr('Unable to load this page. Check the project files and dependencies.','Não foi possível carregar esta página. Confira os arquivos e dependências.'))
    st.exception(exc)
