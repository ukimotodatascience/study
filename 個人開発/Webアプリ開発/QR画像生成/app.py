import streamlit as st
from PIL import Image, ImageOps
import io
import numpy as np
import cv2
from rembg import remove

def make_transparent(image):
    """ Convert white background to transparent """
    image = remove(image)
    return image

def overlay_images(qr_img, overlay_img, position):
    """ Overlay an image on top of a QR code at a given position """
    qr_img = qr_img.convert("RGBA")
    overlay_img = overlay_img.convert("RGBA")
    
    # 透明度を設定
    overlay_img.putalpha(int(255 * 0.65))  # 65%の透明度
    # 位置がQRコードの範囲内にあることを確認
    if position[0] < 0 or position[1] < 0 or position[0] + overlay_img.width > qr_img.width or position[1] + overlay_img.height > qr_img.height:
        raise ValueError("Overlay position is out of bounds.")
    
    qr_img.paste(overlay_img, position, overlay_img)
    return qr_img

def get_image_download_link(img, format):
    """ Convert image to byte stream for download """
    img_byte_arr = io.BytesIO()
    
    # 画像形式に応じて処理を分ける
    if format == "JPEG":
        img = img.convert("RGB")  # JPEG用にRGBに変換
    elif format == "PNG":
        img = img.convert("RGBA")  # PNG用にRGBAを維持
    
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    return img_byte_arr

# def get_image_download_link(img, format):
#     """ Convert image to byte stream for download """
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format=format)
#     img_byte_arr.seek(0)
#     return img_byte_arr

def main():
    st.set_page_config(page_title="QR Image Combiner", layout="centered")
    st.title("📸 QRコード合成アプリ")
    
    # ファイルアップロード
    uploaded_qr = st.file_uploader("QRコード画像をアップロード", type=["png", "jpg", "jpeg"])
    uploaded_img = st.file_uploader("重ねる画像をアップロード", type=["png", "jpg", "jpeg"])
    
    # 合成ボタンを追加
    if st.button("QR画像生成"):
        if uploaded_qr and uploaded_img:
            qr_image = Image.open(uploaded_qr).convert("RGBA")
            overlay_image = Image.open(uploaded_img).convert("RGBA")
            
            # 透過処理
            st.subheader("📏 画像の背景透過処理")
            transparent_img = make_transparent(overlay_image)
            
            # QR画像のサイズを取得
            qr_width, qr_height = qr_image.size
            
            # 重ねる画像のサイズをQR画像のサイズに合わせる
            overlay_resized = transparent_img.resize((qr_width, qr_height), Image.ANTIALIAS)
                                    
            # QRコード画像の左上に配置
            pos_x = 0
            pos_y = 0
            combined_image = overlay_images(qr_image, overlay_resized, (pos_x, pos_y))
            
            # 出力画像を表示
            st.subheader("📌 合成結果")
            st.image(combined_image, caption="合成されたQRコード", use_column_width=True)
            
            # ダウンロードボタン
            st.subheader("💾 ダウンロード")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download as PNG"):
                    st.download_button("Download as PNG", get_image_download_link(combined_image, "PNG"), "qr_image.png", "image/png")
            with col2:
                if st.button("Download as JPG"):
                    st.download_button("Download as JPG", get_image_download_link(combined_image, "JPEG"), "qr_image.jpg", "image/jpeg")
        else:
            st.warning("QRコード画像と重ねる画像の両方をアップロードしてください。")

if __name__ == "__main__":
    main()