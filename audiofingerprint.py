import subprocess
import librosa
import numpy as np
from scipy import signal
import os
import find_similar_video

def remove_temporary_files(original_audio,query_audio ):
    if os.path.exists(original_audio):
        os.remove(original_audio)
    if os.path.exists(query_audio):
        os.remove(query_audio)


def extract_audio(video_path, output_audio_path):
    # Convert to absolute path to avoid any relative path issues
    absolute_video_path = os.path.abspath(video_path)
    
    # Check if the video file exists
    if not os.path.exists(absolute_video_path):
        print(f"Error: Video file not found at {absolute_video_path}")
        return
    
    command = [
        'ffmpeg', '-i', absolute_video_path,  # Use the absolute path
        '-vn',  # No video output
        '-acodec', 'pcm_s16le',  # Convert audio to PCM s16le (linear16)
        '-ar', '44100',  # Set audio sample rate to 44100 Hz
        '-ac', '2',  # Set number of audio channels to 2
        output_audio_path  # Output audio file
    ]
    try:
        subprocess.run(command, check=True)
        print("Audio extracted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract audio: {e}")
        
def find_offset(within_file, find_file, window):
    y_within, sr_within = librosa.load(within_file, sr=None)
    y_find, _ = librosa.load(find_file, sr=sr_within)

    # Truncate the find_file audio if necessary
    y_find = y_find[:sr_within * window] if len(y_find) > sr_within * window else y_find

    c = signal.correlate(y_within, y_find, mode='valid', method='fft')
    peak = np.argmax(c)
    offset = round(peak / sr_within, 2)

    return offset

def convert_seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = round(seconds % 60)
    if remaining_seconds == 60:
        minutes += 1
        remaining_seconds = 0

    return minutes, remaining_seconds

# def process_audio_analysis():
#     """
#     Process audio analysis to find the offset of the query audio within the original video's audio.
#     """
#     original_video_name = find_similar_video.most_similar_video
#     original_video_path = './video/' + original_video_name
#     query_video_path = find_similar_video.query_video_path

#     original_audio = 'original_audio.wav'
#     query_audio = 'query_audio.wav'

#     remove_temporary_files(original_audio, query_audio)

#     extract_audio(original_video_path, original_audio)
#     extract_audio(query_video_path, query_audio)

#     offset = find_offset(original_audio, query_audio, 10)  # Analyze first 10 seconds of the audio
#     total_seconds = offset
#     minutes, seconds = convert_seconds_to_min_sec(total_seconds)

#     print(f"The query audio is found at {minutes} minutes and {seconds} seconds in the {original_video_name}.")

#     remove_temporary_files(original_audio, query_audio)

# # Paths to the video files
# original_video_name = find_similar_video.most_similar_video

# original_video_path = './video/' + original_video_name
# query_video_path = find_similar_video.query_video_path


# # Paths for the extracted audio files
# original_audio = 'original_audio.wav'
# query_audio = 'query_audio.wav'

# remove_temporary_files(original_audio,query_audio )

# # Extract audio from videos
# extract_audio(original_video_path, original_audio)
# extract_audio(query_video_path, query_audio)

# # Analyze audio to find the offset
# offset = find_offset(original_audio, query_audio, 10)  # Using the first 10 seconds of the query audio
# total_seconds = offset
# minutes, seconds = convert_seconds_to_min_sec(total_seconds)

# print(f"The query audio is found at {minutes} minutes and {seconds} seconds in the {original_video_name}.")

# remove_temporary_files(original_audio,query_audio )
