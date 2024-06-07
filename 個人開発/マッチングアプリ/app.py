import streamlit as st
import pandas as pd
import numpy as np        
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import schedule
import time
import threading

def job():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_COPE)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SP_SHEET_KEY)
    worksheet = sh.worksheet(SP_SHEET)
    df = worksheet.get_all_values()

# スケジュールを設定
schedule.every().day.at("09:00").do(job)

def schedule_job():
    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

df = df.drop('Unnamed: 0', axis=1)

st.title('キャリツクマッチング')
st.caption('これはキャリツク生の共通点を見つけるためのアプリです')

df_ = df.copy()
column = ['時間','名前','卒業年度','趣味','読書_ジャンル',
          'スポーツ_ジャンル','音楽_ジャンル','ゲーム_ジャンル',
          'アニメ・漫画_ジャンル','映画_ジャンル','出身地','居住地',
          'アウトドア_ジャンル','テレビ_ジャンル','MBTI','志望業界・職種',
    	  '就活状況','学部・専攻','部活','プロジェクト','強み','弱み','会える場所',
	      '相談に乗れること','筋トレ_目的','手伝ってほしいこと','推し活']
df_.columns = column

df_['名前'] = df_['名前'].replace('',np.nan)
df_ = df_.dropna(subset='名前')

df_['時間'] = pd.to_datetime(df_['時間'])
df_ = df_.groupby('名前').last().reset_index()

df_ = df_.fillna('0')

# df_['卒業年度'] = df_['卒業年度'].replace({'学部1年':0,'学部2年':1,'学部3年':2,'学部4年':3,'院1年':4,'院2年':5})

category_order = ['INTJ-A（建築家）', 'INTJ-T（建築家）', 
                  'INTP-A（論理学者）', 'INTP-T（論理学者）',
                  'ENTJ-A（指揮官）', 'ENTJ-T（指揮官）',
                  'ENTP-A（討論者）', 'ENTP-T（討論者）',
                  'INFJ-A（提唱者）', 'INFJ-T（提唱者）',
                  'INFP-A（仲介者）', 'INFP-T（仲介者）',
                  'ENFJ-A（主人公）', 'ENFJ-T（主人公）',
                  'ENFP-A（運動家）', 'ENFP-T（運動家）',
                  'ISTJ-A（管理者）', 'ISTJ-T（管理者）',
                  'ISFJ-A（擁護者）', 'ISFJ-T（擁護者）',
                  'ESTJ-A（幹部）', 'ESTJ-T（幹部）',
                  'ESFJ-A（領事）', 'ESFJ-T（領事）',
                  'ISTP-A（巨匠）', 'ISTP-T（巨匠）',
                  'ISFP-A（冒険家）', 'ISFP-T（冒険家）',
                  'ESTP-A（起業家）', 'ESTP-T（起業家）',
                  'ESFP-A（エンターテイナー）', 'ESFP-T（エンターテイナー）']
df_["MBTI"] = pd.Categorical(df_["MBTI"], categories=category_order, ordered=True)
df_["MBTI"] = df_["MBTI"].cat.codes

category_order = ['就活準備中（1・2年生など）','絶賛就活中','就活終了']
df_["就活状況"] = pd.Categorical(df_["就活状況"], categories=category_order, ordered=True)
df_["就活状況"] = df_["就活状況"].cat.codes

category_order = ['文学部', '経営学部', '経済学部', '商学部', '心理学部',
                  '教育学部', '医学部', '法学部', '外国語学部', '工学部',
                  '建築学部', '数学部', '薬学部', '情報学部', 'その他',]
df_["学部・専攻"] = pd.Categorical(df_["学部・専攻"], categories=category_order, ordered=True)
df_["学部・専攻"] = df_["学部・専攻"].cat.codes

category_order = ['マッチョになりたい', '健康（運動不足の解消）のため', 'ダイエットのため']
df_["筋トレ_目的"] = pd.Categorical(df_["筋トレ_目的"], categories=category_order, ordered=True)
df_["筋トレ_目的"] = df_["筋トレ_目的"].cat.codes

category_order = ['北海道', '青森県', '岩手県', '宮城県', '秋田県',
                  '山形県', '福島県', '茨城県', '栃木県', '群馬県',
                  '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県',
                  '富山県', '石川県', '福井県', '山梨県', '長野県',
                  '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県',
                  '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
                  '鳥取県', '島根県', '岡山県', '広島県', '山口県',
                  '徳島県', '香川県', '愛媛県', '高知県', '福岡県',
                  '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県',
                  '鹿児島県', '沖縄県', '海外']
df_["出身地"] = pd.Categorical(df_["出身地"], categories=category_order, ordered=True)
df_["出身地"] = df_["出身地"].cat.codes
df_["居住地"] = pd.Categorical(df_["居住地"], categories=category_order, ordered=True)
df_["居住地"] = df_["居住地"].cat.codes

