import streamlit as st

def show(fig, x=None, y=None):
    fig.update_layout(template='plotly_dark',paper_bgcolor='#111B2B',plot_bgcolor='#111B2B',font_color='#F1F5F9',margin=dict(l=20,r=20,t=45,b=20),height=340,legend=dict(orientation='h',y=1.12),xaxis_title=x,yaxis_title=y)
    fig.update_xaxes(gridcolor='#243247')
    fig.update_yaxes(gridcolor='#243247')
    st.plotly_chart(fig,width='stretch',theme=None,config={'displaylogo':False})
