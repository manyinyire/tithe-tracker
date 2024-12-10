import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_income_distribution_chart(income_data):
    df = pd.DataFrame(income_data)
    fig = px.pie(
        df,
        values='total',
        names='source',
        title='Income Distribution by Source',
        color_discrete_sequence=px.colors.sequential.Purples,
        hole=0.4
    )
    fig.update_layout(
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_tithe_progress_chart(tithe_due, tithe_paid):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=tithe_paid,
        delta={'reference': tithe_due},
        title={'text': "Tithe Progress"},
        gauge={
            'axis': {'range': [None, tithe_due * 1.2]},
            'bar': {'color': "#6B46C1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, tithe_due], 'color': 'rgba(107, 70, 193, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        font={'color': "#2D3748", 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    return fig
