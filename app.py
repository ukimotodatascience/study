#【超簡単Webアプリ】streamlitでWebアプリを最速で作ってネット公開！〜 プログラミング初心者向け 〜
#https://www.youtube.com/watch?v=4nsTce1Oce8&list=WL&index=6

import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import matplotlib.pyplot as plt

#テキスト関連
st.title('サプーアプリ')
st.caption('これはサプーの動画用のテストアプリです')

col1, col2 = st.columns(2)

with col1:
    #テキスト
    st.subheader('自己紹介')
    st.text('Pythonに関する情報をYouTube上で発信しているPython VTuber サプーです\n'
            'よければチャンネル登録よろしくお願いします！')
    code = '''
    import streamlit as st

    st.title('サプーアプリ')
    '''
    st.code(code, language='python')

    #画像
    # image = Image.open('サプー_デフォルメ1.png')
    # st.image(image, width=200)

    #動画
    # video_file = open('サプーTwitter動画.mov', 'rb')
    # video_bytes = video_file.read()
    # st.video(video_bytes)

    with st.form(key='profile_form'):
        #テキストボックス
        name = st.text_input('名前')
        address = st.text_input('住所')

        # age_category = st.selectbox(
        #     '年齢層',
        #     ('子ども(18才未満)', '大人(18才以上)'))
        
        age_category = st.radio(
            '年齢層',
            ('子ども(18才未満)', '大人(18才以上)'))
        
        #複数選択
        hobby = st.multiselect(
            '趣味',
            ('スポーツ','読書','プログラミング','アニメ・映画','釣り','料理'))
        
        #チェックボックス
        mail_subscribe = st.checkbox('メールマガジンを購読する')
        
        #スライダー
        height = st.slider('身長', min_value=110, max_value=210)
        
        #日付
        start_date = st.date_input(
            '開始日',
            datetime.date(2022,7,1))
        
        #カラーピッカー
        color = st.color_picker('テーマカラー', '#00f900')

        #ボタン
        submit_btn = st.form_submit_button('送信')
        cancel_btn = st.form_submit_button('キャンセル')

        if submit_btn:
            st.text(f'ようこそ！{name}さん！{address}に書籍を送りました！')
            st.text(f'年齢層: {age_category}')
            st.text(f'趣味: {", ".join(hobby)}')
    
# with col2:
    #データ分析関連
    # df = pd.read_csv('平均気温.csv', index_col='月')
    # st.dataframe(df)
    # st.table(df)
    # st.line_chart(df)
    # st.bar_chart(df['2021年'])

    #maplotlib
    # fig, ax = plt.subplots()
    # ax.plot(df.index), df['2021年']
    # ax.set_title('matplotlib graph')
    # st.pyplot(fig)