df_['志望業界_人材'] = df_['志望業界・職種'].apply(lambda x: 1 if '人材' in x else 0)
df_['志望業界_教育'] = df_['志望業界・職種'].apply(lambda x: 1 if '教育' in x else 0)
df_['志望業界_商社'] = df_['志望業界・職種'].apply(lambda x: 1 if '商社' in x else 0)
df_['志望業界_コンサル'] = df_['志望業界・職種'].apply(lambda x: 1 if 'コンサル' in x else 0)
df_['志望業界_メーカー'] = df_['志望業界・職種'].apply(lambda x: 1 if 'メーカー' in x else 0)
df_['志望業界_広告'] = df_['志望業界・職種'].apply(lambda x: 1 if '広告' in x else 0)
df_['志望業界_マーケティング'] = df_['志望業界・職種'].apply(lambda x: 1 if 'マーケティング' in x else 0)
df_['志望業界_金融・保険'] = df_['志望業界・職種'].apply(lambda x: 1 if '金融・保険' in x else 0)
df_['志望業界_小売'] = df_['志望業界・職種'].apply(lambda x: 1 if '小売' in x else 0)
df_['志望業界_サービス'] = df_['志望業界・職種'].apply(lambda x: 1 if 'サービス' in x else 0)
df_['志望業界_メディア'] = df_['志望業界・職種'].apply(lambda x: 1 if 'メディア' in x else 0)
df_['志望業界_エンジニア'] = df_['志望業界・職種'].apply(lambda x: 1 if 'エンジニア' in x else 0)
df_['志望業界_企画職'] = df_['志望業界・職種'].apply(lambda x: 1 if '企画職' in x else 0)
df_['志望業界_未定'] = df_['志望業界・職種'].apply(lambda x: 1 if '未定' in x else 0)

df_['プロジェクト_CS'] = df_['プロジェクト'].apply(lambda x: 1 if 'CS' in x else 0)
df_['プロジェクト_営業'] = df_['プロジェクト'].apply(lambda x: 1 if '営業' in x else 0)
df_['プロジェクト_ailes（エールズ）'] = df_['プロジェクト'].apply(lambda x: 1 if 'ailes（エールズ）' in x else 0)
df_['プロジェクト_license'] = df_['プロジェクト'].apply(lambda x: 1 if 'license' in x else 0)
df_['プロジェクト_ライティング'] = df_['プロジェクト'].apply(lambda x: 1 if 'ライティング' in x else 0)
df_['プロジェクト_ナイトワーク運営'] = df_['プロジェクト'].apply(lambda x: 1 if 'ナイトワーク運営' in x else 0)
df_['プロジェクト_メディア'] = df_['プロジェクト'].apply(lambda x: 1 if 'メディア' in x else 0)
df_['プロジェクト_デザイン'] = df_['プロジェクト'].apply(lambda x: 1 if 'デザイン' in x else 0)
df_['プロジェクト_TikTok'] = df_['プロジェクト'].apply(lambda x: 1 if 'TikTok' in x else 0)
df_['プロジェクト_X（旧：Twitter）'] = df_['プロジェクト'].apply(lambda x: 1 if 'X（旧：Twitter）' in x else 0)

df_['部活_サッカー'] = df_['部活'].apply(lambda x: 1 if 'サッカー' in x else 0)
df_['部活_バスケットボール'] = df_['部活'].apply(lambda x: 1 if 'バスケットボール' in x else 0)
df_['部活_野球'] = df_['部活'].apply(lambda x: 1 if '野球' in x else 0)
df_['部活_卓球'] = df_['部活'].apply(lambda x: 1 if '卓球' in x else 0)
df_['部活_テニス'] = df_['部活'].apply(lambda x: 1 if 'テニス' in x else 0)
df_['部活_陸上'] = df_['部活'].apply(lambda x: 1 if '陸上' in x else 0)
df_['部活_バレーボール'] = df_['部活'].apply(lambda x: 1 if 'バレーボール' in x else 0)
df_['部活_バドミントン'] = df_['部活'].apply(lambda x: 1 if 'バドミントン' in x else 0)
df_['部活_剣道'] = df_['部活'].apply(lambda x: 1 if '剣道' in x else 0)
df_['部活_水泳'] = df_['部活'].apply(lambda x: 1 if '水泳' in x else 0)
df_['部活_柔道'] = df_['部活'].apply(lambda x: 1 if '柔道' in x else 0)
df_['部活_ハンドボール'] = df_['部活'].apply(lambda x: 1 if 'ハンドボール' in x else 0)
df_['部活_体操'] = df_['部活'].apply(lambda x: 1 if '体操' in x else 0)
df_['部活_ソフトボール'] = df_['部活'].apply(lambda x: 1 if 'ソフトボール' in x else 0)
df_['部活_相撲'] = df_['部活'].apply(lambda x: 1 if '相撲' in x else 0)
df_['部活_空手'] = df_['部活'].apply(lambda x: 1 if '空手' in x else 0)
df_['部活_アイスホッケー'] = df_['部活'].apply(lambda x: 1 if 'アイスホッケー' in x else 0)
df_['部活_スケート'] = df_['部活'].apply(lambda x: 1 if 'スケート' in x else 0)
df_['部活_新体操'] = df_['部活'].apply(lambda x: 1 if '新体操' in x else 0)
df_['部活_スキー'] = df_['部活'].apply(lambda x: 1 if 'スキー' in x else 0)
df_['部活_吹奏楽'] = df_['部活'].apply(lambda x: 1 if '吹奏楽' in x else 0)
df_['部活_美術'] = df_['部活'].apply(lambda x: 1 if '美術' in x else 0)
df_['部活_合唱・コーラス'] = df_['部活'].apply(lambda x: 1 if '合唱・コーラス' in x else 0)
df_['部活_アカペラ'] = df_['部活'].apply(lambda x: 1 if 'アカペラ' in x else 0)
df_['部活_パソコン'] = df_['部活'].apply(lambda x: 1 if 'パソコン' in x else 0)
df_['部活_自然科学'] = df_['部活'].apply(lambda x: 1 if '自然科学' in x else 0)
df_['部活_調理'] = df_['部活'].apply(lambda x: 1 if '調理' in x else 0)
df_['部活_茶道'] = df_['部活'].apply(lambda x: 1 if '茶道' in x else 0)
df_['部活_放送'] = df_['部活'].apply(lambda x: 1 if '放送' in x else 0)
df_['部活_弓道'] = df_['部活'].apply(lambda x: 1 if '弓道' in x else 0)
df_['部活_ラグビー'] = df_['部活'].apply(lambda x: 1 if 'ラグビー' in x else 0)
df_['部活_ボート'] = df_['部活'].apply(lambda x: 1 if 'ボート' in x else 0)
df_['部活_アーチェリー'] = df_['部活'].apply(lambda x: 1 if 'アーチェリー' in x else 0)
df_['部活_ボクシング'] = df_['部活'].apply(lambda x: 1 if 'ボクシング' in x else 0)
df_['部活_レスリング'] = df_['部活'].apply(lambda x: 1 if 'レスリング' in x else 0)
df_['部活_少林寺拳法'] = df_['部活'].apply(lambda x: 1 if '少林寺拳法' in x else 0)
df_['部活_書道'] = df_['部活'].apply(lambda x: 1 if '書道' in x else 0)
df_['部活_写真'] = df_['部活'].apply(lambda x: 1 if '写真' in x else 0)
df_['部活_演劇'] = df_['部活'].apply(lambda x: 1 if '演劇' in x else 0)
df_['部活_ダンス'] = df_['部活'].apply(lambda x: 1 if 'ダンス' in x else 0)
df_['部活_チアリーダー・チアダンス'] = df_['部活'].apply(lambda x: 1 if 'チアリーダー・チアダンス' in x else 0)
df_['部活_ボランティア'] = df_['部活'].apply(lambda x: 1 if 'ボランティア' in x else 0)

