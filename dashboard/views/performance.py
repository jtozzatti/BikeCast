import streamlit as st
import plotly.express as px
from dashboard.i18n import tr,format_number as fmt
from dashboard.services.data_service import load_evaluation_metrics,load_test_predictions,read_csv
from dashboard.components.charts import show

def render_performance():
    st.title(tr('Model Performance','Desempenho do modelo'))
    m=load_evaluation_metrics(); test=m[(m.Conjunto=='Teste') & (m.Modelo=='Gradient Boosting')].iloc[0]
    for col,k in zip(st.columns(3),['MAE','RMSE','R2']):
        with col: st.metric('R²' if k=='R2' else k,fmt(test[k],4 if k=='R2' else 2))
    df=load_test_predictions(); n=st.slider(tr('Days from test start','Dias desde o início do teste'),1,30,7)
    subset=df[df.datetime<df.datetime.min()+__import__('pandas').Timedelta(days=n)].rename(columns={'real':tr('Actual','Real'),'previsto':tr('Predicted','Previsto')})
    st.subheader(tr('Actual vs predicted','Real vs previsto'))
    show(px.line(subset,x='datetime',y=[tr('Actual','Real'),tr('Predicted','Previsto')],color_discrete_sequence=['#22D3EE','#34D399']),tr('Date','Data'),tr('Rentals','Aluguéis'))
    a,b=st.columns(2)
    with a:
        st.subheader(tr('Residual distribution','Distribuição dos resíduos'))
        show(px.histogram(df,x='residuo',nbins=50,color_discrete_sequence=['#22D3EE']),tr('Actual − predicted','Real − previsto'),tr('Count','Contagem'))
    with b:
        st.subheader(tr('Error by hour','Erro por hora'))
        h=df.groupby('hr',as_index=False).erro_absoluto.mean()
        show(px.bar(h,x='hr',y='erro_absoluto',color_discrete_sequence=['#34D399']),tr('Hour','Hora'),'MAE')
    st.subheader(tr('Evaluation results','Resultados da avaliação'))
    st.dataframe(m.rename(columns={'Conjunto':tr('Split','Conjunto'),'Modelo':tr('Model','Modelo')}),hide_index=True,width='stretch')
    st.caption(tr('Chronological held-out test. R² is not classification accuracy.','Teste cronológico separado. R² não é acurácia de classificação.'))
