import streamlit as st
from datetime import datetime
import pandas as pd
from functions import request_alphavantage
from functions import plot_candles_stick_bar
from contact import contact_form

@st.cache_data
def fetch_symbol_search(keywords):
    json_data = request_alphavantage(
        function='SYMBOL_SEARCH',
        keywords=keywords,
        apike=API_KEY
    ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.cache_data
def fetch_time_series_daily(ticker):
    json_data = request_alphavantage(
        function='TIME_SERIES_DAILY',
        symbol=ticker,
        outputsize='compact', # compact returns only the latest 100 data points
        datatype='json'
        ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.cache_data
def fetch_splits_events(ticker):
    json_data = request_alphavantage(
        function='SPLITS',
        symbol=ticker,
        ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.cache_data
def fetch_overview(ticker):
    json_data = request_alphavantage(
        function='OVERVIEW',
        symbol=ticker,
        ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.cache_data
def fetch_etf_profile(ticker):
    json_data = request_alphavantage(
        function='ETF_PROFILE',
        symbol=ticker,
        ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.cache_data
def fetch_quote_endpoint(ticker):
    json_data = request_alphavantage(
        function='GLOBAL_QUOTE',
        symbol=ticker,
        ).json()
    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()
    return json_data

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

st.set_page_config(
    page_title="Stock", # The page title, shown in the browser tab.
    page_icon=":chart:", # The page favicon.
    layout="wide", # How the page content should be laid out.
    initial_sidebar_state="auto", # How the sidebar should start out.
    menu_items={ # Configure the menu that appears on the top-right side of this app.
        "Get help": "https://github.com/LMAPcoder" # The URL this menu item should point to.
    }
)

API_KEY = st.secrets["API_KEY"]




# ---- SIDEBAR ----
with st.sidebar:

    KEYWORD = st.text_input(
        label="Security",
        value='MSFT',
        placeholder="Input security ticker"
    )
    st.write("eg: MSFT, QQQ, SPY")
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

    button = st.button("✉️ Contact Me", key="contact")

    if button:
        show_contact_form()



# ---- MAINPAGE ----


#----FIRST SECTION----
st.title("Stock Market")

col1, col2 = st.columns([0.7, 0.3], gap="medium")

col1.header("Global Markets Status")

button = col1.button("Refresh", key="refresh_mkt_status")
if button:
    del st.session_state['market_status']

if "market_status" not in st.session_state:

    json_data = request_alphavantage(
        function='MARKET_STATUS',
        apike=API_KEY
    ).json()

    if "Information" in json_data:
        st.warning(json_data['Information'])
        st.stop()

    st.session_state.market_status = json_data
    now = datetime.now()
    col1.write(f'Latest update: {now.strftime("%Y-%m-%d %H:%M")}')

df = pd.DataFrame(st.session_state.market_status['markets']).drop(columns=['notes'])

col1.dataframe(
    data=df,
    hide_index=True
)

col2.header("Search Endpoint")

KEYWORDS = col2.text_input(
    label="Search box",
    value=None,
    placeholder="Enter security name"
)

if KEYWORDS:
    json_data = fetch_symbol_search(KEYWORDS)

    df = pd.DataFrame(json_data['bestMatches'])

    col2.dataframe(
        data=df[['1. symbol', '2. name', '3. type', '4. region']],
        hide_index=True
    )


#----SECOND SECTION----

json_data = fetch_symbol_search(KEYWORD)

TICKER = json_data['bestMatches'][0]['1. symbol']
TYPE = json_data['bestMatches'][0]['3. type']
NAME = json_data['bestMatches'][0]['2. name']

st.header(f"Stock: {TICKER}")
st.write(NAME)

button = st.button("Refresh", key="refresh_security")
if button:
    fetch_quote_endpoint.clear()
    fetch_time_series_daily.clear()

#----INFORMATION----
with st.expander("More info"):
    if TYPE == "Equity":
        json_data = fetch_overview(TICKER)
        data = {
            'Country': json_data['Country'],
            'Market Exchange': json_data['Exchange'],
            'Sector': json_data['Sector'],
            'Industry': json_data['Industry'],
            'Market Capitalization': json_data['MarketCapitalization'],
            'EBITDA': json_data['EBITDA'],
            'Beta': json_data['Beta']
        }
        df = pd.DataFrame([data]).T
        df.index.name = 'Feature'
        st.dataframe(
            data=df.reset_index(),
            hide_index=True
        )
        #st.write(json_data)
    elif TYPE == "ETF":

        col1, col2, col3 = st.columns([0.3, 0.3, 0.4], gap="small")

        json_data = fetch_etf_profile(TICKER)
        data = {
            'Net Assets': json_data['net_assets'],
            'Net Expense Ratio': json_data['net_expense_ratio'],
            'Portfolio Turnover ': json_data['portfolio_turnover'],
            'Dividend Yield': json_data['dividend_yield'],
            'Inception Date': json_data['inception_date'],
            'Allocation: Domestic Equities': json_data['asset_allocation']['domestic_equities'],
            'Allocation: Foreign Equities': json_data['asset_allocation']['foreign_equities'],
            'Allocation: Bonds': json_data['asset_allocation']['bond'],
            'Allocation: Cash': json_data['asset_allocation']['cash'],
            'Allocation: Other': json_data['asset_allocation']['other']
        }
        df = pd.DataFrame([data]).T
        col1.dataframe(
            data=df.reset_index(),
            use_container_width=True,
            hide_index=True
        )
        df = pd.DataFrame(json_data['sectors'])
        col2.dataframe(
            data=df,
            hide_index=True
        )
        #st.write(json_data)

#----METRICS----

json_data = fetch_quote_endpoint(TICKER)
data = json_data['Global Quote']
PRICE = float(data['05. price'])
CHANGE = float(data['09. change'])
CHANGE_PER = float(data['10. change percent'].strip('%'))
HIGH = float(data['03. high'])
LOW = float(data['04. low'])
VOLUME = int(data['06. volume'])
LATEST_DATE = data['07. latest trading day']

st.metric(
    "Latest Price",
    value=f'{PRICE:.1f} USD',
    delta=f'{CHANGE:.1f} ({CHANGE_PER:.2f}%)'
    )


col1, col2, col3 = st.columns(3, gap="medium")

col1.metric(
    "High",
    value=f'{HIGH:.1f} USD'
    )

col2.metric(
    "Low",
    value=f'{LOW:.1f} USD'
)

col3.metric(
    "Volume",
    value=f'{VOLUME}'
)

st.write("Latest update:", LATEST_DATE)

#----CANDLESTICK CHART----
json_data = fetch_time_series_daily(TICKER)

meta_data = json_data['Meta Data']
CHART = meta_data['1. Information']
TITLE = f'{CHART}: {TICKER}'

df_dts = pd.DataFrame(json_data['Time Series (Daily)']).T
df_dts.columns = [col.split('. ', 1)[1] for col in df_dts.columns]
df_dts.index.name = 'date'
df_dts.reset_index(inplace=True)

if "SMA" in INDICATORS:
    df_dts['SMA'] = df_dts['close'].rolling(window=TIME_SPAN, min_periods=1).mean()
if "EMA" in INDICATORS:
    df_dts['EMA'] = df_dts['close'].ewm(span=TIME_SPAN, adjust=False, min_periods=1).mean()

fig = plot_candles_stick_bar(df_dts, TITLE, TIME_SPAN)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Show data"):

    json_data = fetch_splits_events(TICKER)
    df_splits = pd.DataFrame(json_data['data'])

    col1, col2 = st.columns([0.6, 0.4], gap="medium")

    col1.markdown("Daily prices")
    col1.dataframe(
        data=df_dts,
        hide_index=False
    )

    col2.markdown("Historical split events")
    col2.dataframe(
        data=df_splits,
        hide_index=True
    )