df_['趣味_映画鑑賞'] = df_['趣味'].apply(lambda x: 1 if '映画鑑賞' in x else 0)
df_['趣味_ダーツ'] = df_['趣味'].apply(lambda x: 1 if 'ダーツ' in x else 0)
df_['趣味_動物好き'] = df_['趣味'].apply(lambda x: 1 if '動物好き' in x else 0)
df_['趣味_料理'] = df_['趣味'].apply(lambda x: 1 if '料理' in x else 0)
df_['趣味_美術鑑賞'] = df_['趣味'].apply(lambda x: 1 if '美術鑑賞' in x else 0)
df_['趣味_ドライブ'] = df_['趣味'].apply(lambda x: 1 if 'ドライブ' in x else 0)
df_['趣味_グルメ・食べ歩き'] = df_['趣味'].apply(lambda x: 1 if 'グルメ・食べ歩き' in x else 0)
df_['趣味_旅行'] = df_['趣味'].apply(lambda x: 1 if '旅行' in x else 0)
df_['趣味_スノーボード・スキー'] = df_['趣味'].apply(lambda x: 1 if 'スノーボード・スキー' in x else 0)
df_['趣味_アウトドア'] = df_['趣味'].apply(lambda x: 1 if 'アウトドア' in x else 0)
df_['趣味_カフェ巡り'] = df_['趣味'].apply(lambda x: 1 if 'カフェ巡り' in x else 0)
df_['趣味_スポーツ観戦'] = df_['趣味'].apply(lambda x: 1 if 'スポーツ観戦' in x else 0)
df_['趣味_音楽鑑賞'] = df_['趣味'].apply(lambda x: 1 if '音楽鑑賞' in x else 0)
df_['趣味_カラオケ'] = df_['趣味'].apply(lambda x: 1 if 'カラオケ' in x else 0)
df_['趣味_ファッション・買い物'] = df_['趣味'].apply(lambda x: 1 if 'ファッション・買い物' in x else 0)
df_['趣味_読書'] = df_['趣味'].apply(lambda x: 1 if '読書' in x else 0)
df_['趣味_ビリヤード'] = df_['趣味'].apply(lambda x: 1 if 'ビリヤード' in x else 0)
df_['趣味_アニメ・漫画'] = df_['趣味'].apply(lambda x: 1 if 'アニメ・漫画' in x else 0)
df_['趣味_ゲーム'] = df_['趣味'].apply(lambda x: 1 if 'ゲーム' in x else 0)
df_['趣味_ランニング'] = df_['趣味'].apply(lambda x: 1 if 'ランニング' in x else 0)
df_['趣味_カメラ'] = df_['趣味'].apply(lambda x: 1 if 'カメラ' in x else 0)
df_['趣味_バイク'] = df_['趣味'].apply(lambda x: 1 if 'バイク' in x else 0)
df_['趣味_釣り'] = df_['趣味'].apply(lambda x: 1 if '釣り' in x else 0)
df_['趣味_サバイバルゲーム'] = df_['趣味'].apply(lambda x: 1 if 'サバイバルゲーム' in x else 0)
df_['趣味_ダンス'] = df_['趣味'].apply(lambda x: 1 if 'ダンス' in x else 0)
df_['趣味_楽器・バンド'] = df_['趣味'].apply(lambda x: 1 if '楽器・バンド' in x else 0)
df_['趣味_DIY'] = df_['趣味'].apply(lambda x: 1 if 'DIY' in x else 0)
df_['趣味_インテリア'] = df_['趣味'].apply(lambda x: 1 if 'インテリア' in x else 0)
df_['趣味_プラモデル'] = df_['趣味'].apply(lambda x: 1 if 'プラモデル' in x else 0)
df_['趣味_スポーツ全般'] = df_['趣味'].apply(lambda x: 1 if 'スポーツ全般' in x else 0)
df_['趣味_スキューバダイビング'] = df_['趣味'].apply(lambda x: 1 if 'スキューバダイビング' in x else 0)
df_['趣味_サーフィン'] = df_['趣味'].apply(lambda x: 1 if 'サーフィン' in x else 0)
df_['趣味_手芸'] = df_['趣味'].apply(lambda x: 1 if '手芸' in x else 0)
df_['趣味_麻雀'] = df_['趣味'].apply(lambda x: 1 if '麻雀' in x else 0)
df_['趣味_囲碁・将棋'] = df_['趣味'].apply(lambda x: 1 if '囲碁・将棋' in x else 0)
df_['趣味_お酒'] = df_['趣味'].apply(lambda x: 1 if 'お酒' in x else 0)
df_['趣味_テレビ'] = df_['趣味'].apply(lambda x: 1 if 'テレビ' in x else 0)
df_['趣味_筋トレ'] = df_['趣味'].apply(lambda x: 1 if '筋トレ' in x else 0)
df_['趣味_その他'] = df_['趣味'].apply(lambda x: 1 if 'その他' in x else 0)

