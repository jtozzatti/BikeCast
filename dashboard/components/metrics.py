from html import escape
import streamlit as st

def render_metric(label,value,description):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{escape(str(label))}</div><div class="metric-value">{escape(str(value))}</div><div class="metric-description">{escape(str(description))}</div></div>', unsafe_allow_html=True)
