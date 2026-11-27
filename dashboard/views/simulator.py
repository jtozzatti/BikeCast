import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.i18n import tr,format_number as fmt
from dashboard.services.data_service import load_dataset
from dashboard.services.model_service import predict
from dashboard.components.charts import show

def render_simulator():
    st.title(tr('Demand Simulator','Simulador de demanda'))
    st.info(tr('Historical scenario simulation (2011–2012), not a live forecast. Calendar and weather inputs start from an observed record.','Simulação histórica (2011–2012), não uma previsão atual. Calendário e clima partem de um registro observado.'))
    df=load_dataset(); dates=sorted(df.datetime.dt.date.unique())
    day=st.selectbox(tr('Historical date','Data histórica'),dates,index=len(dates)-1)
    rows=df[df.datetime.dt.date==day].sort_values('hr')
    hour=st.selectbox(tr('Observed hour','Hora observada'),rows.hr.tolist())
    row=rows[rows.hr==hour].iloc[[0]].copy()
    with st.form('scenario'):
        a,b=st.columns(2)
        with a:
            weather=st.selectbox(tr('Weather category','Categoria climática'),[1,2,3,4],index=int(row.weathersit.iloc[0])-1,format_func=lambda v:{1:tr('Clear / partly cloudy','Limpo / parcialmente nublado'),2:tr('Mist / cloudy','Névoa / nublado'),3:tr('Light rain / snow','Chuva / neve leve'),4:tr('Severe weather (rare)','Clima severo (raro)')}[v])
            temp=st.slider(tr('Normalized temperature','Temperatura normalizada'),0.,1.,float(row.temp.iloc[0]),.01)
            atemp=st.slider(tr('Normalized feels-like temperature','Sensação térmica normalizada'),0.,1.,float(row.atemp.iloc[0]),.01)
        with b:
            hum=st.slider(tr('Relative humidity (%)','Umidade relativa (%)'),0.,100.,float(row.hum.iloc[0])*100,1.)
            wind=st.slider(tr('Normalized wind speed','Velocidade do vento normalizada'),0.,1.,float(row.windspeed.iloc[0]),.01)
            st.caption(tr('Normalized inputs follow the dataset scale; independently edited conditions may be unrealistic.','Entradas seguem a escala do dataset; condições editadas independentemente podem ser irreais.'))
        submitted=st.form_submit_button(tr('Simulate demand','Simular demanda'),type='primary')
    if submitted:
        row.loc[:,['weathersit','temp','atemp','hum','windspeed']]=[weather,temp,atemp,hum/100,wind]
        value=float(predict(row)[0]); st.metric(tr('Estimated rentals in selected hour','Aluguéis estimados na hora selecionada'),fmt(value,0))
        if weather==4: st.warning(tr('Very rare weather category: estimate is unreliable.','Categoria climática muito rara: estimativa pouco confiável.'))
        profile=pd.concat([row]*24,ignore_index=True); profile['hr']=range(24); profile['estimate']=predict(profile)
        st.subheader(tr('Scenario profile (fixed weather)','Perfil do cenário (clima fixo)'))
        show(px.line(profile,x='hr',y='estimate',markers=True,color_discrete_sequence=['#22D3EE']),tr('Hour','Hora'),tr('Estimated rentals','Aluguéis estimados'))
        st.caption(tr('Point estimates only; no calibrated prediction intervals.','Estimativas pontuais; sem intervalos de previsão calibrados.'))
