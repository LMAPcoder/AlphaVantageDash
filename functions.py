import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def request_alphavantage(**kwargs):
    params = {
        'function': 'TIME_SERIES_INTRADAY', # The time series of your choice.
        'apikey': 'XXX' # Your API key
        }

    params.update(kwargs)

    try:

        response = requests.get('https://www.alphavantage.co/query', params=params)

        return response

    except:

        return None

def plot_candles_stick_bar(df, title="", time_span=None):

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01,
                        subplot_titles=None,
                        row_heights=[0.7, 0.3])


    fig.add_trace(go.Candlestick(x=df['date'].to_numpy(),
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name="OHVC"),
                  row=1, col=1)

    if 'SMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['SMA'],
                                 mode='lines',
                                 line=dict(color='black', width=2),
                                 name=f'{time_span}SMA'),
                      row=1, col=1)
    if 'EMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['EMA'],
                                 mode='lines',
                                 line=dict(color='blue', width=2),
                                 name=f'{time_span}EMA'),
                      row=1, col=1)

    if 'volume' in df.columns:
        fig.add_trace(go.Bar(x=df['date'].to_numpy(),
                             y=df['volume'],
                             name='Volume',
                             marker_color='rgba(0, 0, 255, 0.2)'),
                      row=2, col=1)

    fig.update_layout(
        title=title,
        # xaxis_title='Date',
        yaxis_title='Price',
        xaxis2_title='Date',
        yaxis2_title='Volume',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.3,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    return fig


def plot_candles_stick(df, title="", time_span=None):

    fig = go.Figure()


    fig.add_trace(go.Candlestick(x=df['date'].to_numpy(),
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name="OHVC")
                  )

    if 'SMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['SMA'],
                                 mode='lines',
                                 line=dict(color='black', width=2),
                                 name=f'{time_span}SMA')
                      )
    if 'EMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['EMA'],
                                 mode='lines',
                                 line=dict(color='blue', width=2),
                                 name=f'{time_span}EMA')
                      )

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.3,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    return fig


def plot_line_chart(df, title="", time_span=None):
    # Create a candlestick chart using Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                             y=df['value'],
                             mode='lines',
                             line=dict(color='green', width=2),
                             name='Value'))

    if 'SMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['SMA'],
                                 mode='lines',
                                 line=dict(color='black', width=2),
                                 name=f'{time_span}SMA')
                      )
    if 'EMA' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'].to_numpy(),
                                 y=df['EMA'],
                                 mode='lines',
                                 line=dict(color='blue', width=2),
                                 name=f'{time_span}EMA')
                      )

    # Update layout to add titles and formatting
    fig.update_layout(
        title=title,
        xaxis=dict(
            tickmode='linear',
            dtick="M1",  # Set ticks to show every month
            tickformat="%b %Y",  # Format ticks to show Month and Year (e.g., Jan 2023)
        ),
        xaxis_title='Date',
        yaxis_title='Price',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.6,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        height=600,
        xaxis_rangeslider_visible=True  # Remove range slider (optional)
    )

    return fig