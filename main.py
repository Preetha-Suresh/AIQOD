import re
import whisper
from transformers import pipeline
import subprocess

# Initialize Whisper model for transcription
model = whisper.load_model("base")

# Transcribe the audio file
def transcribe_audio(audio_file):
    print(f"Transcribing {audio_file}...")
    result = model.transcribe(audio_file)
    return result["text"]

# Summarize the transcript
# Summarize the transcript in chunks
def summarize_transcript(transcript, chunk_size=1000):
    summarizer = pipeline("summarization")
    print("Summarizing transcript...")

    # Split the transcript into chunks
    chunks = [transcript[i:i+chunk_size] for i in range(0, len(transcript), chunk_size)]
    summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine all chunk summaries into one
    full_summary = " ".join(summaries)
    return full_summary


# Extract tasks from the summary
def extract_tasks(transcript):
    task_patterns = [
        re.compile(r'(\w+) will (\w+ .*?)\.', re.IGNORECASE),
        re.compile(r'(\w+) is responsible for (.*?)(?:\.|$)', re.IGNORECASE),
        re.compile(r'let\'s have (\w+) (\w+ .*?)\.', re.IGNORECASE)
    ]

    tasks = []
    for pattern in task_patterns:
        tasks.extend(pattern.findall(transcript))

    return tasks

# Main function to run the full pipeline
def main(video_file):
    audio_file = "audio.wav"
    
    # Extract audio using ffmpeg
    command = ["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", audio_file, "-y"]
    subprocess.run(command, check=True)
    
    # Transcribe and summarize
    transcript = transcribe_audio(audio_file)
    print("\nMeeting Transcript:")
    print(transcript)
    
    summary = summarize_transcript(transcript)
    print("\nMeeting Summary:")
    print(summary)
    
    # Extract tasks
    task_list = extract_tasks(summary)

    print("\nTask Assignments:")
    if task_list:
        for name, task in task_list:
            print(f"- {name}: {task}")
    else:
        print("No tasks assigned.")

# Example video file
video_file = r"C:\\Users\Sahi\Downloads\Annual General Meeting FY 2019-20.mp4"
main(video_file)

