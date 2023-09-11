from prometheus_client import start_http_server, Gauge
import time
import re
import os

# Define a Prometheus Gauge metric with labels for each channel
ffmpeg_metrics = Gauge(
    'ffmpeg_channel_metrics',
    'FFmpeg Channel Metrics (fps, time, bitrate, speed)',
    ['channel_name', 'fps', 'bitrate', 'speed']
)

# Function to parse and extract metrics from an FFmpeg log file
def extract_metrics_from_log(log_file):
    try:
        with open(log_file, 'r') as f:
            log_content = f.read()

            # Use regex to find metrics data in the log, handling 'x' in speed
            pattern = r'fps=(\s*\d+\.?\d*) q=-1\.0 size=\s*(\d+)kB time=([0-9:.]+) bitrate=(\d+\.\d+kbits/s) speed=(\s*\d+\.?\d*)x'
            matches = re.findall(pattern, log_content)

            for match in matches:
                fps, size, time, bitrate, speed = match
                speed = float(speed) if speed else 0.0  # Handle 'x' in speed
                yield {
                    'fps': float(fps.strip()),
                    'size': int(size),
                    'bitrate': float(bitrate.strip().replace('kbits/s', '')),
                    'speed': speed
                }

    except Exception as e:
        print(f"Error reading log file {log_file}: {str(e)}")

# Function to update Prometheus metrics with the extracted data for a log file
def update_prometheus_metrics(log_file):
    for channel_data in extract_metrics_from_log(log_file):
        channel_name = os.path.basename(log_file).split('.')[0]
        ffmpeg_metrics.labels(channel_name, channel_data['fps'], channel_data['bitrate'], channel_data['speed']).set(1)

# Directory containing FFmpeg log files
log_directory = '/root/log/'

if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000 (for exposing metrics)
    start_http_server(8000)

    while True:
        # Iterate through log files in the directory and update Prometheus metrics for each
        for log_file in os.listdir(log_directory):
            if log_file.endswith('.log'):
                log_file_path = os.path.join(log_directory, log_file)
                update_prometheus_metrics(log_file_path)

        time.sleep(10)
