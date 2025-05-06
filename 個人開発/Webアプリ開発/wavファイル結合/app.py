import streamlit as st
from pydub import AudioSegment
from io import BytesIO

def combine_wav_files_pydub(file_data_list, target_format="wav"):
    combined = AudioSegment.empty()

    for file_data in file_data_list:
        file = file_data["file"]
        audio = AudioSegment.from_file(file, format="wav")
        audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
        combined += audio

    buffer = BytesIO()
    combined.export(buffer, format=target_format)
    buffer.seek(0)
    return buffer

st.title("WAVファイル一括結合アプリ（順序指定付き）")

uploaded_files = st.file_uploader(
    "WAVファイルをアップロード（複数選択可）", type=["wav"], accept_multiple_files=True
)

if uploaded_files:
    # 初期ファイル順を記録
    st.write("アップロードされたファイル：")
    filenames = [file.name for file in uploaded_files]
    for i, name in enumerate(filenames):
        st.write(f"{i+1}. {name}")

    # 並び順を決める
    st.write("ファイルを結合する順番を指定してください：")
    selected_order = st.multiselect(
        "順番にファイルを選択してください（すべて選んでください）",
        options=filenames,
        default=filenames,
    )

    if len(selected_order) == len(filenames):
        file_data_list = [{"label": f.name, "file": f} for f in uploaded_files]
        sorted_file_data = [next(item for item in file_data_list if item["label"] == name) for name in selected_order]

        try:
            output_buffer = combine_wav_files_pydub(sorted_file_data)
            st.success("結合が完了しました！")
            st.audio(output_buffer, format='audio/wav')
            st.download_button("ダウンロード", output_buffer, file_name="combined.wav", mime="audio/wav")

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("すべてのファイルを順番に選択してください。")

# import streamlit as st
# from pydub import AudioSegment
# import os
# from tempfile import NamedTemporaryFile

# def combine_wav_files_pydub(uploaded_files, output_path, target_format="wav"):
#     combined = AudioSegment.empty()

#     for file in uploaded_files:
#         audio = AudioSegment.from_file(file, format="wav")

#         # 任意で全ファイルを統一フォーマット（例: モノラル/16bit/44.1kHz）に変換
#         audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)

#         combined += audio

#     combined.export(output_path, format=target_format)

# # Streamlit UI
# st.title("WAVファイル一括結合アプリ（フォーマット自動統一）")
# st.write("複数のWAVファイルをアップロードすると、自動でフォーマットを統一して順番に結合します。")

# uploaded_files = st.file_uploader("WAVファイルをアップロード（複数選択可）", type=["wav"], accept_multiple_files=True)

# if uploaded_files:
#     with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_output:
#         output_path = tmp_output.name

#     try:
#         combine_wav_files_pydub(uploaded_files, output_path)
#         st.success("結合が完了しました！")

#         with open(output_path, 'rb') as audio_file:
#             st.audio(audio_file.read(), format='audio/wav')
#             st.download_button("ダウンロード", audio_file, file_name="combined.wav")

#     except Exception as e:
#         st.error(f"エラーが発生しました: {str(e)}")

#     finally:
#         if os.path.exists(output_path):
#             os.remove(output_path)
