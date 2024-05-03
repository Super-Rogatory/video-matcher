import json
import cv2
import numpy as np

# Function to get frame hash
 

def get_frame_hash(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (8, 8))

    diff = resized_frame > np.mean(resized_frame)
    frame_hash = "".join(["1" if val else "0" for val in diff.flatten()])
    return frame_hash

# Extract frame hashes from a video
def extract_frame_hashes(video_path, step=30):
    frame_hashes = []
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if frame_count % step == 0:
            frame_hash = get_frame_hash(frame)
            frame_hashes.append(frame_hash)

        frame_count += 1

    video.release()
    return frame_hashes

# Find the most similar video
def find_similar_video(query_video_path, json_path):
    # Load the preprocessed frame hashes
    with open(json_path, 'r') as json_file:
        video_hashes = json.load(json_file)

    query_frame_hashes = extract_frame_hashes(query_video_path)
    similarities = {}

    # Calculate similarities
    for video_name, frame_hashes in video_hashes.items():
        frame_similarities = [
            max(sum(c1 == c2 for c1, c2 in zip(query_hash, video_hash)) / 64
                for video_hash in frame_hashes)
            for query_hash in query_frame_hashes
        ]
        similarities[video_name] = np.mean(frame_similarities)

    # Return the most similar video
    return sorted(similarities.items(), key=lambda x: -x[1])[0][0]

# Example usage
# query_video_path = './Queries/video10_1_modified.mp4'  # Path to the query video
# json_path = "./preprocessing.json"  # Preprocessing JSON file path

# Find the most similar video
# most_similar_video = find_similar_video(query_video_path, json_path)
# print("The most similar video is:", most_similar_video)