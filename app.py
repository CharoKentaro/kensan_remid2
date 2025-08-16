import streamlit as st
from PIL import Image
import google.generativeai as genai
import json
import time

# ---------------------------------------------------------------
# アプリの基本設定
# ---------------------------------------------------------------
st.set_page_config(
    page_title="kensan_remid2",
    page_icon="✅"
)

# ---------------------------------------------------------------
# サイドバー: APIキーの設定
# ちゃろさんのコードを参考に、このアプリ用に簡略化して実装
# ---------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ 設定")
    st.divider()

    # st.session_stateにAPIキーがなければ初期化
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ''

    # st.expander内でフォームを作成
    with st.expander("APIキーの設定", expanded=(not st.session_state.gemini_api_key)):
        with st.form("api_key_form"):
            # テキスト入力欄でAPIキーを求める
            api_key_input = st.text_input(
                "Gemini APIキー", 
                type="password", 
                value=st.session_state.gemini_api_key,
                placeholder="ここにAPIキーを貼り付けてください"
            )
            
            # 保存ボタンとクリアボタンを横並びに配置
            col1, col2 = st.columns(2)
            with col1:
                save_button = st.form_submit_button("💾 保存", use_container_width=True)
            with col2:
                reset_button = st.form_submit_button("🔄 クリア", use_container_width=True)

    # 保存ボタンが押されたときの処理
    if save_button:
        st.session_state.gemini_api_key = api_key_input
        st.success("APIキーを保存しました！")
        time.sleep(1)
        st.rerun() # 画面を再読み込みして設定を反映

    # クリアボタンが押されたときの処理
    if reset_button:
        st.session_state.gemini_api_key = ''
        st.info("APIキーをクリアしました。")
        time.sleep(1)
        st.rerun()

# ---------------------------------------------------------------
# メイン画面
# ---------------------------------------------------------------
st.title("✅ LINEリマインダー")
st.subheader("LINEのスクリーンショットから返信内容を忘れないようにします")

# APIキーが設定されているか確認
api_key = st.session_state.gemini_api_key
if not api_key:
    st.warning("サイドバーの「⚙️ 設定」からGemini APIキーを設定してください。")
    st.stop() # APIキーがなければ、ここで処理を中断

# --- ファイルアップローダー ---
uploaded_file = st.file_uploader(
    "下のボタンから、先ほど撮影したスクリーンショットを選択してください。", 
    type=['png', 'jpg', 'jpeg']
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="読み込んだスクリーンショット", width=300)
    
    # --- AI解析ボタン ---
    if st.button("この内容でリマインダーを作成", type="primary", use_container_width=True):
        with st.spinner("🧠 AIが画像を解析し、カレンダー登録内容を作成しています..."):
            try:
                # Gemini APIの設定
                genai.configure(api_key=api_key)
                
                # ちゃろさんご指定のモデルを使用
                model = genai.GenerativeModel('gemini-1.5-flash-latest')

                # AIへの指示プロンプト
                prompt = """
                あなたは、非常に優秀な秘書です。
                このLINEのトーク画面の画像から、「誰に」「何を」返信または対応する必要があるかを正確に読み取ってください。
                そして、Googleカレンダーに登録するための情報を、以下のJSON形式で出力してください。

                # 指示
                1.  **title**: カレンダーの予定のタイトルです。「【LINE返信】〇〇さんへ」のように、誰への返信か分かるように簡潔にまとめてください。
                2.  **description**: カレンダーの予定の詳細です。返信すべき内容の要点や、元の会話の要約を、分かりやすく記述してください。

                # 出力形式 (JSON以外の説明は絶対に含めないこと)
                {
                  "title": "ここにカレンダーのタイトル",
                  "description": "ここにカレンダーの詳細説明"
                }
                """

                # モデルに画像とプロンプトを渡して解析を実行
                response = model.generate_content([prompt, image])
                
                # AIの応答からJSON部分だけを抽出
                raw_text = response.text.strip()
                json_start = raw_text.find('{')
                json_end = raw_text.rfind('}') + 1
                clean_json_text = raw_text[json_start:json_end]
                
                # JSONを辞書型に変換
                result_data = json.loads(clean_json_text)
                
                # 解析結果を画面に表示
                st.success("AIによる解析が完了しました！")
                st.subheader("🗓️ カレンダー登録内容（案）")
                with st.container(border=True):
                    st.text_input("タイトル案", value=result_data.get("title", "取得失敗"), disabled=True)
                    st.text_area("詳細説明案", value=result_data.get("description", "取得失敗"), height=200, disabled=True)

                # --- ここから次のステップ ---
                # 将来的には、このresult_dataをGoogle Calendar APIに渡して
                # 実際にカレンダーへ登録する処理を追加します。
                # st.info("（次のステップで、実際にカレンダーへ登録する機能を追加します）")
                # -------------------------

            except Exception as e:
                st.error(f"AIの解析中にエラーが発生しました: {e}")
                st.error("もう一度試すか、別の画像でお試しください。")