df_['読書_小説'] = df_['読書_ジャンル'].apply(lambda x: 1 if '小説' in x else 0)
df_['読書_ビジネス書'] = df_['読書_ジャンル'].apply(lambda x: 1 if 'ビジネス' in x else 0)
df_['読書_自己啓発書'] = df_['読書_ジャンル'].apply(lambda x: 1 if '自己啓発' in x else 0)
df_['読書_専門書'] = df_['読書_ジャンル'].apply(lambda x: 1 if '専門書' in x else 0)
df_['読書_その他'] = df_['読書_ジャンル'].apply(lambda x: 1 if 'その他' in x else 0)

df_['スポーツ_野球'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if '野球' in x else 0)
df_['スポーツ_サッカー'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'サッカー' in x else 0)
df_['スポーツ_テニス'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'テニス' in x else 0)
df_['スポーツ_バレーボール'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'バレーボール' in x else 0)
df_['スポーツ_バスケットボール'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'バスケットボール' in x else 0)
df_['スポーツ_バドミントン'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'バドミントン' in x else 0)
df_['スポーツ_ラグビー'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'ラグビー' in x else 0)
df_['スポーツ_格闘技'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if '格闘技' in x else 0)
df_['スポーツ_ゴルフ'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'ゴルフ' in x else 0)
df_['スポーツ_スキー'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'スキー' in x else 0)
df_['スポーツ_ダンス'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'ダンス' in x else 0)
df_['スポーツ_相撲'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if '相撲' in x else 0)
df_['スポーツ_その他'] = df_['スポーツ_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['音楽_J-POP'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'J-POP' in x else 0)
df_['音楽_K-POP'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'K-POP' in x else 0)
df_['音楽_ロック'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'ロック' in x else 0)
df_['音楽_アニソン'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'アニソン' in x else 0)
df_['音楽_ラップ'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'ラップ' in x else 0)
df_['音楽_ヒップホップ'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'ヒップホップ' in x else 0)
df_['音楽_バンド'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'バンド' in x else 0)
df_['音楽_洋楽'] = df_['音楽_ジャンル'].apply(lambda x:1 if '洋楽' in x else 0)
df_['音楽_クラシック'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'クラシック' in x else 0)
df_['音楽_演歌'] = df_['音楽_ジャンル'].apply(lambda x:1 if '演歌' in x else 0)
df_['音楽_ボカロ'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'ボカロ' in x else 0)
df_['音楽_その他'] = df_['音楽_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['ゲーム_アクション'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'アクション' in x else 0)
df_['ゲーム_RPG'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'RPG' in x else 0)
df_['ゲーム_カード'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'カード' in x else 0)
df_['ゲーム_ボードゲーム'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'ボードゲーム' in x else 0)
df_['ゲーム_パズル'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'パズル' in x else 0)
df_['ゲーム_シミュレーション'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'シミュレーション' in x else 0)
df_['ゲーム_スポーツ'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'スポーツ' in x else 0)
df_['ゲーム_音ゲー'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if '音ゲー' in x else 0)
df_['ゲーム_その他'] = df_['ゲーム_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['アニメ_ロボット'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'ロボット' in x else 0)
df_['アニメ_アクション'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'アクション' in x else 0)
df_['アニメ_冒険'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if '冒険' in x else 0)
df_['アニメ_コメディ'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'コメディ' in x else 0)
df_['アニメ_恋愛・ロマンス'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if '恋愛・ロマンス' in x else 0)
df_['アニメ_ファンタジー'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'ファンタジー' in x else 0)
df_['アニメ_ホラー'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'ホラー' in x else 0)
df_['アニメ_SF'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'SF' in x else 0)
df_['アニメ_スポーツ'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'スポーツ' in x else 0)
df_['アニメ_異世界'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if '異世界' in x else 0)
df_['アニメ_ミステリー'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'ミステリー' in x else 0)
df_['アニメ_歴史'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if '歴史' in x else 0)
df_['アニメ_美少女'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if '美少女' in x else 0)
df_['アニメ_その他'] = df_['アニメ・漫画_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['映画_アクション'] = df_['映画_ジャンル'].apply(lambda x:1 if 'アクション' in x else 0)
df_['映画_ドラマ'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ドラマ' in x else 0)
df_['映画_コメディ'] = df_['映画_ジャンル'].apply(lambda x:1 if 'コメディ' in x else 0)
df_['映画_恋愛・ロマンス'] = df_['映画_ジャンル'].apply(lambda x:1 if '恋愛・ロマンス' in x else 0)
df_['映画_ホラー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ホラー' in x else 0)
df_['映画_SF'] = df_['映画_ジャンル'].apply(lambda x:1 if 'SF' in x else 0)
df_['映画_ファンタジー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ファンタジー' in x else 0)
df_['映画_ミステリー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ミステリー' in x else 0)
df_['映画_冒険'] = df_['映画_ジャンル'].apply(lambda x:1 if '冒険' in x else 0)
df_['映画_ジブリ'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ジブリ' in x else 0)
df_['映画_歴史・戦争'] = df_['映画_ジャンル'].apply(lambda x:1 if '歴史・戦争' in x else 0)
df_['映画_スポーツ'] = df_['映画_ジャンル'].apply(lambda x:1 if 'スポーツ' in x else 0)
df_['映画_ドキュメンタリー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ドキュメンタリー' in x else 0)
df_['映画_伝記'] = df_['映画_ジャンル'].apply(lambda x:1 if '伝記' in x else 0)
df_['映画_アニメ'] = df_['映画_ジャンル'].apply(lambda x:1 if 'アニメ' in x else 0)
df_['映画_ピクサー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ピクサー' in x else 0)
df_['映画_ディズニー'] = df_['映画_ジャンル'].apply(lambda x:1 if 'ディズニー' in x else 0)
df_['映画_洋画'] = df_['映画_ジャンル'].apply(lambda x:1 if '洋画' in x else 0)
df_['映画_その他'] = df_['映画_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['アウトドア_登山'] = df_['アウトドア_ジャンル'].apply(lambda x:1 if '登山' in x else 0)
df_['アウトドア_サイクリング'] = df_['アウトドア_ジャンル'].apply(lambda x:1 if 'サイクリング' in x else 0)
df_['アウトドア_キャンプ'] = df_['アウトドア_ジャンル'].apply(lambda x:1 if 'キャンプ' in x else 0)
df_['アウトドア_散歩'] = df_['アウトドア_ジャンル'].apply(lambda x:1 if '散歩' in x else 0)
df_['アウトドア_その他'] = df_['アウトドア_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['テレビ_バラエティ'] = df_['テレビ_ジャンル'].apply(lambda x:1 if 'バラエティ' in x else 0)
df_['テレビ_ドラマ'] = df_['テレビ_ジャンル'].apply(lambda x:1 if 'ドラマ' in x else 0)
df_['テレビ_お笑い・漫才'] = df_['テレビ_ジャンル'].apply(lambda x:1 if 'お笑い・漫才' in x else 0)
df_['テレビ_音楽'] = df_['テレビ_ジャンル'].apply(lambda x:1 if '音楽' in x else 0)
df_['テレビ_その他'] = df_['テレビ_ジャンル'].apply(lambda x:1 if 'その他' in x else 0)

df_['強み_論理的思考'] = df_['強み'].apply(lambda x:1 if '論理的思考' in x else 0)
df_['強み_自己肯定感が高い'] = df_['強み'].apply(lambda x:1 if '自己肯定感が高い' in x else 0)
df_['強み_メンタルが強い'] = df_['強み'].apply(lambda x:1 if 'メンタルが強い' in x else 0)
df_['強み_コミュニケーション能力'] = df_['強み'].apply(lambda x:1 if 'コミュニケーション能力' in x else 0)
df_['強み_聞き上手'] = df_['強み'].apply(lambda x:1 if '聞き上手' in x else 0)
df_['強み_主体性がある'] = df_['強み'].apply(lambda x:1 if '主体性がある' in x else 0)
df_['強み_課題解決力'] = df_['強み'].apply(lambda x:1 if '課題解決力' in x else 0)
df_['強み_チームワーク力'] = df_['強み'].apply(lambda x:1 if 'チームワーク力' in x else 0)
df_['強み_リーダーシップ'] = df_['強み'].apply(lambda x:1 if 'リーダーシップ' in x else 0)
df_['強み_協調性'] = df_['強み'].apply(lambda x:1 if '協調性' in x else 0)
df_['強み_実行力'] = df_['強み'].apply(lambda x:1 if '実行力' in x else 0)
df_['強み_創造力'] = df_['強み'].apply(lambda x:1 if '創造力' in x else 0)
df_['強み_発信力'] = df_['強み'].apply(lambda x:1 if '発信力' in x else 0)

df_['弱み_論理的思考'] = df_['弱み'].apply(lambda x:1 if '論理的思考' in x else 0)
df_['弱み_自己肯定感が高い'] = df_['弱み'].apply(lambda x:1 if '自己肯定感が高い' in x else 0)
df_['弱み_メンタルが強い'] = df_['弱み'].apply(lambda x:1 if 'メンタルが強い' in x else 0)
df_['弱み_コミュニケーション能力'] = df_['弱み'].apply(lambda x:1 if 'コミュニケーション能力' in x else 0)
df_['弱み_聞き上手'] = df_['弱み'].apply(lambda x:1 if '聞き上手' in x else 0)
df_['弱み_主体性がある'] = df_['弱み'].apply(lambda x:1 if '主体性がある' in x else 0)
df_['弱み_課題解決力'] = df_['弱み'].apply(lambda x:1 if '課題解決力' in x else 0)
df_['弱み_チームワーク力'] = df_['弱み'].apply(lambda x:1 if 'チームワーク力' in x else 0)
df_['弱み_リーダーシップ'] = df_['弱み'].apply(lambda x:1 if 'リーダーシップ' in x else 0)
df_['弱み_協調性'] = df_['弱み'].apply(lambda x:1 if '協調性' in x else 0)
df_['弱み_実行力'] = df_['弱み'].apply(lambda x:1 if '実行力' in x else 0)
df_['弱み_創造力'] = df_['弱み'].apply(lambda x:1 if '創造力' in x else 0)
df_['弱み_発信力'] = df_['弱み'].apply(lambda x:1 if '発信力' in x else 0)

df_['会える場所_北海道'] = df_['会える場所'].apply(lambda x:1 if '北海道' in x else 0)
df_['会える場所_青森県'] = df_['会える場所'].apply(lambda x:1 if '青森県' in x else 0)
df_['会える場所_岩手県'] = df_['会える場所'].apply(lambda x:1 if '岩手県' in x else 0)
df_['会える場所_宮城県'] = df_['会える場所'].apply(lambda x:1 if '宮城県' in x else 0)
df_['会える場所_秋田県'] = df_['会える場所'].apply(lambda x:1 if '秋田県' in x else 0)
df_['会える場所_山形県'] = df_['会える場所'].apply(lambda x:1 if '山形県' in x else 0)
df_['会える場所_福島県'] = df_['会える場所'].apply(lambda x:1 if '福島県' in x else 0)
df_['会える場所_茨城県'] = df_['会える場所'].apply(lambda x:1 if '茨城県' in x else 0)
df_['会える場所_栃木県'] = df_['会える場所'].apply(lambda x:1 if '栃木県' in x else 0)
df_['会える場所_群馬県'] = df_['会える場所'].apply(lambda x:1 if '群馬県' in x else 0)
df_['会える場所_埼玉県'] = df_['会える場所'].apply(lambda x:1 if '埼玉県' in x else 0)
df_['会える場所_千葉県'] = df_['会える場所'].apply(lambda x:1 if '千葉県' in x else 0)
df_['会える場所_東京都'] = df_['会える場所'].apply(lambda x:1 if '東京都' in x else 0)
df_['会える場所_神奈川県'] = df_['会える場所'].apply(lambda x:1 if '神奈川県' in x else 0)
df_['会える場所_新潟県'] = df_['会える場所'].apply(lambda x:1 if '新潟県' in x else 0)
df_['会える場所_富山県'] = df_['会える場所'].apply(lambda x:1 if '富山県' in x else 0)
df_['会える場所_石川県'] = df_['会える場所'].apply(lambda x:1 if '石川県' in x else 0)
df_['会える場所_福井県'] = df_['会える場所'].apply(lambda x:1 if '福井県' in x else 0)
df_['会える場所_山梨県'] = df_['会える場所'].apply(lambda x:1 if '山梨県' in x else 0)
df_['会える場所_長野県'] = df_['会える場所'].apply(lambda x:1 if '長野県' in x else 0)
df_['会える場所_岐阜県'] = df_['会える場所'].apply(lambda x:1 if '岐阜県' in x else 0)
df_['会える場所_静岡県'] = df_['会える場所'].apply(lambda x:1 if '静岡県' in x else 0)
df_['会える場所_愛知県'] = df_['会える場所'].apply(lambda x:1 if '愛知県' in x else 0)
df_['会える場所_三重県'] = df_['会える場所'].apply(lambda x:1 if '三重県' in x else 0)
df_['会える場所_滋賀県'] = df_['会える場所'].apply(lambda x:1 if '滋賀県' in x else 0)
df_['会える場所_京都府'] = df_['会える場所'].apply(lambda x:1 if '京都府' in x else 0)
df_['会える場所_大阪府'] = df_['会える場所'].apply(lambda x:1 if '大阪府' in x else 0)
df_['会える場所_兵庫県'] = df_['会える場所'].apply(lambda x:1 if '兵庫県' in x else 0)
df_['会える場所_奈良県'] = df_['会える場所'].apply(lambda x:1 if '奈良県' in x else 0)
df_['会える場所_和歌山県'] = df_['会える場所'].apply(lambda x:1 if '和歌山県' in x else 0)
df_['会える場所_鳥取県'] = df_['会える場所'].apply(lambda x:1 if '鳥取県' in x else 0)
df_['会える場所_島根県'] = df_['会える場所'].apply(lambda x:1 if '島根県' in x else 0)
df_['会える場所_岡山県'] = df_['会える場所'].apply(lambda x:1 if '岡山県' in x else 0)
df_['会える場所_広島県'] = df_['会える場所'].apply(lambda x:1 if '広島県' in x else 0)
df_['会える場所_山口県'] = df_['会える場所'].apply(lambda x:1 if '山口県' in x else 0)
df_['会える場所_徳島県'] = df_['会える場所'].apply(lambda x:1 if '徳島県' in x else 0)
df_['会える場所_香川県'] = df_['会える場所'].apply(lambda x:1 if '香川県' in x else 0)
df_['会える場所_愛媛県'] = df_['会える場所'].apply(lambda x:1 if '愛媛県' in x else 0)
df_['会える場所_高知県'] = df_['会える場所'].apply(lambda x:1 if '高知県' in x else 0)
df_['会える場所_福岡県'] = df_['会える場所'].apply(lambda x:1 if '福岡県' in x else 0)
df_['会える場所_佐賀県'] = df_['会える場所'].apply(lambda x:1 if '佐賀県' in x else 0)
df_['会える場所_長崎県'] = df_['会える場所'].apply(lambda x:1 if '長崎県' in x else 0)
df_['会える場所_熊本県'] = df_['会える場所'].apply(lambda x:1 if '熊本県' in x else 0)
df_['会える場所_大分県'] = df_['会える場所'].apply(lambda x:1 if '大分県' in x else 0)
df_['会える場所_宮崎県'] = df_['会える場所'].apply(lambda x:1 if '宮崎県' in x else 0)
df_['会える場所_鹿児島県'] = df_['会える場所'].apply(lambda x:1 if '鹿児島県' in x else 0)
df_['会える場所_沖縄県'] = df_['会える場所'].apply(lambda x:1 if '沖縄県' in x else 0)

df_['相談に乗れること_自己分析'] = df_['相談に乗れること'].apply(lambda x:1 if '自己分析' in x else 0)
df_['相談に乗れること_ES添削'] = df_['相談に乗れること'].apply(lambda x:1 if 'ES添削' in x else 0)
df_['相談に乗れること_面接練習'] = df_['相談に乗れること'].apply(lambda x:1 if '面接練習' in x else 0)
df_['相談に乗れること_GD練習・FB'] = df_['相談に乗れること'].apply(lambda x:1 if 'GD練習・FB' in x else 0)

df_['手伝ってほしいこと_自己分析'] = df_['手伝ってほしいこと'].apply(lambda x:1 if '自己分析' in x else 0)
df_['手伝ってほしいこと_ES添削'] = df_['手伝ってほしいこと'].apply(lambda x:1 if 'ES添削' in x else 0)
df_['手伝ってほしいこと_面接練習'] = df_['手伝ってほしいこと'].apply(lambda x:1 if '面接練習' in x else 0)
df_['手伝ってほしいこと_GD練習・FB'] = df_['手伝ってほしいこと'].apply(lambda x:1 if 'GD練習・FB' in x else 0)

df_['推し活_LDH'] = df_['推し活'].apply(lambda x:1 if 'LDH' in x else 0)
df_['推し活_Vaundy'] = df_['推し活'].apply(lambda x:1 if 'Vaundy' in x else 0)
df_['推し活_Official髭男dism'] = df_['推し活'].apply(lambda x:1 if 'Official髭男dism' in x else 0)
df_['推し活_なにわ男子'] = df_['推し活'].apply(lambda x:1 if 'なにわ男子' in x else 0)
df_['推し活_back number'] = df_['推し活'].apply(lambda x:1 if 'back number' in x else 0)
df_['推し活_マカロニえんぴつ'] = df_['推し活'].apply(lambda x:1 if 'マカロニえんぴつ' in x else 0)
df_['推し活_クリープハイプ'] = df_['推し活'].apply(lambda x:1 if 'クリープハイプ' in x else 0)
df_['推し活_snowman'] = df_['推し活'].apply(lambda x:1 if 'snowman' in x else 0)
df_['推し活_坂道グループ'] = df_['推し活'].apply(lambda x:1 if '坂道グループ' in x else 0)
df_['推し活_BLACKPINK'] = df_['推し活'].apply(lambda x:1 if 'BLACKPINK' in x else 0)
df_['推し活_TWICE'] = df_['推し活'].apply(lambda x:1 if 'TWICE' in x else 0)
df_['推し活_モーニング娘。'] = df_['推し活'].apply(lambda x:1 if 'モーニング娘。' in x else 0)
df_['推し活_優里'] = df_['推し活'].apply(lambda x:1 if '優里' in x else 0)
df_['推し活_Novelbright'] = df_['推し活'].apply(lambda x:1 if 'Novelbright' in x else 0)
df_['推し活_SEKAI NO OWARI'] = df_['推し活'].apply(lambda x:1 if 'SEKAI NO OWARI' in x else 0)
df_['推し活_Mrs. GREEN APPLE'] = df_['推し活'].apply(lambda x:1 if 'Mrs. GREEN APPLE' in x else 0)
df_['推し活_iLiFE!'] = df_['推し活'].apply(lambda x:1 if 'iLiFE!' in x else 0)
df_['推し活_INI'] = df_['推し活'].apply(lambda x:1 if 'INI' in x else 0)
df_['推し活_ずっと真夜中でいいのに。'] = df_['推し活'].apply(lambda x:1 if 'ずっと真夜中でいいのに。' in x else 0)
df_['推し活_BE:FIRST'] = df_['推し活'].apply(lambda x:1 if 'BE:FIRST' in x else 0)
df_['推し活_AAA'] = df_['推し活'].apply(lambda x:1 if 'AAA' in x else 0)
df_['推し活_Nissy'] = df_['推し活'].apply(lambda x:1 if 'Nissy' in x else 0)
df_['推し活_GReeeeN'] = df_['推し活'].apply(lambda x:1 if 'GReeeeN' in x else 0)
df_['推し活_ジャニーズ'] = df_['推し活'].apply(lambda x:1 if 'ジャニーズ' in x else 0)
df_['推し活_ワンピース'] = df_['推し活'].apply(lambda x:1 if 'ワンピース' in x else 0)
df_['推し活_呪術廻戦'] = df_['推し活'].apply(lambda x:1 if '呪術回線' in x else 0)
df_['推し活_少年ジャンプ'] = df_['推し活'].apply(lambda x:1 if '少年ジャンプ' in x else 0)
df_['推し活_キングダム'] = df_['推し活'].apply(lambda x:1 if 'キングダム' in x else 0)
df_['推し活_進撃の巨人'] = df_['推し活'].apply(lambda x:1 if '進撃の巨人' in x else 0)
df_['推し活_東京リベンジャーズ'] = df_['推し活'].apply(lambda x:1 if '東京リベンジャーズ' in x else 0)
df_['推し活_ハイキュー'] = df_['推し活'].apply(lambda x:1 if 'ハイキュー' in x else 0)
df_['推し活_僕のヒーローアカデミア'] = df_['推し活'].apply(lambda x:1 if '僕のヒーローアカデミア' in x else 0)
df_['推し活_クレヨンしんちゃん'] = df_['推し活'].apply(lambda x:1 if 'クレヨンしんちゃん' in x else 0)
df_['推し活_文豪ストレイドッグス'] = df_['推し活'].apply(lambda x:1 if '文豪ストレイドッグス' in x else 0)
df_['推し活_名探偵コナン'] = df_['推し活'].apply(lambda x:1 if '名探偵コナン' in x else 0)
df_['推し活_銀魂'] = df_['推し活'].apply(lambda x:1 if '銀魂' in x else 0)
df_['推し活_魔法少女まどかマギカ'] = df_['推し活'].apply(lambda x:1 if '魔法少女まどかマギカ' in x else 0)
df_['推し活_大乱闘スマッシュブラザーズ'] = df_['推し活'].apply(lambda x:1 if '大乱闘スマッシュブラザーズ' in x else 0)
df_['推し活_原神'] = df_['推し活'].apply(lambda x:1 if '原神' in x else 0)
df_['推し活_ドラゴンクエスト'] = df_['推し活'].apply(lambda x:1 if 'ドラゴンクエスト' in x else 0)
df_['推し活_ポケモン'] = df_['推し活'].apply(lambda x:1 if 'ポケモン' in x else 0)
df_['推し活_ディズニー'] = df_['推し活'].apply(lambda x:1 if 'ディズニー' in x else 0)
df_['推し活_ちいかわ'] = df_['推し活'].apply(lambda x:1 if 'ちいかわ' in x else 0)
df_['推し活_東海オンエア'] = df_['推し活'].apply(lambda x:1 if '東海オンエア' in x else 0)

df_ = df_.drop({
    '志望業界・職種',
    'プロジェクト',
    '部活',
    '趣味',
    '読書_ジャンル',
    'スポーツ_ジャンル',
    '音楽_ジャンル',
    'ゲーム_ジャンル',
    'アニメ・漫画_ジャンル',
    '映画_ジャンル',
    'アウトドア_ジャンル',
    'テレビ_ジャンル',
    '強み',
    '弱み',
    '会える場所',
    '相談に乗れること',
    '手伝ってほしいこと',
    '推し活',
    },axis=1)
# st.dataframe(df_)

df_['卒業年度'] = df_['卒業年度'].astype(int)
df_.iloc[:, 2:] = df_.iloc[:, 2:].astype(int)

df_column = df_.columns

name = st.text_input('あなたの名前を入力してください（漢字フルネーム、スペースなし）')
options = st.radio(
    "マッチングタイプを選んでください",
    ['全項目', '趣味・好きなこと', '就活', 'MBTI', '悩み', '学部・専攻', '対面']
)
submit_btn = st.button('マッチング開始')

def matching():
    df_x = df_[df_['名前'] != name]
    df_y = df_[df_['名前'] == name]
    df_x['スコア'] = 0
    for i in range(len(df_x)):
        for j in range(2,len(df_column)):
            df_x['スコア'][i] = df_x['スコア'][i] + (df_x[df_column[j]][i] - df_y.iloc[0, j])

    result = df_x[['名前','スコア']]
    return result


if submit_btn:
    result = matching()
    st.dataframe(result)
    
data = {
    "都道府県": [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", 
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", 
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", 
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", 
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", 
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ],
    "県庁所在地": [
        "札幌市", "青森市", "盛岡市", "仙台市", "秋田市", "山形市", "福島市", 
        "水戸市", "宇都宮市", "前橋市", "さいたま市", "千葉市", "新宿区", "横浜市", 
        "新潟市", "富山市", "金沢市", "福井市", "甲府市", "長野市", "岐阜市", 
        "静岡市", "名古屋市", "津市", "大津市", "京都市", "大阪市", "神戸市", 
        "奈良市", "和歌山市", "鳥取市", "松江市", "岡山市", "広島市", "山口市", 
        "徳島市", "高松市", "松山市", "高知市", "福岡市", "佐賀市", "長崎市", 
        "熊本市", "大分市", "宮崎市", "鹿児島市", "那覇市"
    ],
    "lat": [
        43.06417, 40.82444, 39.70361, 38.26889, 39.71861, 38.24056, 37.75, 
        36.34139, 36.56583, 36.39111, 35.85694, 35.60472, 35.68944, 35.44778, 
        37.90222, 36.69528, 36.59444, 36.06528, 35.66389, 36.65139, 35.39111, 
        34.97694, 35.18028, 34.73028, 35.00444, 35.02139, 34.68639, 34.69139, 
        34.68528, 34.22611, 35.50361, 35.47222, 34.66167, 34.39639, 34.18583, 
        34.06583, 34.34028, 33.84167, 33.55972, 33.59028, 33.24944, 32.74472, 
        32.78972, 33.23806, 31.91111, 31.56028, 26.2125
    ],
    "lon": [
        141.34694, 140.74, 141.1525, 140.87194, 140.1025, 140.36333, 140.46778, 
        140.44667, 139.88361, 139.06083, 139.64889, 140.12333, 139.69167, 139.6425, 
        139.02361, 137.21139, 136.62556, 136.22194, 138.56833, 138.18111, 136.72222, 
        138.38306, 136.90667, 136.50861, 135.86833, 135.75556, 135.52, 135.19556, 
        135.83278, 135.1675, 134.23833, 133.05056, 133.93444, 132.45944, 131.47139, 
        134.55944, 134.04333, 132.76611, 133.53111, 130.40172, 130.29889, 129.87361, 
        130.74167, 131.6125, 131.42389, 130.55806, 127.68111
    ]
}

map_df = pd.DataFrame(data)
map_df["都道府県"] = pd.Categorical(map_df["都道府県"], categories=category_order, ordered=True)
map_df["都道府県"] = map_df["都道府県"].cat.codes
df_ = df_.merge(map_df, left_on='居住地', right_on='都道府県', how='left')

st.title('キャリツク生がいる場所')
st.write('※県庁所在地で表示されます。')
st.map(df_[['lat', 'lon']])
