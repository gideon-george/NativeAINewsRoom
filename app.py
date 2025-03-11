import streamlit as st
import tempfile
from transformers import pipeline

# Title & Description
st.write("""**ICIR Native AI Demo – Phase 2**

Experience the next stage of AI-driven media technology, tailored for Nigerian newsrooms. We’ve successfully completed Phase 2. Now, we’re moving into Phase 3, which will bring accent-specific training and fine-tuning using larger Hausa, Yoruba, and Igbo datasets for even higher accuracy with local accents.

**How It Works**  
Upload your audio (WAV, MP3, M4A) to see real-time English transcriptions and instant translations into Hausa, Igbo, and Yoruba—all powered by AI built for Nigerian media professionals.

**Key Features**  
- **Phase 2 Completed:** AI Model Foundations (ASR & MT)  
- **Phase 3 (Upcoming):**  
  - Accent-Specific Training & Fine-Tuning (Hausa, Yoruba, Igbo)  
  - Improved accuracy for local accents  
- **Optimized for Nigerian Accents** (Coming Soon)  
- **Tailored for Newsroom Workflows** (Coming Soon)  
- **Breaking Language Barriers with AI**  

Empowering journalists and media professionals with robust AI tools for a more connected, informed audience.
""")


# Cache the ASR pipeline so it doesn't reload each time
@st.cache_resource
def load_asr_pipeline():
    st.write("Loading ASR model...")
    return pipeline("automatic-speech-recognition", 
                    model="mosesdaudu/afrolinguahub_accented_english_ASR")

# Cache the translation pipeline
@st.cache_resource
def load_translation_pipeline():
    st.write("Loading Translation model...")
    return pipeline("translation", 
                    model="HelpMumHQ/AI-translator-eng-to-9ja")

def perform_asr(audio_file_path: str) -> str:
    asr_pipeline = load_asr_pipeline()
    st.write(f"Transcribing: {audio_file_path}")
    asr_result = asr_pipeline(audio_file_path)
    transcript = asr_result.get("text", "")
    st.subheader("Transcript")
    st.write(transcript)
    return transcript

def translate_text(text: str) -> str:
    translation_pipeline = load_translation_pipeline()
    translation_result = translation_pipeline(text, max_length=512)
    translation = translation_result[0]['translation_text']
    st.subheader("Translated Text")
    st.write(translation)
    return translation

# File Uploader for audio
uploaded_file = st.file_uploader("Upload an audio file (wav, mp3, m4a)", type=["wav","mp3","m4a"])
if uploaded_file is not None:
    # Write the uploaded file to a temp file so we can pass it to the model
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # Display audio player
    st.audio(tmp_file_path, format='audio/wav')

    # Button to process the audio
    if st.button("Process Audio"):
        transcript = perform_asr(tmp_file_path)
        if transcript:
            translate_text(transcript)
