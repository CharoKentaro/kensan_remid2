import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="kensan_remid2",
    page_icon="✅"
)

st.title("✅ LINEリマインダー")
st.subheader("LINEのスクリーンショットを登録します")

# ファイルアップローダーを設置
# labelには、ユーザーへの指示を分かりやすく書く
uploaded_file = st.file_uploader(
    "下のボタンから、先ほど撮影したスクリーンショットを選択してください。", 
    type=['png', 'jpg', 'jpeg'] # 受け付けるファイル形式を指定
)

# ファイルがアップロードされたら、以下の処理を実行
if uploaded_file is not None:
    # アップロードされたファイルをPillowを使って画像として開く
    image = Image.open(uploaded_file)
    
    st.subheader("読み込んだスクリーンショット：")
    # 読み込んだ画像を表示
    st.image(image, caption="この画像をAIに渡して、カレンダーに登録します。")
    
    # AI処理とカレンダー登録を行うボタン
    if st.button("この内容でリマインダーを作成", type="primary"):
        with st.spinner("AIが解析し、カレンダーに登録しています..."):
            # --- ここから次のステップ ---
            # ここに、画像(image)をGemini APIに渡し、
            # 結果をGoogle Calendar APIに送るコードを書いていきます。
            
            # (仮の成功メッセージ)
            st.success("カレンダーへの登録が完了しました！")
            st.balloons()
            # -------------------------
