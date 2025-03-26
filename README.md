# YouTube Downloader & Cutter

This project provides a command-line tool to download and cut YouTube videos using **yt-dlp** and **FFmpeg**. It allows you to specify start and end times (or clip length) to extract specific segments from the downloaded media.

---

## Quick Usage

Run the tool with:

```bash
python ytDL.py "<YouTube URL>" [options]
```

**Examples:**

- **Download audio only (from 1:00 to 2:00):**
  ```bash
  python ytDL.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a -s 01.00 -e 02.00 -n audio_clip.mp3
  ```
- **Download video + audio (from 1:00 to 2:00):**
  ```bash
  python ytDL.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -s 01.00 -e 02.00 -n video_clip.mp4
  ```

---

## Files Overview

- **ytDL.py**  
  The main script that:
  - Downloads YouTube videos via [yt-dlp](https://github.com/yt-dlp/yt-dlp).
  - Supports three download modes:
    - **Audio only:** Extracts and saves audio as an MP3 file.
    - **Video only:** Downloads video without audio.
    - **Video + Audio:** Downloads and merges the best video and audio streams into an MP4.
  - Cuts the media file using **FFmpeg** based on start (`-s`), end (`-e`), or clip length (`-l`) parameters.

- **starter.bat**  
  A Windows batch script that:
  - Checks for and creates a Python virtual environment (`venv`) if it doesn’t exist.
  - Activates the virtual environment.
  - Upgrades pip and installs dependencies from `requirements.txt`.

- **requirements.txt**  
  Contains the necessary Python package dependencies:
  ```plaintext
  yt-dlp
  moviepy
  ```

---

## Prerequisites

- **Python 3.6+** (Python 3.8+ recommended)
- **FFmpeg** installed and added to your system's PATH  
  Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/) if needed.

---

## Setup & Installation

### Clone the Repository

```bash
git clone https://github.com/DejviUka/TubeSlice.git
cd TubeSlice
```

### Using the Starter Batch File (Windows)

Double-click `starter.bat` or run it from the command prompt:

```bat
call starter.bat
```

This will:
- Create and activate a Python virtual environment.
- Upgrade pip.
- Install required dependencies.

### Manual Setup (Alternative)

```bash
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Command-Line Options

```bash
python ytDL.py <YouTube URL> [options]
```

### Positional Argument
- `<YouTube URL>`: The URL of the YouTube video.

### Optional Flags
- `-a`: Download audio only (extract audio as MP3).
- `-v`: Download video only (no audio).
- `-s mm.ss`: Set the start time for cutting (e.g., `01.30` for 1 minute 30 seconds).
- `-e mm.ss`: Set the end time for cutting.
- `-l mm.ss`: Set the length of the clip (must be used with `-s` or `-e`).
- `-n output_filename`: Specify the output file name (default is `out.mp4`).

**Note:** Do not use `-a` and `-v` simultaneously.

---

## Additional Notes

### FFmpeg Requirement
This script uses **FFmpeg** to cut the media file. Ensure FFmpeg is installed and available in your system's PATH.

### Virtual Environment
The `starter.bat` script simplifies setting up a virtual environment on Windows. For other platforms, use your standard method for creating and activating a Python virtual environment.

### Error Handling
The script provides error messages for issues such as download failures, invalid time parameters, or file processing errors. Check the console output for troubleshooting.

### Updating Dependencies
To update dependencies, activate your virtual environment and run:

```bash
pip install --upgrade yt-dlp moviepy
```

---

## License

This project is licensed under the APACHE2 License. See the `LICENSE` file for details.

---

## Contact

For questions or suggestions, please open an issue in the repository or contact `dejvendetta@hotmail.com`.

**Happy Downloading & Editing!**
