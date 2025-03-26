# YouTube Downloader & Cutter

This project provides a command-line tool to download and cut YouTube videos. It uses **yt-dlp** to download videos (or extract audio) and **FFmpeg** to cut the media file. The tool supports specifying start and end times (or clip length) for cutting the downloaded media. This repository also includes a starter batch file to create a Python virtual environment and install required dependencies.

---

## Files Overview

- **ytDL.py**  
  The main Python script that:
  - Downloads YouTube videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp).
  - Supports three download modes:
    - **Audio only:** Extracts and saves the audio as an MP3 file.
    - **Video only:** Downloads video without audio.
    - **Video + Audio:** Downloads and merges the best video and audio streams into an MP4.
  - Cuts a segment of the downloaded file based on specified start (`-s`), end (`-e`), or length (`-l`) arguments.
  - Uses **FFmpeg** (via subprocess calls) for precise media cutting.

- **starter.bat**  
  A Windows batch script that:
  - Checks for an existing Python virtual environment (`venv`) and creates it if missing.
  - Activates the virtual environment.
  - Upgrades pip and installs all required dependencies from `requirements.txt`.
  - Keeps the command prompt open with the virtual environment active.

- **requirements.txt**  
  Contains the Python package dependencies:
yt-dlp moviepy

yaml
Copy
Edit
These packages are used by `ytDL.py` for downloading videos and processing media files.

---

## Prerequisites

- **Python 3.6+** (recommended Python 3.8+)
- **FFmpeg** installed and added to your system's PATH  
Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/) if it is not already installed.

---

## Setup & Installation

1. **Clone the Repository:**

 ```bash
 git clone https://github.com/yourusername/your-repository.git
 cd your-repository
Run the Starter Batch File (Windows):

Double-click starter.bat or run it from a command prompt to:

Create and activate a Python virtual environment.

Upgrade pip.

Install required Python packages from requirements.txt.

Alternatively, you can manually create the virtual environment and install dependencies:

bat
Copy
Edit
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
Usage
With the virtual environment activated, you can run the script using Python.

Command-Line Options
bash
Copy
Edit
python ytDL.py <YouTube URL> [options]
Positional Argument:

<YouTube URL>: URL of the YouTube video.

Optional Flags:

-a: Download audio only (extracts audio as MP3).

-v: Download video only (no audio).

-s mm.ss: Set the start time for cutting (in mm.ss format, e.g., 01.30 for 1 minute 30 seconds).

-e mm.ss: Set the end time for cutting.

-l mm.ss: Set the length of the clip; must be used with either -s or -e (cannot be used when both are provided).

-n output_filename: Specify the output file name (default is out.mp4).

Note: You cannot use both -a (audio only) and -v (video only) simultaneously.

Examples
Audio Only Clip (from 1:00 to 2:00):

bash
Copy
Edit
python ytDL.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a -s 01.00 -e 02.00 -n audio_clip.mp4
Video + Audio Clip (from 1:00 to 2:00):

bash
Copy
Edit
python ytDL.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -s 01.00 -e 02.00 -n video_clip.mp4
Additional Notes
FFmpeg Requirement:
This script uses FFmpeg for cutting the downloaded media. Ensure that FFmpeg is installed and accessible via your system's PATH.

Virtual Environment:
The provided starter.bat simplifies setting up the virtual environment on Windows. For other platforms, follow your platform’s standard procedures for creating and activating Python virtual environments.

Error Handling:
The script provides error messages for issues such as download failures, invalid time parameters, or file processing errors. Please review the console output for troubleshooting.

Updating Dependencies:
To update dependencies, activate your virtual environment and run:

bash
Copy
Edit
pip install --upgrade yt-dlp moviepy
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or suggestions, please open an issue in the repository or contact your.email@example.com.

Happy Downloading & Editing!

Copy
Edit
