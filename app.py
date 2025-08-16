import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import threading
from PIL import Image

st.set_page_config(
    page_title="kensan_remid2",
    page_icon="✅"
)

st.title("✅ LINEリマインダー")

# -------------------------------------------------------------------
# (修正) 最新のキャプチャ画像をセッション状態で保持するように変更
# これにより、ページが再読み込みされても画像が消えなくなる
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None
# -------------------------------------------------------------------

# (修正) video_frame_callbackをクラスベースに変更し、より安定させる
class VideoProcessor:
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # 新しいフレームをPillow画像に変換
        image = frame.to_image()
        # セッション状態に最新の画像を保存
        st.session_state.captured_image = image
        return frame

st.info("下の「START」ボタンを押して画面共有を開始してください。")

webrtc_ctx = webrtc_streamer(
    key="display-capture",
    mode=WebRtcMode.RECVONLY,
    # (修正) video_processor_factoryを使ってクラスを渡す
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    # プレビュー表示は不要なのでコメントアウト（または削除）
    # video_html_attrs={ ... },
)

if webrtc_ctx.state.playing:
    st.success("画面共有中...")
    st.info("LINEアプリに切り替え、リマインドしたい画面を表示してください。表示したら、この画面に戻ってきて下のボタンを押してください。")
    
    # -------------------------------------------------------------------
    # (修正) ボタンの役割を変更
    # -------------------------------------------------------------------
    if st.button("この画面でリマインダー作成！", type="primary"):
        # セッション状態から最新の画像を取得
        final_image = st.session_state.captured_image

        if final_image:
            st.subheader("直前にキャプチャされた画面：")
            st.image(final_image, caption="この画像をAIが解析します", use_column_width=True)

            with st.spinner("AIが解析中です..."):
                # --- ここからステップ3 ---
                # ここに、取得した final_image をGemini APIに渡すコードを
                # 将来的に追加していきます。
                # result = gemini_process_image(final_image)
                # st.write(result)
                pass # 今はまだ何もしない
            # -------------------------
        else:
            st.warning("まだ画像を取得できていません。画面共有が開始されていることを確認してください。")

else:
    st.warning("「START」ボタンを押して画面共有の許可をしてください。")
