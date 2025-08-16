import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings

st.set_page_config(
    page_title="kensan_remid2",
    page_icon="✅"
)

st.title("✅ LINEリマインダー")

st.write("下の「START」ボタンを押してから、LINEの画面を共有してください。")

# webrtc_streamerを使って画面共有を開始する
webrtc_ctx = webrtc_streamer(
    key="display-capture",
    mode=WebRtcMode.RECVONLY,
    client_settings=ClientSettings(
        media_stream_constraints={
            "video": True, # ここをTrueにすることで映像（画面）を取得する
            "audio": False, # 音声は不要なのでFalse
        },
        # getDisplayMediaを強制的に使用するように設定
        # これが画面共有のダイアログを出すための重要な設定
        display_surface="monitor",
    ),
    # 共有中の映像をアプリ上に表示するかどうか (デバッグ用にTrueにしておくと便利)
    video_receiver_size=1, 
    # 映像をPython側に送信しないので、recv_interval_msは設定不要
)

if webrtc_ctx.state.playing:
    st.success("画面のキャプチャを開始しました！")
    st.info("この画面を開いたまま、LINEアプリに切り替えてください。")
    # ここに将来、キャプチャした画像を処理するコードを追加していく
