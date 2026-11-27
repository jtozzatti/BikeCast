from pathlib import Path
import pandas as pd
import streamlit as st
BASE_DIR=Path(__file__).resolve().parents[2]
@st.cache_data
def _read(path, modified):
    return pd.read_csv(path,encoding='utf-8-sig')
def read_csv(relative):
    path=BASE_DIR/relative
    return _read(str(path),path.stat().st_mtime_ns)
def load_dataset():
    df=read_csv('data/hour.csv')
    df['datetime']=pd.to_datetime(df['dteday'])+pd.to_timedelta(df['hr'],unit='h')
    return df
def load_modeling_results(): return read_csv('resultados_modelagem.csv')
def load_evaluation_metrics(): return read_csv('reports/metricas_avaliacao.csv')
def load_test_predictions():
    df=read_csv('reports/previsoes_teste.csv')
    df['datetime']=pd.to_datetime(df['datetime'])
    return df
