from pydub import AudioSegment
import speech_recognition as sr
import os
from langdetect import detect
from googletrans import Translator
from transformers import pipeline


# Set the path to ffmpeg if it's not in PATH
os.environ["FFMPEG_BINARY"] = r"C:\Users\sreel\OneDrive\Documents\AIQOD\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"  # Correct this path if needed
os.environ["FFPROBE_BINARY"] = r"C:\Users\sreel\OneDrive\Documents\AIQOD\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"  # Optional, in case ffprobe is missing

# Specify the path to your video file
video_file = r"C:\Users\sreel\OneDrive\Documents\AIQOD\meeting_video.mp4"  # Replace with your video file path

# Step 1: Extract audio from the video file using pydub
audio = AudioSegment.from_file(video_file, format="mp4")  # Extract audio from the video file
audio.export("meeting_audio.wav", format="wav")  # Save audio as a .wav file
print("Audio extraction complete!")

# Step 2: Load the audio file (ensure it's in the same folder as the code or specify the path)
n_audio = AudioSegment.from_wav("meeting_audio.wav")
audio = n_audio.normalize()  # Normalize the audio

# Step 3: Split the audio into smaller chunks (1 minute = 60000 milliseconds)
chunk_length_ms = 60000  # 1 minute
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# Step 4: Initialize the recognizer
recognizer = sr.Recognizer()

full_transcript = ""

# Process each chunk of audio
for idx, chunk in enumerate(chunks):
    chunk_filename = f"chunk_{idx}.wav"
    chunk.export(chunk_filename, format="wav")  # Save each chunk as a separate WAV file
    
    with sr.AudioFile(chunk_filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        # Transcribe each chunk using Google Speech Recognition API
        text = recognizer.recognize_google(audio_data)
        full_transcript += text + "\n"  # Add the transcription of this chunk to the full transcript
    except sr.UnknownValueError:
        print(f"Couldn't understand the audio in chunk {idx}.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# After all chunks are transcribed, print the full transcript
print("\nFull Transcript of the Meeting:")
print(full_transcript)
