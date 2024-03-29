import yfinance
import datetime
import pandas as pd
import numpy as np
import streamlit as st

data = {
    '企業名':['ニッスイ', 'INPEX', 'コムシスHD','大成建', '大林組',
           '清水建', '長谷工', '鹿島', 'ハウス', '積ハウス', '日揮HD',
           '日清粉G', '明治HD', '日ハム', 'エムスリー', 'ディーエヌエ',
           'サッポロHD', 'アサヒ', 'キリンHD', '宝HLD', '双日', 'キッコマン',
           '味の素', 'ニチレイ', 'JT', 'Jフロント', '三越伊勢丹', '東急不HD',
           'セブン＆アイ', '帝人', '東レ', 'クラレ', '旭化成', 'SUMCO',
           'ネクソン', '王子HD', '日本紙', 'レゾナック', '住友化', '日産化',
           '東ソー', 'トクヤマ', 'デンカ', '信越化', '協和キリン', '三井化学',
           '三菱ケミG', 'UBE', '電通グループ', 'メルカリ', '花王', '武田',
           'アステラス', '住友ファーマ', '塩野義', '中外薬', 'エーザイ', 'テルモ',
           '第一三共', '大塚HD', 'DIC', 'OLC', 'ラインヤフー', 'トレンド',
           'サイバー', '楽天グループ', '富士フイルム', 'コニカミノル', '資生堂',
           '出光興産', 'ENEOS', '浜ゴム', 'ブリヂストン', 'AGC', '日電硝',
           '住友大阪', '太平洋セメ', '東海カーボン', 'TOTO', 'ガイシ', '日本製鉄',
           '神戸鋼', 'JFE', '大平金', '日製鋼', '三井金', '三菱マ', '住友鉱',
           'DOWA', '古河電', '住友電', 'フジクラ', 'しずおかFG', 'リクルート',
           'オークマ', 'アマダ', '日本郵政', 'SMC', 'コマツ', '住友重', '日立建機',
           'クボタ', '荏原', 'ダイキン', '日精工', 'NTN', 'ジェイテクト', 'ミネベア',
           '日立', '三菱電', '富士電機', '安川電', 'ニデック', 'オムロン',
           'GSユアサ', 'NEC', '富士通', 'ルネサス', 'エプソン', 'パナHD', 'シャープ',
           'ソニーG', 'TDK', 'アルプスアル', '横河電', 'アドテスト', 'キーエンス',
           'デンソー', 'レーザーテク', 'カシオ', 'ファナック', '京セラ', '太陽誘電',
           '村田製', '日東電', '日立造', '三菱重', '川重', 'IHI', 'コンコルディ',
           '日産自', 'いすゞ', 'トヨタ', '日野自', '三菱自', 'マツダ', 'ホンダ',
           'スズキ', 'SUBARU', 'ヤマハ発', 'ニコン', 'オリンパス', 'スクリン',
           'HOYA', 'キヤノン', 'リコー', 'シチズン', 'バンナムHD', 'TOPPAN',
           '大日印', 'ヤマハ', '任天堂', '伊藤忠', '丸紅', '豊田通商', '三井物',
           '東エレク', '住友商', '三菱商', '高島屋', '丸井G', 'クレセゾン',
           'イオン', 'あおぞら銀', '三菱UFJ', 'りそなHD', '三井住友トラ',
           '三井住友FG', '千葉銀', 'ふくおかFG', 'みずほFG', 'オリックス', '大和',
           '野村', 'SOMPO', '日本取引所', 'MS&AD', '第一生命HD', '東京海上',
           'T&D', '三井不', '菱地所', '東建物', '住友不', '東武', '東急', '小田急',
           '京王', '京成', 'JR東日本', 'JR西日本', 'JR東海', 'ヤマトHD', '郵船',
           '商船三井', '川崎汽', 'NXHD', 'JAL', 'ANAHD', '三菱倉', 'NTT', 'KDDI',
           'SB', '東電HD', '中部電', '関西電', '東ガス', '大ガス', '東宝',
           'NTTデータ', 'セコム', 'コナミG', 'ニトリHD', 'ファストリ', 'SBG',
    ],
    '産業':['水産', '鉱業', '建設', '建設', '建設', '建設', '建設', '建設', '建設',
          '建設', '建設', '食品', '食品', '食品', 'サービス', 'サービス', '食品',
          '食品', '食品', '食品', '商社', '食品', '食品', '食品', '食品', '小売業',
          '小売業', '不動産', '小売業', '繊維', '繊維', '化学', '化学', '非鉄金属製品',
          'サービス', 'パルプ・紙', 'パルプ・紙', '化学', '化学', '化学', '化学',
          '化学', '化学', '化学', '医薬品', '化学', '化学', '化学', 'サービス',
          'サービス', '化学', '医薬品', '医薬品', '医薬品', '医薬品', '医薬品',
          '医薬品', '精密機器', '医薬品', '医薬品', '化学', 'サービス', 'サービス',
          'サービス', 'サービス', 'サービス', '化学', '精密機器', '化学', '石油',
          '石油', 'ゴム', 'ゴム', '窯業', '窯業', '窯業', '窯業', '窯業', '窯業',
          '窯業', '鉄鋼', '鉄鋼', '鉄鋼', '鉄鋼', '機械', '非鉄金属製品', 
          '非鉄金属製品', '非鉄金属製品', '非鉄金属製品', '非鉄金属製品', 
          '非鉄金属製品', '非鉄金属製品', '銀行', 'サービス', '機械', '機械',
          'サービス', '機械', '機械', '機械', '機械', '機械', '機械', '機械', '機械',
          '機械', '機械', '電気機器', '電気機器', '電気機器', '電気機器', '電気機器',
          '電気機器', '電気機器', '電気機器', '電気機器', '電気機器', '電気機器',
          '電気機器', '電気機器', '電気機器', '電気機器', '電気機器', '電気機器',
          '電気機器', '電気機器', '電気機器', '電気機器', '電気機器', '電気機器',
          '電気機器', '電気機器', '電気機器', '電気機器', '化学', '機械', '機械',
          '造船', '機械', '銀行', '自動車', '自動車', '自動車', '自動車', '自動車',
          '自動車', '自動車', '自動車', '自動車', '自動車', '精密機器', '精密機器',
          '電気機器', '精密機器', '電気機器', '電気機器', '精密機器', 'その他製造',
          'その他製造', 'その他製造', 'その他製造', 'サービス', '商社', '商社',
          '商社', '商社', '電気機器', '商社', '商社', '小売業', '小売業', 'その他金融',
          '小売業', '銀行', '銀行', '銀行', '銀行', '銀行', '銀行', '銀行', '銀行',
          'その他金融', '証券', '証券', '保険', 'その他金融', '保険', '保険', '保険',
          '保険', '不動産', '不動産', '不動産', '不動産', '鉄道・バス', '鉄道・バス',
          '鉄道・バス', '鉄道・バス', '鉄道・バス', '鉄道・バス', '鉄道・バス',
          '鉄道・バス', '陸運', '海運', '海運', '海運', '陸運', '空運', '空運',
          '倉庫', '通信', '通信', '通信', '電力', '電力', '電力', 'ガス', 'ガス',
          'サービス', '通信', 'サービス', 'サービス', '小売業', '小売業', '通信'
          ],
    '証券コード':[1332, 1605, 1721, 1801,	1802, 1803, 1808, 1812 ,1925 ,1928,
             1963, 2002, 2269, 2282, 2413, 2432, 2501, 2502, 2503, 2531, 2768,
             2801, 2802, 2871, 2914, 3086, 3099, 3289, 3382, 3401, 3402, 3405,
             3407, 3436, 3659, 3861, 3863, 4004, 4005, 4021, 4042, 4043, 4061,
             4063, 4151, 4183, 4188, 4208, 4324, 4385, 4452, 4502, 4503, 4506,
             4507, 4519, 4523, 4543, 4568, 4578, 4631, 4661, 4689, 4704, 4751,
             4755, 4901, 4902, 4911, 5019, 5020, 5101, 5108, 5201, 5214, 5232,
             5233, 5301, 5332, 5333, 5401, 5406, 5411, 5541, 5631, 5706, 5711,
             5713, 5714, 5801, 5802, 5803, 5831, 6098, 6103, 6113, 6178, 6273,
             6301, 6302, 6305, 6326, 6361, 6367, 6471, 6472, 6473, 6479, 6501,
             6503, 6504, 6506, 6594, 6645, 6674,	6701, 6702, 6723, 6724, 6752,
             6753, 6758, 6762, 6770, 6841, 6857, 6861, 6902, 6920, 6952, 6954,
             6971, 6976, 6981, 6988, 7004, 7011, 7012, 7013, 7186, 7201, 7202,
             7203, 7205, 7211, 7261, 7267, 7269, 7270, 7272, 7731, 7733, 7735,
             7741, 7751, 7752, 7762, 7832, 7911, 7912, 7951, 7974, 8001, 8002,
             8015, 8031, 8035, 8053, 8058, 8233, 8252, 8253, 8267, 8304, 8306,
             8308, 8309, 8316, 8331, 8354, 8411, 8591, 8601, 8604, 8630, 8697,
             8725, 8750, 8766, 8795, 8801, 8802, 8804, 8830, 9001, 9005, 9007,
             9008, 9009, 9020, 9021, 9022, 9064, 9101, 9104, 9107, 9147, 9201,
             9202, 9301, 9432, 9433, 9434, 9501, 9502, 9503, 9531, 9532, 9602,
             9613, 9735, 9766, 9843, 9983, 9984]
}

cor = pd.DataFrame(data)

df = pd.DataFrame(columns=cor['企業名'])

for i in cor['証券コード']:
    symbol = str(i)+'.T'
    period = "2d"

    Ticker = yfinance.Ticker(symbol)
    df_data = Ticker.history(period=period)
    ind = cor[cor['証券コード'] == i].index
    df.iloc[:,int(ind.values)] = df_data['Close']
    
df_change = pd.DataFrame(index=cor['企業名'], columns=['産業','変化額','変化率'])

for index, row in df_change.iterrows():
    if index in cor['企業名'].values:
        corresponding_industry = cor.loc[cor['企業名'] == index, '産業'].values[0]
        df_change.at[index, '産業'] = corresponding_industry
    df_change.at[index, '変化額'] = df[index].iloc[-2:,].values[1] - df[index].iloc[-2:,].values[0]
    df_change.at[index, '変化率'] = df[index].iloc[-2:,].values[1] / df[index].iloc[-2:,].values[0]

df_change = df_change.sort_values(by='変化額', ascending=False)

st.title('日経平均株価')
st.dataframe(df_change)