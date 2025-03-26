#!/usr/bin/env python3
import argparse
import os
import sys
import re
import subprocess
import yt_dlp

# Import moviepy modules with fallback in case moviepy.editor is missing.
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
except ModuleNotFoundError:
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        from moviepy.audio.io.AudioFileClip import AudioFileClip
    except ModuleNotFoundError:
        print("Error: The 'moviepy' module is not installed or not found. Please run: pip install moviepy")
        sys.exit(1)

def parse_time(time_str):
    """
    Parse a time string in mm.ss format to seconds.
    Example: "01.30" -> 90 seconds.
    """
    if not re.match(r'^\d{1,2}\.\d{2}$', time_str):
        raise ValueError("Time format must be mm.ss (e.g. 01.30 for 1 minute 30 seconds)")
    minutes, seconds = time_str.split('.')
    return int(minutes) * 60 + int(seconds)

def download_video(url, audio_only=False, video_only=False):
    temp_output = "temp_download"
    ydl_opts = {}
    
    if audio_only:
        # Download best audio and extract it as mp3.
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        expected_ext = "mp3"
    elif video_only:
        # Download best video-only stream (mp4 format) with no audio.
        ydl_opts['format'] = 'bestvideo[ext=mp4]'
        expected_ext = "mp4"
    else:
        # Download best video+audio and merge into mp4.
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'
        expected_ext = "mp4"

    ydl_opts['outtmpl'] = temp_output + ".%(ext)s"

    print("Downloading from YouTube...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)
    
    temp_filename = f"{temp_output}.{expected_ext}"
    if not os.path.exists(temp_filename):
        print(f"Error: Expected downloaded file {temp_filename} not found.")
        sys.exit(1)
    return temp_filename

def ffmpeg_cut(input_file, output_file, start, end, audio_only):
    duration = end - start
    if audio_only:
        # For audio-only, use stream copy
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", input_file,
            "-t", str(duration),
            "-c", "copy",
            output_file
        ]
    else:
        # For video+audio, re-encode using libx264 and aac.
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-i", input_file,
            "-t", str(duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            output_file
        ]
    print("Running ffmpeg command:")
    print(" ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr.decode())
        sys.exit(1)

def cut_clip(input_file, output_file, start, end, audio_only=False):
    print(f"Processing clip from {input_file} ...")
    # Use MoviePy to get duration of the file.
    try:
        if audio_only:
            clip = AudioFileClip(input_file)
        else:
            clip = VideoFileClip(input_file)
        clip_duration = clip.duration
        clip.close()
    except Exception as e:
        print(f"Error getting file duration: {e}")
        sys.exit(1)

    s = start if start is not None else 0
    e = end if end is not None else clip_duration

    if s < 0 or e > clip_duration or s >= e:
        print("Invalid cut times provided.")
        sys.exit(1)

    ffmpeg_cut(input_file, output_file, s, e, audio_only)

def main():
    parser = argparse.ArgumentParser(
        description="Download and optionally cut a YouTube video using yt-dlp and ffmpeg.",
        add_help=False
    )
    parser.add_argument("-h", "-help", "-?", "--help", action="help", default=argparse.SUPPRESS,
                        help="Show this help message and exit")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-a", action="store_true", help="Download audio only")
    parser.add_argument("-v", action="store_true", help="Download video only (no audio)")
    parser.add_argument("-s", help="Start time in mm.ss")
    parser.add_argument("-e", help="End time in mm.ss")
    parser.add_argument("-l", help="Length of the clip in mm.ss (use with -s or -e; cannot be used with both -s and -e simultaneously)")
    parser.add_argument("-n", default="out.mp4", help="Output file name (default: out.mp4)")
    args = parser.parse_args()

    if args.a and args.v:
        print("Error: -a (audio only) and -v (video only) cannot be used together.")
        sys.exit(1)

    start = None
    end = None
    length = None

    try:
        if args.s:
            start = parse_time(args.s)
        if args.e:
            end = parse_time(args.e)
        if args.l:
            length = parse_time(args.l)
    except ValueError as ve:
        print(f"Time parsing error: {ve}")
        sys.exit(1)

    if length is not None and (args.s and args.e):
        print("Error: -l cannot be used when both -s and -e are provided. Use either start+length or end-length.")
        sys.exit(1)

    if length is not None:
        if start is not None and end is None:
            end = start + length
        elif end is not None and start is None:
            start = end - length
        elif start is None and end is None:
            print("Error: When using -l, you must also provide either -s or -e.")
            sys.exit(1)

    temp_file = download_video(args.url, audio_only=args.a, video_only=args.v)

    if start is None and end is None:
        print(f"No cutting parameters provided. Renaming downloaded file to {args.n}")
        try:
            os.rename(temp_file, args.n)
        except Exception as e:
            print(f"Error renaming file: {e}")
            sys.exit(1)
    else:
        cut_clip(temp_file, args.n, start, end, audio_only=args.a)
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Warning: could not remove temporary file: {e}")

if __name__ == "__main__":
    main()
