# massencode

This script allows for the compression of video files using both GPU acceleration (currently only via AMD VAAPI) and CPU encoding **concurrently**. It maintains the original directory structure and filenames in the output directory.

## Features

- Compress videos in various formats: MP4, MOV, AVI, MKV.
- Utilize CPU and GPU for hardware-accelerated compression.
- Maintain original directory structure and names in the output directory.
- Multi-threaded to compress videos efficiently, processing one video using GPU and one using CPU at the same time.

## Requirements

- Python 3.x
- ffmpeg-python
- FFmpeg with support for VAAPI (GPU acceleration)

## Installation

1. **Install Python and FFmpeg**: Ensure you have Python 3 and ffmpeg-python installed on your system.
With pip:
`pip install ffmpeg-python`

2. **Clone the repository** or just create a new Python file with the script code provided.

For VAAPI installation and configuration, consult your distribution's wiki.

## Usage

You can run the script from the command line as follows:

`python script_name.py /path/to/input/folder /path/to/output/folder --bitrate <bitrate>`

### Parameters

- `input_folder`: Path to the input directory containing the video files to compress.
- `output_folder`: Path to the directory where the compressed videos will be saved.
- `--bitrate`: Optional. The bitrate for compression (default is `10M`). `15M` is recommended for 1440p

### Example Command

To compress all videos located in `/home/user/videos` and save the compressed files to `/home/user/compressed_videos` with a bitrate of `5M`, you would run:

python compress_videos.py /home/user/videos /home/user/compressed_videos --bitrate 5M

## Notes

- The script will traverse the input directory recursively, compressing **ALL** supported video files it finds.
- If the output directory does not exist, it will be created automatically.
- The script will only process two videos at a time, one using GPU and one using CPU. Doing more at the same time is less efficient.
- I used it for compressing the Radeon ReLive folder. It managed to reduce its size to about half with 15M bitrate (from 40.9GiB to 20.1GiB)
- **Don't** point the input and the destination to the same folder.
- Most of the code was written with the help of AI

## Troubleshooting

- If you encounter issues with FFmpeg or encoding, ensure that FFmpeg is properly installed and that you have the required codecs available.
- If you have problems with GPU acceleration, ensure that your AMD drivers and VAAPI support are correctly set up.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
