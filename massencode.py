import os
import ffmpeg
import threading
from pathlib import Path
from queue import Queue
import argparse

# Function to compress a video with VAAPI (AMD GPU acceleration)
def compress_video_hw(input_path, output_path, bitrate="10M"):
    """
    Compress a video file using ffmpeg with VAAPI GPU acceleration and save to the output path.

    :param input_path: Path to the input video.
    :param output_path: Path where compressed video should be saved.
    :param bitrate: Compression bitrate (default is '10M').
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        print(f"Compressing video with HW acceleration:\nInput: {input_path}\nOutput: {output_path}")

        # Compress the video using VAAPI for AMD GPU acceleration
        ffmpeg.input(str(input_path), hwaccel='vaapi', hwaccel_device='/dev/dri/renderD128').output(
            str(output_path),
            vcodec='h264_vaapi',  # Use VAAPI for H.264 encoding
            video_bitrate=bitrate,
            vf='format=nv12|vaapi,hwupload'  # Format and upload the frames to the GPU
        ).run(overwrite_output=True)

        print(f"Compressed (HW): {input_path} -> {output_path}")

    except Exception as e:
        print(f"Error compressing {input_path} with HW acceleration: {e}")

# Function to compress a video with CPU (non-HW acceleration)
def compress_video_cpu(input_path, output_path, bitrate="10M"):
    """
    Compress a video file using ffmpeg with CPU encoding and save to the output path.

    :param input_path: Path to the input video.
    :param output_path: Path where compressed video should be saved.
    :param bitrate: Compression bitrate (default is '10M').
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        print(f"Compressing video with CPU:\nInput: {input_path}\nOutput: {output_path}")

        # Compress the video using CPU (libx264)
        ffmpeg.input(str(input_path)).output(
            str(output_path),
            vcodec='libx264',  # Use libx264 for H.264 encoding
            video_bitrate=bitrate
        ).run(overwrite_output=True)

        print(f"Compressed (CPU): {input_path} -> {output_path}")

    except Exception as e:
        print(f"Error compressing {input_path} with CPU: {e}")

# Worker function for processing jobs
def worker(queue, hw_mode):
    while True:
        # Get a job from the queue (blocking)
        input_file, output_file = queue.get()

        if hw_mode:
            compress_video_hw(input_file, output_file)
        else:
            compress_video_cpu(input_file, output_file)

        # Mark the job as done
        queue.task_done()

# Function to compress videos in a controlled manner
def compress_videos(input_dir, output_dir, bitrate="10M", extensions=(".mp4", ".mov", ".avi", ".mkv")):
    """
    Recursively find all video files in the input_dir, compress them using both HW and CPU methods,
    and save them in the output_dir, maintaining the directory structure.

    :param input_dir: Path to the source directory containing videos.
    :param output_dir: Path to the destination directory for compressed videos.
    :param bitrate: Compression bitrate (default is '10M').
    :param extensions: Tuple of file extensions to process.
    """
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()

    # Queue to hold video files
    queue = Queue()

    # Walk through the input directory and populate the queue
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(extensions):
                # Full path of the source video
                input_file = Path(root) / file

                # Define output path to maintain the same structure and keep the original name
                output_file = output_dir / input_file.relative_to(input_dir)

                # Add to the queue
                queue.put((input_file, output_file))

    # Create and start worker threads
    thread_hw = threading.Thread(target=worker, args=(queue, True), daemon=True)
    thread_cpu = threading.Thread(target=worker, args=(queue, False), daemon=True)

    # Start the threads
    thread_hw.start()
    thread_cpu.start()

    # Wait for the queue to be processed
    queue.join()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Compress multiple videos with GPU and CPU at the same time.")
    parser.add_argument("input_folder", type=str, help="Path to the input folder containing videos.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder for compressed videos.")
    parser.add_argument("--bitrate", type=str, default="10M", help="Bitrate for compression (default is 10M).")

    args = parser.parse_args()

    # Call the function to compress videos
    compress_videos(args.input_folder, args.output_folder, bitrate=args.bitrate)

if __name__ == "__main__":
    main()