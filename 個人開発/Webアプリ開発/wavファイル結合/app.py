import streamlit as st
import wave
import os
from tempfile import NamedTemporaryFile

def combine_wav_files(opening_path, user_path, closing_path, output_path):
    # opening, user, closing の順で結合
    with wave.open(opening_path, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())

    with wave.open(output_path, 'wb') as output:
        output.setparams(params)
        output.writeframes(frames)

        for path in [user_path, closing_path]:
            with wave.open(path, 'rb') as wf:
                if wf.getparams() != params:
                    raise ValueError(f"{path} のフォーマットが一致しません。")
                frames = wf.readframes(wf.getnframes())
                output.writeframes(frames)

# Streamlit UI
st.title("WAVファイル結合アプリ")
st.write("オープニングトークとクロージングトークの間に、あなたの音声を挿入します。")

uploaded_file = st.file_uploader("WAVファイルをアップロードしてください", type=["wav"])

if uploaded_file is not None:
    # 開始・終了トークのパス
    opening_path = "opening.wav"
    closing_path = "closing.wav"

    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input_path = tmp_input.name

    output_path = "output.wav"

    try:
        combine_wav_files(opening_path, tmp_input_path, closing_path, output_path)
        st.success("結合が完了しました！")

        with open(output_path, 'rb') as audio_file:
            st.audio(audio_file.read(), format='audio/wav')
            st.download_button("ダウンロード", audio_file, file_name="combined.wav")

    except ValueError as e:
        st.error(str(e))

    finally:
        os.remove(tmp_input_path)
