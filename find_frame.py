import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import audiofingerprint # audio fingerprint gets - hit first
import find_similar_video
from moviepy.editor import VideoFileClip
import subprocess
import json

def get_video_frames(video_path):
    """
    Load frames from a given video file.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames

def resize_frame(frame, target_width, target_height):
    """
    Resize a frame to specified dimensions.
    """
    return cv2.resize(frame, (target_width, target_height))

def compare_frames(frame1, frame2):
    """
    Compare two frames using SSIM.
    """
    # Ensure frames have the same size
    if frame1.shape != frame2.shape:
        frame1 = resize_frame(frame1, frame2.shape[1], frame2.shape[0])
    
    # Convert frames to grayscale
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM between the grayscale frames
    ssim_value, _ = ssim(frame1_gray, frame2_gray, full=True)
    
    return ssim_value

def find_best_match(original_video_path, query_video_path):
    """
    Find the most likely frame where the query video starts in the original video.
    """
    original_frames = get_video_frames(original_video_path)
    query_frames = get_video_frames(query_video_path)

    best_match_index = -1
    best_match_score = float('-inf')

    # Loop over the original video frames and compare them with the query video frames
    for i in range(len(original_frames) - len(query_frames) + 1):
        match_score = 0
        
        # Compare each frame pair-wise and accumulate the SSIM score
        for j in range(len(query_frames)):
            score = compare_frames(original_frames[i + j], query_frames[j])
            match_score += score
        
        # Normalize match score by the number of frames in the query video
        match_score /= len(query_frames)
        
        # Update the best match
        if match_score > best_match_score:
            best_match_score = match_score
            best_match_index = i

    print(f"The most likely frame where the query video starts is frame {best_match_index} with an average similarity score of {best_match_score}.")
    return best_match_index

def get_video_duration(file_path):
    # Run the `ffprobe` command to get metadata in JSON format
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-of", "json", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Parse the output to JSON
    metadata = json.loads(result.stdout)
    duration = float(metadata["format"]["duration"])
    return duration

def process_videos(input_video_path, query_video_path, total_seconds):
    """
    Process videos to find the best match frame.
    """
    # video_path = "./video/"
    # origin_video = find_similar_video.most_similar_video
    # input_video_path = video_path + origin_video
    # query_video_path = find_similar_video.query_video_path
    # query_video_duration = get_video_duration(query_video_path)
    video_cut_duration = 10

    start_time = int(total_seconds) - 2
    start_time = max(start_time, 0)
    end_time = start_time + video_cut_duration + 4

    output_video_path = "output_video.mp4"
    video = VideoFileClip(input_video_path)
    video_cut = video.subclip(start_time, end_time)
    video_cut.write_videofile(output_video_path, codec="libx264")

    output_query_video_path = "output_query_video.mp4"
    video = VideoFileClip(query_video_path)
    video_cut = video.subclip(0, video_cut_duration)
    video_cut.write_videofile(output_query_video_path, codec="libx264")

    frame = find_best_match(output_video_path, output_query_video_path)
    frame_num = int(start_time * 30 + frame) - 1
    return frame_num

# # Specify the input video file path
# video_path = "./video/"

# origin_video = find_similar_video.most_similar_video
# input_video_path = video_path + origin_video
# query_video_path = find_similar_video.query_video_path
# query_video_duration = get_video_duration(query_video_path)
# video_cut_duration = 10

# # Specify the start and end times in seconds
# start_time = int(audiofingerprint.total_seconds) - 2
# if start_time < 2:
#     start_time = 0
# end_time = start_time + video_cut_duration + 4 

# # Specify the output video file path
# output_video_path = "output_video.mp4"

# # Load the video clip
# video = VideoFileClip(input_video_path)

# # Cut the video clip from start_time to end_time
# video_cut = video.subclip(start_time, end_time)

# # Save the cut video to the specified path
# video_cut.write_videofile(output_video_path, codec="libx264")

# # Specify the output video file path
# output_query_video_path = "output_query_video.mp4"

# # Load the video clip
# video = VideoFileClip(query_video_path)

# # Cut the video clip from start_time to end_time
# video_cut = video.subclip(0, video_cut_duration)

# # Save the cut video to the specified path
# video_cut.write_videofile(output_query_video_path, codec="libx264")


# # Usage:
# frame = find_best_match('output_video.mp4', "output_query_video.mp4")
# # print(frame_num)
# # print(audiofingerprint.total_seconds)
# # print(start_time * 30)
# frame_num = int(start_time * 30 + frame)-1
# print(frame_num)
