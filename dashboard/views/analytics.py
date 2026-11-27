import streamlit as st
import plotly.express as px
from dashboard.i18n import tr,format_number as fmt
from dashboard.services.data_service import load_dataset
from dashboard.components.charts import show

def render_analytics():
    st.title(tr('Data Analytics','Análise de dados'))
    df=load_dataset()
    a,b=st.columns(2)
    with a: years=st.multiselect(tr('Years','Anos'),[2011,2012],default=[2011,2012],key='years')
    with b: days=st.selectbox(tr('Day type','Tipo de dia'),['all','work','off'],format_func=lambda x:{'all':tr('All','Todos'),'work':tr('Working day','Dia útil'),'off':tr('Non-working day','Dia não útil')}[x])
    df=df[df.datetime.dt.year.isin(years)]
    if days!='all': df=df[df.workingday==int(days=='work')]
    if df.empty: st.warning(tr('No observations for these filters.','Nenhuma observação para estes filtros.')); return
    st.metric(tr('Observations','Observações'),fmt(len(df)))
    df=df.copy(); df['year']=df.datetime.dt.year.astype(str); df['day_type']=df.workingday.map({0:tr('Non-working','Não útil'),1:tr('Working','Útil')})
    st.subheader(tr('Hourly profile','Perfil horário'))
    h=df.groupby(['hr','day_type'],as_index=False).cnt.mean()
    show(px.line(h,x='hr',y='cnt',color='day_type',markers=True,color_discrete_sequence=['#22D3EE','#34D399'],labels={'day_type':tr('Day type','Tipo de dia'),'cnt':tr('Mean rentals','Média de aluguéis'),'hr':tr('Hour','Hora')}),tr('Hour','Hora'),tr('Mean rentals','Média de aluguéis'))
    a,b=st.columns(2)
    with a:
        st.subheader(tr('Monthly demand','Demanda mensal'))
        m=df.groupby(['mnth','year'],as_index=False).cnt.mean()
        show(px.line(m,x='mnth',y='cnt',color='year',markers=True,labels={'year':tr('Year','Ano'),'cnt':tr('Mean rentals','Média de aluguéis'),'mnth':tr('Month','Mês')}),tr('Month','Mês'),tr('Mean rentals','Média de aluguéis'))
    with b:
        st.subheader(tr('Weather conditions','Condições climáticas'))
        w=df.groupby('weathersit',as_index=False).cnt.agg(['mean','count']).reset_index(drop=True)
        w['weather']=w.weathersit.astype(str)
        show(px.bar(w,x='weather',y='mean',hover_data=['count'],color_discrete_sequence=['#22D3EE']),tr('Weather category (1–4)','Categoria climática (1–4)'),tr('Mean rentals','Média de aluguéis'))
    st.caption(tr('Descriptive historical associations, not causal effects.','Associações históricas descritivas, não efeitos causais.'))
