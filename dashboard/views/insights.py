import streamlit as st
from dashboard.i18n import tr, format_number as fmt
from dashboard.services.data_service import load_dataset, load_evaluation_metrics


def render_summary(df):
    annual = df.groupby(df.datetime.dt.year).cnt.mean()
    growth = (annual.loc[2012] / annual.loc[2011] - 1) * 100
    st.subheader(tr('Executive summary', 'Resumo executivo'))
    st.write(tr(
        f'Average hourly demand rose from {fmt(annual.loc[2011], 2)} in 2011 to {fmt(annual.loc[2012], 2)} in 2012 ({fmt(growth, 1)}%). Demand also varies by hour, season and weather. These historical patterns can inform operational planning.',
        f'A demanda média por hora passou de {fmt(annual.loc[2011], 2)} em 2011 para {fmt(annual.loc[2012], 2)} em 2012 ({fmt(growth, 1)}%). A demanda também varia por horário, estação e clima. Esses padrões históricos podem orientar o planejamento operacional.'
    ))


def render_insights():
    df = load_dataset()
    st.title(tr('Beyond the Numbers', 'Além dos números'))
    st.caption(tr('Full historical dataset · 2011–2012', 'Dataset histórico completo · 2011–2012'))
    render_summary(df)
    months = df.groupby('mnth').cnt.mean()
    seasons = df.groupby('season').cnt.mean()
    work = df[df.workingday == 1].groupby('hr').cnt.mean()
    off = df[df.workingday == 0].groupby('hr').cnt.mean()
    weather = df.groupby('weathersit').cnt.agg(['mean','count'])
    names = tr('January February March April May June July August September October November December','Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro').split()
    month = names[int(months.idxmax())-1]
    st.divider()
    sections = [
        (tr('Monthly seasonality','Sazonalidade mensal'), tr(f'{month} had the highest hourly mean ({fmt(months.max(), 2)} rentals). Season category {seasons.idxmax()} led with {fmt(seasons.max(), 2)} rentals per hour.', f'{month} apresentou a maior média horária ({fmt(months.max(), 2)} aluguéis). A categoria de estação {seasons.idxmax()} liderou com {fmt(seasons.max(), 2)} aluguéis por hora.'), tr('Plan capacity and maintenance around historical demand patterns.','Planejar capacidade e manutenção considerando os padrões históricos de demanda.')),
        (tr('Daily mobility','Mobilidade diária'), tr(f'Working days peak at {int(work.idxmax()):02d}:00 ({fmt(work.max(), 2)} rentals/hour); non-working days peak at {int(off.idxmax()):02d}:00 ({fmt(off.max(), 2)}).',f'Dias úteis atingem o pico às {int(work.idxmax()):02d}h ({fmt(work.max(), 2)} aluguéis/hora); dias não úteis, às {int(off.idxmax()):02d}h ({fmt(off.max(), 2)}).'),tr('Consider different bicycle availability schedules for working and non-working days.','Considerar estratégias diferentes de disponibilidade de bicicletas em dias úteis e não úteis.')),
        (tr('Weather and demand','Clima e demanda'),tr(f'Weather category 1 averaged {fmt(weather.loc[1,"mean"],2)} rentals/hour versus {fmt(weather.loc[3,"mean"],2)} in category 3. Category 4 has only {fmt(weather.loc[4,"count"])} observations.',f'A categoria climática 1 teve média de {fmt(weather.loc[1,"mean"],2)} aluguéis/hora, contra {fmt(weather.loc[3,"mean"],2)} na categoria 3. A categoria 4 possui apenas {fmt(weather.loc[4,"count"])} observações.'),tr('Use weather information cautiously when planning capacity.','Usar informações climáticas com cautela no planejamento de capacidade.')),
    ]
    for title, finding, implication in sections:
        with st.container(border=True):
            st.subheader(title)
            st.write(finding)
            st.markdown('**'+tr('Potential operational implication','Possível implicação operacional')+'**')
            st.write(implication)
    m=load_evaluation_metrics(); test=m[m.Conjunto=='Teste'].set_index('Modelo'); model=test.loc['Gradient Boosting']; base=test.loc['Baseline']
    with st.container(border=True):
        st.subheader(tr('Predictive performance','Desempenho preditivo'))
        st.write(tr(f'Test MAE was {fmt(model.MAE,2)} rentals/hour, a {fmt(100*(1-model.MAE/base.MAE),2)}% reduction versus the baseline. R² was {fmt(model.R2,4)}.',f'O MAE de teste foi de {fmt(model.MAE,2)} aluguéis/hora, uma redução de {fmt(100*(1-model.MAE/base.MAE),2)}% em relação ao baseline. O R² foi de {fmt(model.R2,4)}.'))
    st.caption(tr('Historical descriptive associations, not causal evidence or current forecasts. Operational benefits have not been validated.','Associações históricas descritivas, não evidências causais nem previsões atuais. Os benefícios operacionais não foram validados.'))
