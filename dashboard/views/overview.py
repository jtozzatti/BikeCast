import streamlit as st
import plotly.express as px
from dashboard.i18n import tr,format_number as fmt
from dashboard.components.metrics import render_metric
from dashboard.views.insights import render_summary
from dashboard.components.charts import show
from dashboard.services.data_service import load_dataset,load_evaluation_metrics,load_modeling_results

def render_overview():
    df=load_dataset(); m=load_evaluation_metrics(); test=m[m.Conjunto=='Teste'].set_index('Modelo'); model=test.loc['Gradient Boosting']; base=test.loc['Baseline']
    st.title(tr('Demand Intelligence','Inteligência de demanda'))
    st.caption(tr('Historical bicycle sharing · 2011–2012','Compartilhamento de bicicletas · 2011–2012'))
    for col,(label,value,desc) in zip(st.columns(4),[(tr('Historical records','Registros históricos'),fmt(len(df)),tr('Hourly observations','Observações por hora')),('R²',fmt(model.R2,4),tr('Test set','Conjunto de teste')),('MAE',fmt(model.MAE,2),tr('Rentals per hour','Aluguéis por hora')),(tr('MAE reduction','Redução do MAE'),fmt(100*(1-model.MAE/base.MAE),2)+'%',tr('Against test baseline','Contra baseline de teste'))]):
        with col: render_metric(label,value,desc)
    st.divider()
    a,b=st.columns(2)
    with a:
        st.subheader(tr('Hourly demand','Demanda por hora'))
        hourly=df.groupby('hr',as_index=False).cnt.mean()
        show(px.line(hourly,x='hr',y='cnt',markers=True,color_discrete_sequence=['#22D3EE']),tr('Hour','Hora'),tr('Mean rentals','Média de aluguéis'))
    with b:
        st.subheader(tr('Model comparison','Comparação de modelos'))
        results=load_modeling_results().sort_values('MAE').drop_duplicates('Modelo').sort_values('MAE',ascending=False)
        results['Model']=results.Modelo.replace({'Regressão Linear':tr('Linear Regression','Regressão Linear')})
        show(px.bar(results,x='MAE',y='Model',orientation='h',color_discrete_sequence=['#22D3EE']), 'MAE',None)
        st.caption(tr('Best configuration per model on validation data. Lower is better.','Melhor configuração por modelo na validação. Menor é melhor.'))
    st.info(tr('Explore historical patterns, simulate demand and inspect held-out test results using the navigation menu.','Explore padrões históricos, simule demanda e examine resultados de teste pelo menu lateral.'))

    st.divider()
    render_summary(df)
