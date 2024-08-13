import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# タイトル
st.title('輪郭抽出')

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 画像を開く
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)

    # スライダーでCannyの閾値を調整
    low_threshold = st.slider('Threshold1 (小さいほど線に隣接している部分が線になりやすい)', 0, 800, 300)
    high_threshold = st.slider('Threshold2 (小さいほど線が増える)', 0, 800, 500)

    # PIL画像をnumpy配列に変換
    img_array = np.array(image)

    # グレースケールに変換
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    # Cannyエッジ検出
    edges = cv2.Canny(gray, low_threshold, high_threshold)

    # 白黒反転
    inverted_edges = cv2.bitwise_not(edges)

    # 画像を表示
    st.image(inverted_edges, caption='輪郭抽出された画像', use_column_width=True)

    # 画像のダウンロード準備
    result_image = Image.fromarray(inverted_edges)
    buf = io.BytesIO()
    result_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # ダウンロードリンクの作成
    # ボタンは中央に寄せる
    st.download_button(
        label="画像をダウンロード",
        data=byte_im,
        file_name="processed_image.png",
        mime="image/png"
    )