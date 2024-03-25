from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image

def generate_thumbnail(video_path, thumbnail_path, time_point=2):
    try:
        clip = VideoFileClip(video_path)
        thumbnail = clip.get_frame(time_point)
        Image.fromarray(thumbnail).save(thumbnail_path)
        
    except Exception as e:
        print(f"Error generating thumbnail: {str(e)}")
