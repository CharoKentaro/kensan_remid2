import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.set_page_config(
    page_title="kensan_remid2",
    page_icon="✅"
)

st.title("✅ LINEリマインダー")

st.info("下の「START」ボタンを押して画面共有を開始してください。")

# webrtc_streamerを使って画面共有を開始する
webrtc_ctx = webrtc_streamer(
    key="display-capture",
    mode=WebRtcMode.RECVONLY,
    # ClientSettingsを使わず、直接引数として設定を渡す
    media_stream_constraints={
        "video": True,
        "audio": False,
    },
    # getDisplayMediaを強制的に使用するように設定
    # これが画面共有のダイアログを出すための重要な設定
    video_html_attrs={
        "style": {"width": "100%", "border": "1px solid #ccc", "border-radius": "5px"},
        "autoplay": True, 
        "controls": False,
    },
)

if webrtc_ctx.state.playing:
    st.success("画面のキャプチャを開始しました！")
    st.info("このままLINEアプリに切り替えて、リマインドしたい画面を表示してください。")
    # ここに将来、キャプチャした画像を処理するコードを追加していく

else:
    st.warning("「START」ボタンを押して画面共有の許可をしてください。")
