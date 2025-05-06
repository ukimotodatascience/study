import streamlit as st
from pydub import AudioSegment
from io import BytesIO
import streamlit_sortables as sortables

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

# Streamlit UI
st.title("WAVファイル一括結合アプリ（並び替え対応）")
st.write("WAVファイルをアップロードし、結合順をドラッグで並び替えてください。")

uploaded_files = st.file_uploader("WAVファイルをアップロード（複数選択可）", type=["wav"], accept_multiple_files=True)

if uploaded_files:
    # ファイル情報のリストを作成
    file_data_list = [{"label": file.name, "file": file} for file in uploaded_files]

    # 並び替えUI
    sorted_items = sortables.sort_items(
        [item["label"] for item in file_data_list],
        direction="vertical",
        label="ドラッグで順序を変更できます：",
    )

    # 並び替えられた順でファイルデータを再構成
    sorted_file_data = [next(item for item in file_data_list if item["label"] == label) for label in sorted_items]

    # 結合処理
    try:
        output_buffer = combine_wav_files_pydub(sorted_file_data)
        st.success("結合が完了しました！")
        st.audio(output_buffer, format='audio/wav')
        st.download_button("ダウンロード", output_buffer, file_name="combined.wav", mime="audio/wav")

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")



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
