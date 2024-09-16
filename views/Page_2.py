import streamlit as st
import pandas as pd
from functions import request_alphavantage
from functions import plot_candles_stick

@st.cache_data
def fetch_fx_daily(sym_1, sym_2):
    json_data = request_alphavantage(
        function='FX_DAILY',
        from_symbol=sym_1,
        to_symbol=sym_2
    ).json()
    return json_data

@st.cache_data
def fetch_fx_now(sym_1, sym_2):
    json_data = request_alphavantage(
        function='CURRENCY_EXCHANGE_RATE',
        from_currency=sym_1,
        to_currency=sym_2
    ).json()
    return json_data

@st.cache_data
def fetch_fxd_daily(sym_1, sym_2):
    json_data = request_alphavantage(
        function='DIGITAL_CURRENCY_DAILY',
        symbol=sym_1,
        market=sym_2
    ).json()
    return json_data


st.set_page_config(
    page_title="Forex", # The page title, shown in the browser tab.
    page_icon=":moneybag:", # The page favicon.
    layout="wide", # How the page content should be laid out.
    initial_sidebar_state="auto", # How the sidebar should start out.
    menu_items={ # Configure the menu that appears on the top-right side of this app.
        "Get help": "https://github.com/LMAPcoder" # The URL this menu item should point to.
    }
)


# ---- SIDEBAR ----
with st.sidebar:

    currencies_1 = {
        'United States Dollar': 'USD',
        'Euro': 'EUR',
        'Japanese Yen': 'JPY',
        'British Pound Sterling': 'GBP',
        'Chinese Yuan': 'CNY',
        'Argentine Peso': 'ARS',
        'Bitcoin': 'BTC',
        'Ethereum': 'ETH',
        'Tether': 'USDT'
    }
    currencies_2 = {
        'United States Dollar': 'USD',
        'Euro': 'EUR',
        'Japanese Yen': 'JPY',
        'British Pound Sterling': 'GBP',
        'Chinese Yuan': 'CNY',
        'Argentine Peso': 'ARS'
    }

    option1 = st.selectbox(
        label="Base currency",
        options=list(currencies_1.keys()),
        index=0,
        placeholder="Select origin currency...",
    )

    CURRENCY_1 = currencies_1[option1]

    st.write(CURRENCY_1)

    if option1 in currencies_2:
        currencies_2.pop(option1)

    option2 = st.selectbox(
        label="Counter currency",
        options=list(currencies_2.keys()),
        index=0,
        placeholder="Select destination currency...",
    )

    CURRENCY_2 = currencies_2[option2]

    st.write(currencies_2[option2])

    INDICATORS = st.multiselect(
        label="Technical indicators:",
        options=['SMA', 'EMA']
    )
    TIME_SPAN = None
    if INDICATORS:
        TIME_SPAN = st.slider(
            label="Select time span:",
            min_value=1,  # The minimum permitted value.
            max_value=20,  # The maximum permitted value.
            value=10  # The value of the slider when it first renders.
        )

    st.sidebar.markdown("Made with ❤️ by Leonardo")


# ---- MAINPAGE ----

st.title("Forex Market")

col1, col2, col3 = st.columns(3, gap="medium")

json_data = fetch_fx_now(CURRENCY_1, CURRENCY_2)


EXCHANGE_RATE = float(json_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
BID_PRICE = float(json_data['Realtime Currency Exchange Rate']['8. Bid Price'])
ASK_PRICE = float(json_data['Realtime Currency Exchange Rate']['9. Ask Price'])
LAST_REFRESHED = json_data['Realtime Currency Exchange Rate']['6. Last Refreshed']

col1.metric(
    "Exchange Rate",
    value=f'{EXCHANGE_RATE:.4f}'
    )

col2.metric(
    "Bid Price",
    value=f'{BID_PRICE:.4f}'
)

col3.metric(
    "Ask Price",
    value=f'{ASK_PRICE:.4f}'
)

st.write("Latest update:", LAST_REFRESHED)

if CURRENCY_1 in ["BTC", "ETH", "USDT"]:
    json_data = fetch_fxd_daily(CURRENCY_1, CURRENCY_2)
    df = pd.DataFrame(json_data['Time Series (Digital Currency Daily)']).T[:100]
else:
    json_data = fetch_fx_daily(CURRENCY_1, CURRENCY_2)
    df = pd.DataFrame(json_data['Time Series FX (Daily)']).T

meta_data = json_data['Meta Data']
CHART = meta_data['1. Information']
TITLE = f'{CHART}: {CURRENCY_1}/{CURRENCY_2}'

df.columns = [col.split('. ', 1)[1] for col in df.columns]
df.index.name = 'date'
df.reset_index(inplace=True)

if "SMA" in INDICATORS:
    df['SMA'] = df['close'].rolling(window=TIME_SPAN, min_periods=1).mean()
if "EMA" in INDICATORS:
    df['EMA'] = df['close'].ewm(span=TIME_SPAN, adjust=False, min_periods=1).mean()

fig = plot_candles_stick(df, TITLE, TIME_SPAN)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Show data"):
    st.dataframe(df)