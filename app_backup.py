
import io
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from src.avatar.live_avatar_processor import AvatarVideoProcessor
import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

from src.portrait.cartoon_filters import create_cartoon
from src.portrait.video_processor import process_video

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EMOTUNE | Expressions in Motion",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if "cartoon_result" not in st.session_state:
    st.session_state["cartoon_result"] = None

if "cartoon_source" not in st.session_state:
    st.session_state["cartoon_source"] = None


def navigate_to(page_name):
    st.session_state["page"] = page_name


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                #0b0a13 0%,
                #141023 55%,
                #0c0b15 100%
            );
            color: #f4f0ff;
        }

        [data-testid="stSidebar"] {
            background: #100d1c;
            border-right: 1px solid #302344;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .hero {
            padding: 2.5rem;
            border: 1px solid #44315f;
            border-radius: 24px;
            background: linear-gradient(
                120deg,
                #24163d 0%,
                #171126 65%,
                #21132f 100%
            );
            margin-bottom: 1.5rem;
        }

        .eyebrow {
            color: #c4a5ff;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .hero h1 {
            color: #ffffff;
            font-size: clamp(2.4rem, 6vw, 4.3rem);
            line-height: 1.1;
            margin: 0.7rem 0;
        }

        .gradient-text {
            color: #c4a5ff;
        }

        .hero p {
            color: #d0c7e2;
            font-size: 1.05rem;
            max-width: 720px;
            line-height: 1.8;
        }

        .feature-card {
            background: #171324;
            border: 1px solid #352747;
            border-radius: 18px;
            padding: 1.5rem;
            min-height: 210px;
            margin-bottom: 0.8rem;
        }

        .feature-icon {
            font-size: 2rem;
        }

        .feature-card h3 {
            color: #f4edff;
            margin: 0.8rem 0 0.5rem 0;
        }

        .feature-card p {
            color: #c0b6d3;
            line-height: 1.65;
        }

        .section-label {
            color: #c4a5ff;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            font-size: 0.78rem;
        }

        .footer {
            color: #9186a6;
            text-align: center;
            padding-top: 2rem;
            font-size: 0.85rem;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        div[data-testid="stFileUploader"] {
            border-radius: 14px;
        }

        div.stButton > button,
        div.stDownloadButton > button {
            border-radius: 10px;
            min-height: 42px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

pages = [
    "Home",
    "Live Avatar Studio",
    "Video Avatar Studio",
    "Anime Portrait Lab",
]

with st.sidebar:
    st.markdown("## 🎭 EMOTUNE")
    st.caption("Expressions in Motion.")
    st.divider()

    st.radio(
        "NAVIGATION",
        pages,
        key="page",
        label_visibility="visible",
    )

    st.divider()

    st.caption("YOUR FACE. YOUR CHARACTER. YOUR VIBE.")
    st.caption("Computer Vision • Creative Expression")


page = st.session_state["page"]


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">
                YOUR DIGITAL IDENTITY, REIMAGINED
            </div>

            <h1>
                Meet your anime self.<br>
                <span class="gradient-text">
                    Express every emotion.
                </span>
            </h1>

            <p>
                Welcome to EMOTUNE — a creative computer vision
                experience where facial expressions meet animated
                characters and ordinary portraits become
                stylized art.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">EXPLORE EMOTUNE</div>',
        unsafe_allow_html=True,
    )

    st.write("Choose an experience to get started.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎬</div>
                <h3>Live Avatar Studio</h3>
                <p>
                    Bring an anime character to life with facial
                    movement tracking, expression detection,
                    and responsive 2D animation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "Explore Live Avatar Studio →",
            key="home_avatar",
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
                    Upload a portrait, apply a cartoon effect,
                    preview the transformation, and download
                    your result.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "Explore Anime Portrait Lab →",
            key="home_portrait",
            use_container_width=True,
            on_click=navigate_to,
            args=("Anime Portrait Lab",),
        )

    st.divider()
    st.markdown("### Built around creative expression")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**01 · Detect**")
        st.caption("Analyze facial landmarks and movements.")

    with col2:
        st.markdown("**02 · Animate**")
        st.caption("Map expressions to an animated character.")

    with col3:
        st.markdown("**03 · Transform**")
        st.caption("Apply cartoon effects to your portrait.")

    st.markdown(
        '<div class="footer">'
        'EMOTUNE · Expressions in Motion.'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# LIVE AVATAR STUDIO
# =========================================================

elif page == "Live Avatar Studio":

    st.markdown("## 🎬 Live Avatar Studio")

    st.write(
        "Control your anime character with live facial "
        "expression detection."
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>✨ Your expressions. Your anime character.</h3>
            <p>
                Allow camera access, choose your character,
                and see your facial expressions detected live.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Persistent settings shared with the video processor.
    if "avatar_settings" not in st.session_state:
        st.session_state["avatar_settings"] = {
            "style": "Anime Girl",
            "action": "Idle",
            "expression_mode": "Automatic",
            "manual_expression": "Happy",
        }

    settings = st.session_state["avatar_settings"]

    st.markdown("### 🎨 Character customization")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        avatar_style = st.selectbox(
            "Choose your character",
            ["Anime Girl", "Anime Boy"],
            key="live_avatar_style",
        )

        action = st.selectbox(
            "Choose an action",
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
            "Manual expression",
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

    # Update the existing dictionary so the running
    # video processor can read the latest selections.
    settings["style"] = avatar_style
    settings["action"] = action
    settings["expression_mode"] = expression_mode
    settings["manual_expression"] = manual_expression

    st.divider()

    st.markdown("### 📹 Live camera and avatar")

    st.info(
        "Click START to enable your webcam. Your browser "
        "will ask for camera permission. Keep this page open "
        "while the live studio is running."
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
        "Automatic mode uses detected facial expressions. "
        "Manual mode lets you select an expression. "
        "Wave and Dance currently use static poses, not "
        "continuous animation."
    )

    st.divider()

    st.markdown("### 💡 How to use")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**01 · Select**")
        st.caption("Choose Anime Girl or Anime Boy.")

    with col2:
        st.markdown("**02 · Start**")
        st.caption("Click START and allow webcam access.")

    with col3:
        st.markdown("**03 · Express**")
        st.caption("Change expressions and actions using the controls.")


# =========================================================
# VIDEO AVATAR STUDIO
# =========================================================

elif page == "Video Avatar Studio":

    st.markdown("## 🎞️ Video Avatar Studio")

    st.write(
        "Upload a video and create a cartoon-stylized version "
        "using EMOTUNE's frame-processing engine."
    )

    st.info(
        "This first version stylizes video frames. "
        "Facial tracking and anime avatar replacement "
        "will be added in a later phase."
    )

    uploaded_video = st.file_uploader(
        "Upload a video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_upload",
        help="Maximum 50 MB and 120 seconds.",
    )

    if uploaded_video is not None:

        video_bytes = uploaded_video.getvalue()

        if len(video_bytes) > 50 * 1024 * 1024:
            st.error("Please upload a video smaller than 50 MB.")

        else:
            st.success(
                f"Uploaded: {uploaded_video.name}"
            )

            st.video(video_bytes)

            if st.button(
                "✨ Transform Video",
                type="primary",
                use_container_width=True,
            ):

                try:
                    with st.spinner(
                        "Processing video frames. "
                        "This may take a little while..."
                    ):
                        processed_video = process_video(
                            video_bytes
                        )

                    st.session_state["processed_video"] = (
                        processed_video
                    )

                    st.session_state["processed_video_name"] = (
                        uploaded_video.name
                    )

                    st.success("Video processing completed!")

                except (ValueError, RuntimeError) as exc:
                    st.error(str(exc))

                except Exception as exc:
                    st.error(
                        "An unexpected error occurred "
                        "while processing the video."
                    )
                    st.caption(f"Details: {exc}")

            result = st.session_state.get("processed_video")

            if result is not None:
                st.markdown("### Your cartoon video")

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
            "Supported formats: MP4, MOV, AVI, and MKV. "
            "Actual decoding support depends on the installed "
            "OpenCV video backend."
        )
# =========================================================
# ANIME PORTRAIT LAB
# =========================================================

elif page == "Anime Portrait Lab":

    st.markdown("## 🎨 Anime Portrait Lab")

    st.write(
        "Upload a portrait, apply a cartoon-style filter, "
        "compare the output with your original, and download it."
    )

    st.caption(
        "This first version uses OpenCV image processing. "
        "Generative AI anime transformation is a future enhancement."
    )

    uploaded_file = st.file_uploader(
        "Upload your portrait",
        type=["jpg", "jpeg", "png"],
        key="portrait_upload",
        help="Choose a JPG or PNG image. Maximum size: 10 MB.",
    )

    if uploaded_file is not None:

        # Avoid processing unexpectedly large files.
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error(
                "This image is larger than 10 MB. "
                "Please upload a smaller image."
            )

        else:
            try:
                uploaded_file.seek(0)

                # Apply image orientation from EXIF metadata.
                original = ImageOps.exif_transpose(
                    Image.open(uploaded_file)
                ).convert("RGB")

                if original.width < 2 or original.height < 2:
                    raise ValueError(
                        "The uploaded image dimensions are invalid."
                    )

                # Keep the processing workload manageable.
                max_dimension = 1200

                if max(original.size) > max_dimension:
                    original.thumbnail(
                        (max_dimension, max_dimension),
                        Image.Resampling.LANCZOS,
                    )

                st.success(
                    f"Image ready: {original.width} × {original.height} pixels"
                )

                original_array = np.array(original)

                # Pillow uses RGB; OpenCV expects BGR.
                bgr_image = cv2.cvtColor(
                    original_array,
                    cv2.COLOR_RGB2BGR,
                )

                # Generate a stable key for the uploaded source.
                source_key = (
                    uploaded_file.name,
                    uploaded_file.size,
                )

                # Clear stale results when the source changes.
                if st.session_state["cartoon_source"] != source_key:
                    st.session_state["cartoon_source"] = source_key
                    st.session_state["cartoon_result"] = None

                st.markdown("### Transformation")

                style = st.selectbox(
                    "Choose a style",
                    [
                        "Classic Cartoon",
                    ],
                    key="cartoon_style",
                )

                st.caption(
                    "More artistic styles and AI-based transformations "
                    "can be added later."
                )

                if st.button(
                    "✨ Generate Cartoon",
                    type="primary",
                    use_container_width=True,
                ):
                    with st.spinner("Processing your portrait..."):
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
                        st.image(
                            original,
                            caption="Original Portrait",
                            use_container_width=True,
                        )

                    with after_col:
                        st.image(
                            result,
                            caption=style,
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

            except (UnidentifiedImageError, OSError, ValueError) as exc:
                st.error(
                    "The uploaded file could not be opened as a valid image. "
                    "Please try another JPG or PNG."
                )
                st.caption(f"Details: {exc}")

            except Exception as exc:
                st.error(
                    "Something went wrong while preparing the image."
                )
                st.caption(f"Details: {exc}")

    else:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🖼️</div>
                <h3>Your portrait starts here</h3>
                <p>
                    Upload a JPG or PNG image to create your
                    first cartoon-style portrait.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption(
        "EMOTUNE · Your face. Your character. Your vibe."
    )