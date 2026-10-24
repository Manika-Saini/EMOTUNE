
import io

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from src.avatar.live_avatar_processor import AvatarVideoProcessor
from src.portrait.cartoon_filters import create_cartoon
from src.portrait.video_processor import process_video


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EMOTUNE | Expressions in Motion",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "Home",
    "cartoon_result": None,
    "cartoon_source": None,
    "processed_video": None,
    "processed_video_name": None,
    "avatar_settings": {
        "style": "Anime Girl",
        "action": "Idle",
        "expression_mode": "Automatic",
        "manual_expression": "Happy",
    },
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def navigate_to(page_name):
    st.session_state["page"] = page_name


# =========================================================
# LIGHT THEME
# =========================================================

st.markdown(
    """
    <style>
        :root {
            color-scheme: light;
        }

        .stApp {
            background: #FAF9FF;
            color: #302541;
        }

        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }

        header[data-testid="stHeader"] {
            background: rgba(250, 249, 255, 0.95);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }

        .brand-title {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            color: #35245E;
            margin: 0;
        }

        .brand-tagline {
            font-size: 0.78rem;
            color: #827795;
            margin-top: 2px;
        }

        .hero {
            padding: clamp(1.5rem, 4vw, 3.4rem);
            border: 1px solid #E7DFFF;
            border-radius: 26px;
            background: linear-gradient(
                125deg,
                #F0E9FF 0%,
                #FFFFFF 58%,
                #F8EEFF 100%
            );
            margin: 1.4rem 0 2rem 0;
            box-shadow: 0 12px 40px rgba(91, 60, 155, 0.06);
        }

        .eyebrow,
        .section-label {
            color: #7552CC;
            font-size: 0.76rem;
            font-weight: 750;
            letter-spacing: 1.8px;
            text-transform: uppercase;
        }

        .hero h1 {
            color: #2D2248;
            font-size: clamp(2.2rem, 5vw, 4rem);
            line-height: 1.12;
            letter-spacing: -1.5px;
            margin: 1rem 0;
        }

        .gradient-text {
            color: #8055DB;
        }

        .hero p {
            color: #6F6682;
            font-size: 1rem;
            max-width: 740px;
            line-height: 1.85;
        }

        .feature-card {
            background: #FFFFFF;
            border: 1px solid #EAE4F4;
            border-radius: 20px;
            padding: 1.5rem;
            min-height: 205px;
            margin-bottom: 0.7rem;
            box-shadow: 0 6px 24px rgba(60, 40, 100, 0.045);
        }

        .feature-icon {
            font-size: 2rem;
        }

        .feature-card h3 {
            color: #35274F;
            margin: 0.8rem 0 0.5rem 0;
            font-size: 1.2rem;
        }

        .feature-card p {
            color: #756C86;
            line-height: 1.7;
            font-size: 0.94rem;
        }

        .info-panel {
            background: #F2EDFF;
            border: 1px solid #E2D6FF;
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin: 0.7rem 0 1.2rem 0;
        }

        .info-panel p {
            color: #62527F;
            line-height: 1.65;
            margin-bottom: 0;
        }

        .footer {
            color: #9489A8;
            text-align: center;
            padding-top: 2rem;
            font-size: 0.85rem;
        }

        h1, h2, h3, h4 {
            color: #302541;
        }

        hr {
            border-color: #E9E2F2;
        }

        div.stButton > button,
        div.stDownloadButton > button {
            border-radius: 12px;
            min-height: 44px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        div.stButton > button[kind="primary"],
        div.stDownloadButton > button[kind="primary"] {
            background: #7650D9;
            border: 1px solid #7650D9;
            color: #FFFFFF;
        }

        div.stButton > button[kind="primary"]:hover {
            background: #6240BD;
            border-color: #6240BD;
        }

        div.stButton > button[kind="secondary"],
        div.stDownloadButton > button[kind="secondary"] {
            background: #FFFFFF;
            border: 1px solid #E3DAF2;
            color: #514269;
        }

        div[data-testid="stFileUploader"] {
            background: #FFFFFF;
            border: 1px dashed #D8C9F2;
            border-radius: 16px;
            padding: 0.6rem;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }

        div[data-baseweb="select"] > div {
            border-radius: 10px;
            border-color: #E0D6F0;
            background: #FFFFFF;
        }

        div[data-testid="stImage"] img {
            border-radius: 14px;
        }

        @media (max-width: 768px) {
            .block-container {
                padding: 0.8rem 1rem 2rem 1rem;
            }

            .hero {
                padding: 1.4rem;
                border-radius: 18px;
            }

            .hero h1 {
                letter-spacing: -0.8px;
            }

            .feature-card {
                padding: 1.1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TOP NAVIGATION
# =========================================================

nav_items = [
    ("Home", "Home"),
    ("Live Studio", "Live Avatar Studio"),
    ("Video Studio", "Video Avatar Studio"),
    ("Portrait Lab", "Anime Portrait Lab"),
]

nav_cols = st.columns(
    [1.8, 1, 1.15, 1.15, 1.05],
    gap="small",
)

with nav_cols[0]:
    st.markdown(
        """
        <div style="padding-top:2px;">
            <div class="brand-title">EMOTUNE 🎭</div>
            <div class="brand-tagline">Expressions in Motion</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for index, (label, destination) in enumerate(nav_items, start=1):
    with nav_cols[index]:
        st.button(
            label,
            key=f"top_nav_{index}",
            type=(
                "primary"
                if st.session_state["page"] == destination
                else "secondary"
            ),
            use_container_width=True,
            on_click=navigate_to,
            args=(destination,),
        )

st.divider()

page = st.session_state["page"]


# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">YOUR CREATIVE SPACE</div>
            <h1>
                Bring your expressions to life.<br>
                <span class="gradient-text">Meet your anime self.</span>
            </h1>
            <p>
                Welcome to EMOTUNE — a creative computer vision
                experience where facial expressions meet anime
                characters and ordinary portraits become
                stylized art. Choose a studio and start creating.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">EXPLORE YOUR STUDIO</div>',
        unsafe_allow_html=True,
    )

    st.write("Choose what you would like to create today.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎭</div>
                <h3>Live Avatar Studio</h3>
                <p>
                    Use your webcam to detect facial expressions
                    and control your anime character in real time.
                    Choose a character, expression and action.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "Open Live Studio →",
            key="home_avatar",
            type="primary",
            use_container_width=True,
            on_click=navigate_to,
            args=("Live Avatar Studio",),
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3>Anime Portrait Lab</h3>
                <p>
                    Upload a photo, apply a cartoon effect,
                    compare the result with your original image,
                    and download your creation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "Create a Portrait →",
            key="home_portrait",
            use_container_width=True,
            on_click=navigate_to,
            args=("Anime Portrait Lab",),
        )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎞️</div>
                <h3>Video Avatar Studio</h3>
                <p>
                    Upload a video and process its frames
                    to create a cartoon-stylized video.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "Open Video Studio →",
            key="home_video",
            use_container_width=True,
            on_click=navigate_to,
            args=("Video Avatar Studio",),
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <h3>Made for creativity</h3>
                <p>
                    Explore computer vision, facial landmark
                    tracking and image processing in one
                    easy-to-use creative workspace.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("### How EMOTUNE works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**01 · Detect**")
        st.caption("Analyze facial landmarks and expressions.")

    with col2:
        st.markdown("**02 · Create**")
        st.caption("Choose your character and creative experience.")

    with col3:
        st.markdown("**03 · Transform**")
        st.caption("Preview your result and download your creation.")

    st.markdown(
        '<div class="footer">EMOTUNE · Expressions in Motion</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# LIVE AVATAR STUDIO
# =========================================================

elif page == "Live Avatar Studio":

    st.markdown("## Live Avatar Studio")
    st.caption(
        "Your expressions. Your character. Your creative space."
    )

    st.markdown(
        """
        <div class="info-panel">
            <p>
                Choose an anime character and action, then start
                your webcam to see facial expression detection
                in real time.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    settings = st.session_state["avatar_settings"]

    st.markdown("### Customize your character")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        avatar_style = st.selectbox(
            "Character",
            ["Anime Girl", "Anime Boy"],
            key="live_avatar_style",
        )

        action = st.selectbox(
            "Action",
            ["Idle", "Wave", "Dance", "Cry", "Talk"],
            key="live_avatar_action",
        )

    with col2:
        expression_mode = st.radio(
            "Expression control",
            ["Automatic", "Manual"],
            horizontal=True,
            key="live_expression_mode",
        )

        manual_expression = st.selectbox(
            "Choose an expression",
            [
                "Neutral",
                "Happy",
                "Surprised",
                "Sleepy",
                "Blinking",
                "Angry",
                "Sad",
                "Confused",
                "Laughing",
                "Talking",
            ],
            key="live_manual_expression",
            disabled=expression_mode != "Manual",
        )

    settings["style"] = avatar_style
    settings["action"] = action
    settings["expression_mode"] = expression_mode
    settings["manual_expression"] = manual_expression

    st.divider()
    st.markdown("### Live camera")

    st.info(
        "Press START and allow browser camera access. "
        "Keep this page open while the studio is running."
    )

    try:
        webrtc_streamer(
            key="emotune-live-avatar",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=lambda: AvatarVideoProcessor(
                settings
            ),
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
            async_processing=True,
        )
    except Exception as exc:
        st.error("Unable to initialize the live camera.")
        st.caption(str(exc))

    st.caption(
        "Automatic mode detects expressions from your face. "
        "Manual mode lets you choose an expression. "
        "Wave and Dance currently use static poses."
    )

    st.divider()
    st.markdown("### Getting started")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**01 · Choose**")
        st.caption("Select Anime Girl or Anime Boy.")

    with col2:
        st.markdown("**02 · Start**")
        st.caption("Enable your webcam.")

    with col3:
        st.markdown("**03 · Express**")
        st.caption("Try different expressions and actions.")


# =========================================================
# VIDEO AVATAR STUDIO
# =========================================================

elif page == "Video Avatar Studio":

    st.markdown("## Video Avatar Studio")

    st.caption(
        "Transform your uploaded video with EMOTUNE's "
        "cartoon frame-processing engine."
    )

    st.markdown(
        """
        <div class="info-panel">
            <p>
                This version stylizes video frames. Full facial
                tracking and anime avatar replacement are
                planned as a later enhancement.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_video = st.file_uploader(
        "Upload your video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_upload",
        help="Maximum size: 50 MB. Recommended duration: up to 120 seconds.",
    )

    if uploaded_video is not None:

        video_bytes = uploaded_video.getvalue()

        if len(video_bytes) > 50 * 1024 * 1024:
            st.error("Please upload a video smaller than 50 MB.")

        else:
            st.success(f"Video ready: {uploaded_video.name}")
            st.video(video_bytes)

            if st.button(
                "✨ Transform Video",
                type="primary",
                use_container_width=True,
            ):
                try:
                    with st.spinner(
                        "Processing video frames. Please wait..."
                    ):
                        processed_video = process_video(video_bytes)

                    st.session_state["processed_video"] = processed_video
                    st.session_state["processed_video_name"] = uploaded_video.name

                    st.success("Video processing completed!")

                except (ValueError, RuntimeError) as exc:
                    st.error(str(exc))

                except Exception as exc:
                    st.error("An unexpected error occurred during processing.")
                    st.caption(f"Details: {exc}")

            result = st.session_state.get("processed_video")

            if result is not None:
                st.divider()
                st.markdown("### Your processed video")
                st.video(result)

                st.download_button(
                    "⬇️ Download Processed Video",
                    data=result,
                    file_name="emotune_cartoon_video.mp4",
                    mime="video/mp4",
                    use_container_width=True,
                )

    else:
        st.caption(
            "Supported formats: MP4, MOV, AVI and MKV. "
            "Decoding support depends on your OpenCV installation."
        )


# =========================================================
# ANIME PORTRAIT LAB
# =========================================================

elif page == "Anime Portrait Lab":

    st.markdown("## Anime Portrait Lab")

    st.caption(
        "Transform a portrait, compare the result, and download your creation."
    )

    st.markdown(
        """
        <div class="info-panel">
            <p>
                Upload a JPG or PNG image to apply a cartoon-style
                effect. This version uses OpenCV image processing,
                not generative AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload your portrait",
        type=["jpg", "jpeg", "png"],
        key="portrait_upload",
        help="Maximum image size: 10 MB.",
    )

    if uploaded_file is not None:

        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("Please upload an image smaller than 10 MB.")

        else:
            try:
                uploaded_file.seek(0)

                original = ImageOps.exif_transpose(
                    Image.open(uploaded_file)
                ).convert("RGB")

                if original.width < 2 or original.height < 2:
                    raise ValueError("The image dimensions are invalid.")

                max_dimension = 1200

                if max(original.size) > max_dimension:
                    original.thumbnail(
                        (max_dimension, max_dimension),
                        Image.Resampling.LANCZOS,
                    )

                st.success(
                    f"Image ready · {original.width} × {original.height} px"
                )

                original_array = np.array(original)

                bgr_image = cv2.cvtColor(
                    original_array,
                    cv2.COLOR_RGB2BGR,
                )

                source_key = (
                    uploaded_file.name,
                    uploaded_file.size,
                )

                if st.session_state["cartoon_source"] != source_key:
                    st.session_state["cartoon_source"] = source_key
                    st.session_state["cartoon_result"] = None

                st.markdown("### Transformation settings")

                style = st.selectbox(
                    "Cartoon style",
                    ["Classic Cartoon"],
                    key="cartoon_style",
                )

                st.caption(
                    "Additional artistic and AI-based styles can be added later."
                )

                if st.button(
                    "✨ Generate Cartoon",
                    type="primary",
                    use_container_width=True,
                ):
                    with st.spinner("Transforming your portrait..."):
                        try:
                            result_bgr = create_cartoon(bgr_image)

                            result_rgb = cv2.cvtColor(
                                result_bgr,
                                cv2.COLOR_BGR2RGB,
                            )

                            st.session_state["cartoon_result"] = result_rgb

                        except (ValueError, cv2.error) as exc:
                            st.session_state["cartoon_result"] = None
                            st.error(f"Could not transform the image: {exc}")

                result = st.session_state["cartoon_result"]

                if result is not None:
                    st.divider()
                    st.markdown("### Your result")

                    before_col, after_col = st.columns(2, gap="large")

                    with before_col:
                        st.markdown("**Original portrait**")
                        st.image(
                            original,
                            use_container_width=True,
                        )

                    with after_col:
                        st.markdown(f"**{style}**")
                        st.image(
                            result,
                            use_container_width=True,
                        )

                    output_image = Image.fromarray(result)
                    buffer = io.BytesIO()
                    output_image.save(buffer, format="PNG")

                    st.download_button(
                        "⬇️ Download Cartoon PNG",
                        data=buffer.getvalue(),
                        file_name="emotune_cartoon.png",
                        mime="image/png",
                        use_container_width=True,
                    )

            except (
                UnidentifiedImageError,
                OSError,
                ValueError,
            ) as exc:
                st.error(
                    "This image could not be opened. "
                    "Please upload a valid JPG or PNG."
                )
                st.caption(f"Details: {exc}")

            except Exception as exc:
                st.error("Something went wrong while preparing the image.")
                st.caption(f"Details: {exc}")

    else:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🖼️</div>
                <h3>Your portrait starts here</h3>
                <p>
                    Upload a JPG or PNG portrait to create
                    your first cartoon-style image.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<div class="footer">EMOTUNE · Your face. Your character. Your vibe.</div>',
        unsafe_allow_html=True,
    )