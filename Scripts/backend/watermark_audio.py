import numpy as np
import soundfile
import torch
import wavmark
import os
import io
file_path = r"C:\Users\Ahzam\Downloads\example.wav"


def watermark_audio(model, audio_clips, payload=None ):
    """Embeds a watermark in an audioclip. The watermark itself is a 16 bit payload"""
    if payload == None:
        payload = np.array([1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1], int)

    watermarked_audio = []

    for audio_clip in audio_clips:
        processed_clip, _ = wavmark.encode_watermark(model, audio_clip, payload, show_progress=True)
        watermarked_audio.append(processed_clip)

    return watermarked_audio

def decode_watermark(model, audio_clips):
    """decodes the watermarks from a watermarked audio clip"""
    decoded_payloads = []

    for audio_clip in audio_clips:
        processed_clip, _ = wavmark.decode_watermark(model, audio_clip, show_progress=True)
        decoded_payloads.append(processed_clip)

    return decoded_payloads

def calculate_error(decoded_payloads, payload):
    """calculates the error between the decoded payload and the actual payload"""
    BER_list = []
    for decoded_payload in decoded_payloads:
        BER = (payload != decoded_payload).mean() * 100
        BER_list.append(BER)

    return BER

def read_uploaded_audio(uploaded_file):
    """converts streamlits bvtes based upload into an audiofile that is compatible with the watermarking model"""
    audio_bytes = uploaded_file.read()
    audio_buffer = io.BytesIO(audio_bytes)
    signal, sample_rate = soundfile.read(audio_buffer)
    return signal, sample_rate



