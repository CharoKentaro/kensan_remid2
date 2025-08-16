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
# ステップ2で追加した部分 START
# -------------------------------------------------------------------

# 最新のビデオフレームを安全に保持するための箱を用意
# (threading.Lockを使って、複数の処理が同時にフレームを書き換えないようにする)
class VideoFrameHolder:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

    def get(self):
        with self.lock:
            return self.frame

    def set(self, frame):
        with self.lock:
            self.frame = frame

# VideoFrameHolderのインスタンス（実体）を作成
frame_holder = VideoFrameHolder()

# webrtc_streamerから新しいビデオフレームが届くたびに呼び出される関数
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    # フレームをPillowライブラリで扱える画像形式に変換
    image = frame.to_image()
    # 最新の画像を箱（frame_holder）に保存する
    frame_holder.set(image)
    return frame # このreturnは、画面共有の映像表示に必要

# -------------------------------------------------------------------
# ステップ2で追加した部分 END
# -------------------------------------------------------------------


st.info("下の「START」ボタンを押して画面共有を開始してください。")

webrtc_ctx = webrtc_streamer(
    key="display-capture",
    mode=WebRtcMode.RECVONLY,
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    # 重要な追加：ビデオフレームが届くたびに video_frame_callback関数を呼び出すように設定
    video_frame_callback=video_frame_callback,
    # 共有画面のプレビュー表示はデバッグに便利なので残しておく
    video_html_attrs={
        "style": {"width": "50%", "margin": "0 auto", "border": "1px solid #ccc", "border-radius": "5px"},
        "autoplay": True,
        "controls": False,
    },
)

if webrtc_ctx.state.playing:
    st.success("画面の共有が開始されました！")
    st.info("LINEアプリに切り替えて、リマインドしたい画面を表示してください。")

    # -------------------------------------------------------------------
    # ステップ2で追加した部分 START
    # -------------------------------------------------------------------

    # キャプチャボタンを設置
    if st.button("この画面をキャプチャ！", type="primary"):
        # 箱から最新の画像を取得
        captured_image = frame_holder.get()

        if captured_image:
            st.subheader("キャプチャした画像：")
            st.image(captured_image, caption="この画像をAIが解析します", use_column_width=True)
            
            # --- ここからステップ3 ---
            # ここに、取得した captured_image をGemini APIに渡すコードを
            # 将来的に追加していきます。
            # with st.spinner("AIが解析中です..."):
            #     # result = gemini_process_image(captured_image)
            #     # st.write(result)
            # -------------------------

        else:
            st.warning("まだ映像が届いていません。少し待ってから再度お試しください。")

    # -------------------------------------------------------------------
    # ステップ2で追加した部分 END
    # -------------------------------------------------------------------

else:
    st.warning("「START」ボタンを押して画面共有の許可をしてください。")
