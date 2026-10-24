# EMOTUNE — Expressions in Motion

**EMOTUNE** is an anime-inspired avatar and cartoon portrait application built with Python and Streamlit. It brings expressions to life through a webcam-based avatar experience and provides tools for creating cartoon-style portraits from uploaded images.

## Features

- **Live Avatar Studio:** Use webcam-based facial landmark detection to analyze expressions and display a corresponding anime avatar.
- **Anime Girl & Anime Boy:** Choose your preferred avatar style.
- **Expression Detection:** Recognize expressions such as happy, surprised, blinking, and neutral using facial blendshapes.
- **Avatar Actions:** Select actions and poses such as idle, wave, dance, cry, and talk.
- **Video Avatar Studio:** Upload a video for processing through the video studio.
- **Anime Portrait Lab:** Transform an uploaded photograph into a cartoon-style portrait.
- **Download Results:** Save generated portrait images and processed video outputs where supported.

## Tech Stack

- Python
- Streamlit
- OpenCV
- MediaPipe Tasks
- Pillow (PIL)
- NumPy
- streamlit-webrtc
- PyAV

## Project Structure

```text
EMOTUNE/
├── app.py
├── models/
│   └── face_landmarker.task
├── src/
│   ├── vision/
│   │   ├── face_landmarks.py
│   │   └── expression_analyzer.py
│   ├── avatar/
│   │   ├── avatar_renderer.py
│   │   └── live_avatar_processor.py
│   └── portrait/
│       ├── cartoon_filters.py
│       └── video_processor.py
├── tests/
├── .gitignore
└── README.md
```

*Note: The structure above describes the main project components; the exact files may vary as development continues.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/EMOTUNE.git
cd EMOTUNE
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install streamlit opencv-python mediapipe pillow numpy streamlit-webrtc av
```

### 4. Configure the face landmark model

The live facial tracking feature requires the MediaPipe Face Landmarker model at:

```text
models/face_landmarker.task
```

Ensure the model file is available at this location before using the live avatar feature.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal. Allow camera access when prompted to use the Live Avatar Studio.

## Application Modules

| Module | Purpose |
|---|---|
| Live Avatar Studio | Webcam-based facial expression analysis and avatar rendering |
| Video Avatar Studio | Video upload and processing |
| Anime Portrait Lab | Cartoon-style portrait generation |

## Future Enhancements

- Smoother real-time avatar animation
- More interactive facial expressions and character actions
- Improved video-based face tracking and avatar integration
- Additional portrait styles and customization options
- Improved performance and deployment support

## Development

EMOTUNE is an ongoing project developed using Python-based computer vision and interactive web application technologies.

**Tagline:** *Expressions in Motion*
