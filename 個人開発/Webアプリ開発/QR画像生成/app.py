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
    overlay_img = overlay_img.putalpha(int(255 * 0.65))  # 65%の透明度
    qr_img.paste(overlay_img, position, overlay_img)
    return qr_img

def get_image_download_link(img, format):
    """ Convert image to byte stream for download """
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    return img_byte_arr

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
            
            # ユーザーが切り抜く位置を指定
            st.subheader("✂️ 切り抜く位置を指定")
            left = st.slider("左", 0, qr_image.width, 0)
            top = st.slider("上", 0, qr_image.height, 0)
            right = st.slider("右", 0, qr_image.width, qr_image.width)
            bottom = st.slider("下", 0, qr_image.height, qr_image.height)
            
            # 切り抜き処理
            overlay_cropped = transparent_img.crop((left, top, right, bottom))
            
            # 画像のサイズをQRコード画像に合わせる
            overlay_resized = overlay_cropped.resize((qr_image.width // 3, qr_image.height // 3), Image.ANTIALIAS)
            
            # QRコード画像の中心に配置
            width, height = qr_image.size
            pos_x = (width - overlay_resized.width) // 2
            pos_y = (height - overlay_resized.height) // 2
            combined_image = overlay_images(qr_image, overlay_resized, (pos_x, pos_y))
            
            # 出力画像を表示
            st.subheader("📌 合成結果")
            st.image(combined_image, caption="合成されたQRコード", use_column_width=True)
            
            # ダウンロードボタン
            st.subheader("💾 ダウンロード")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download as PNG", get_image_download_link(combined_image, "PNG"), "qr_image.png", "image/png")
            with col2:
                st.download_button("Download as JPG", get_image_download_link(combined_image, "JPEG"), "qr_image.jpg", "image/jpeg")
        else:
            st.warning("QRコード画像と重ねる画像の両方をアップロードしてください。")

if __name__ == "__main__":
    main()