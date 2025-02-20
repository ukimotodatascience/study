import yfinance
import streamlit as st
import pandas as pd

def input(symbol):
    brand = symbol
    period = 'max'
    
    Ticker = yfinance.Ticker(brand)
    df = Ticker.history(period=period)
    return df

df_microsoft = input('MSFT')
df_amazon = input('AMZN')
df_meta = input('META')
df_google = input('GOOG')
df_apple = input('AAPL')
df_nvidia = input('NVDA')
df_tesla = input('TSLA')

# st.dataframe(df_microsoft)

line_chart_data = pd.DataFrame(
    {
        'Microsoft': df_microsoft['Close'],
        'Amazon': df_amazon['Close'],
        'Meta': df_meta['Close'],
        'Google': df_google['Close'],
        'Apple': df_apple['Close'],
        'NVIDIA': df_nvidia['Close'],
        'tesla': df_tesla['Close']
    }
)

# 折れ線グラフ
line_chart_data.index = pd.to_datetime(line_chart_data.index)
line_chart_data.index = line_chart_data.index.strftime('%Y-%m-%d')
latest_date = line_chart_data.index.max()
latest_date = pd.to_datetime(latest_date)

st.title('マグニフィセントセブンの株価')
term = st.selectbox('期間', ['全期間', '1週間', '1カ月', '6カ月', '1年', '10年'])
if term == '全期間':
    st.line_chart(line_chart_data)
elif term == '1週間':
    st.line_chart(line_chart_data[line_chart_data.index >= str(latest_date - pd.DateOffset(weeks=1))])
elif term == '1カ月':
    st.line_chart(line_chart_data[line_chart_data.index >= str(latest_date - pd.DateOffset(months=1))])
elif term == '6カ月':
    st.line_chart(line_chart_data[line_chart_data.index >= str(latest_date - pd.DateOffset(months=6))])
elif term == '1年':
    st.line_chart(line_chart_data[line_chart_data.index >= str(latest_date - pd.DateOffset(years=1))])
elif term == '10年':
    st.line_chart(line_chart_data[line_chart_data.index >= str(latest_date - pd.DateOffset(years=10))])
