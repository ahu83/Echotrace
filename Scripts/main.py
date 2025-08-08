import streamlit as st
from backend.watermark_audio import *
import torch
import wavmark
import soundfile
import io

def read_uploaded_audio(uploaded_file):
    audio_bytes = uploaded_file.read()
    audio_buffer = io.BytesIO(audio_bytes)
    signal, sample_rate = soundfile.read(audio_buffer)
    return signal, sample_rate

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
            read_files = []
            for file in uploaded_files:
                read_file, _ = read_uploaded_audio(file)
                read_files.append(read_file)

            watermarked_audio_clips = watermark_audio(model, read_files)

            i = 1
            st.success("Watermark applied successfully!")

            for idx, clip in enumerate(watermarked_audio_clips):
                buffer = io.BytesIO()
                soundfile.write(buffer, clip, samplerate=16000, format='WAV')
                buffer.seek(0)
                st.download_button(
                    label=f"Download Clip {idx + 1}",
                    data=buffer,
                    file_name=f"watermarked_{idx + 1}.wav",
                    mime="audio/wav"
                )



elif mode == "Check audio for watermarks":
    st.header("Upload .wav files to check")
    uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"], key="check")

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        if st.button("Check Watermark"):
            read_file, _ = read_uploaded_audio(uploaded_file)
            decoded_file = decode_watermark(model, [read_file])
            BER = calculate_error(decoded_file, np.array([1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1], int))
            st.success(f"Decoded Payload {decoded_file}")
            st.info(f"Bit Error Rate (BER): {BER}")
            if BER == 0:
                st.info(f"The audio contains a watermark")
            elif BER > 1:
                st.info(f"The audio does not contain a watermark")