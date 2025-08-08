import streamlit as st
from Scripts.backend.watermark_audio import *
import torch
import wavmark

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = wavmark.load_model().to(device)

st.set_page_config(page_title="Echotrace", layout="centered")
st.title("Echotrace audio watermarking tool")

mode = st.sidebar.radio("Select page", ["Watermark audio", "Check audio for watermarks"])

if mode == "Watermark audio":
    st.header("Upload .wav files to watermark")
    uploaded_files = st.file_uploader("Choose a WAV file", type=["wav"], key="watermark", accept_multiple_files=True)

    if uploaded_files is not None:
        for file in uploaded_files:
            st.audio(file, format='audio/wav')
        if st.button("Apply Watermark"):
            for file in uploaded_files:
                watermarked_audio_clips = watermark_audio(model, uploaded_files)


            st.success("Watermark applied successfully!")
            st.download_button("Download Watermarked Audio", data=b"", file_name="watermarked.wav", mime="audio/wav")

elif mode == "Check audio for watermarks":
    st.header("🕵️‍♂️ Upload Watermarked File to Check")
    uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"], key="check")

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        if st.button("Check Watermark"):
            # Placeholder for backend logic
            st.success("Decoded Payload: [1, 0, 1, 0, ...]")
            st.info("Bit Error Rate (BER): 0.0%")