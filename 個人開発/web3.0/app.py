import requests
import pandas as pd
import os
# from dotenv import load_dotenv

# .env ファイルの読み込み
# load_dotenv()

# 環境変数の取得
# API_KEY = os.getenv("ETHERSCAN_API_KEY")
API_KEY = os.environ.get("API_KEY")
TOKEN_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDTのコントラクトアドレス



# 取得する取引件数
transactions = 1000

# APIリクエストURL
url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_CONTRACT}&page=1&offset={transactions}&sort=desc&apikey={API_KEY}"

# データ取得
response = requests.get(url)
data = response.json()

# データをDataFrameに変換
df = pd.DataFrame(data['result'])

# 必要なカラムを選択
df = df[['timeStamp', 'from', 'to', 'value', 'tokenSymbol']]

# タイムスタンプを日時変換
df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')

# トークンの値を整数変換（USDTは小数点6桁分シフト）
df['value'] = df['value'].astype(float) / 10**6



# アドレスごとの取引量（送信量＋受信量）
top_senders = df.groupby('from')['value'].sum().reset_index().rename(columns={'from': 'address', 'value': 'sent_value'})
top_receivers = df.groupby('to')['value'].sum().reset_index().rename(columns={'to': 'address', 'value': 'received_value'})

# 送信と受信のデータをマージ
top_addresses = pd.merge(top_senders, top_receivers, on="address", how="outer").fillna(0)

# 合計取引量を算出
top_addresses["total_value"] = top_addresses["sent_value"] + top_addresses["received_value"]

# 取引量の多い順に並び替え
top_addresses = top_addresses.sort_values(by="total_value", ascending=False)



# import matplotlib.pyplot as plt

# 日ごとの取引数を集計
df['date'] = df['timeStamp'].dt.date
# 1時間ごとの取引数を集計
# df['date'] = df['timeStamp'].dt.hour
# 1分ごとの取引数を集計
# df['date'] = df['timeStamp'].dt.minute
daily_transactions = df.groupby('date').size()

# # 可視化
# plt.figure(figsize=(10,5))
# plt.plot(daily_transactions.index, daily_transactions.values, marker='o', linestyle='-')
# plt.xlabel("Date")
# plt.ylabel("Transaction Count")
# plt.title("USDT Daily Transactions")
# plt.xticks(rotation=45)
# plt.grid()
# plt.show()



import streamlit as st

st.title("Ethereum トークン取引分析")

# 最新のデータ取得
st.write("### 最新のUSDT取引データ")
st.dataframe(df.head(10))

# 取引量の多いアドレス
st.write("### 取引量の多いアドレス")
st.dataframe(top_addresses.head(10))

# 日ごとの取引数のグラフ
st.write("### USDTの1日ごとの取引数")
st.line_chart(daily_transactions)

st.write("データソース: Etherscan API")