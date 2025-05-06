import streamlit as st
import wave
import os
from tempfile import NamedTemporaryFile

def combine_multiple_wavs(file_paths, output_path):
    if not file_paths:
        raise ValueError("結合するファイルがありません。")

    with wave.open(file_paths[0], 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())

    with wave.open(output_path, 'wb') as output:
        output.setparams(params)
        output.writeframes(frames)

        for path in file_paths[1:]:
            with wave.open(path, 'rb') as wf:
                if wf.getparams() != params:
                    raise ValueError(f"{os.path.basename(path)} のフォーマットが一致しません。")
                frames = wf.readframes(wf.getnframes())
                output.writeframes(frames)

# Streamlit UI
st.title("WAVファイル一括結合アプリ")
st.write("複数のWAVファイルをアップロードすると、順番に結合されます。")

uploaded_files = st.file_uploader("WAVファイルをアップロード（複数選択可）", type=["wav"], accept_multiple_files=True)

if uploaded_files:
    tmp_paths = []

    try:
        # 各ファイルを一時ファイルに保存
        for file in uploaded_files:
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(file.read())
                tmp_paths.append(tmp.name)

        output_path = "output.wav"
        combine_multiple_wavs(tmp_paths, output_path)

        st.success("結合が完了しました！")

        with open(output_path, 'rb') as audio_file:
            st.audio(audio_file.read(), format='audio/wav')
            st.download_button("ダウンロード", audio_file, file_name="combined.wav")

    except ValueError as e:
        st.error(str(e))

    finally:
        # 一時ファイルを削除
        for path in tmp_paths:
            os.remove(path)
