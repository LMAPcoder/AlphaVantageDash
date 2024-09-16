import streamlit as st
import pandas as pd
from functions import request_alphavantage
from functions import plot_line_chart

@st.cache_data
def fetch_commodity(comm, interval="monthly"):
    json_data = request_alphavantage(
        function=comm,
        interval=interval
    ).json()
    return json_data


st.set_page_config(
    page_title="Commodities", # The page title, shown in the browser tab.
    page_icon=":mountain:", # The page favicon.
    layout="wide", # How the page content should be laid out.
    initial_sidebar_state="auto", # How the sidebar should start out.
    menu_items={ # Configure the menu that appears on the top-right side of this app.
        "Get help": "https://github.com/LMAPcoder" # The URL this menu item should point to.
    }
)

# ---- SIDEBAR ----
with st.sidebar:
    commodities = {
        'West Texas Intermediate': 'WTI',
        'Brent': 'BRENT',
        'Natural Gas': 'NATURAL_GAS',
        'Copper': 'COPPER',
        'Aluminum': 'ALUMINUM',
        'Wheat': 'WHEAT',
        'Corn': 'CORN',
        'Cotton': 'COTTON',
        'Sugar': 'SUGAR',
        'Coffee': 'COFFEE'
    }

    option = st.selectbox(
        label="Commodity",
        options=list(commodities.keys()),
        index=0,
        placeholder="Select commodity...",
    )

    COMMODITY = commodities[option]

    st.write(COMMODITY)

    PERIODS = st.slider(
        label="Select number of months:",
        min_value=1,  # The minimum permitted value.
        max_value=100,  # The maximum permitted value.
        value=24  # The value of the slider when it first renders.
    )

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

st.title("Commodity Market")

json_data = fetch_commodity(COMMODITY)
data = json_data['data']

st.write("Latest month:", data[0]['date'])

df = pd.DataFrame(data)[:PERIODS]

CHART = json_data['name']
TITLE = f'{CHART}'

if "SMA" in INDICATORS:
    df['SMA'] = df['value'].rolling(window=TIME_SPAN, min_periods=1).mean()
if "EMA" in INDICATORS:
    df['EMA'] = df['value'].ewm(span=TIME_SPAN, adjust=False, min_periods=1).mean()

fig = plot_line_chart(df, TITLE, TIME_SPAN)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Show data"):
    st.dataframe(df)