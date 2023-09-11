# FFmpeg Log Metrics Exporter

This Python script is designed to export metrics to Prometheus from FFmpeg log files, allowing you to monitor the performance of various FFmpeg channels. The script extracts metrics such as frames per second (fps), bitrate, and speed from each log file and exposes them as Prometheus metrics.

## Requirements

- Python 3.x
- `prometheus_client` library (`pip install prometheus_client`)

## Functionality

The script performs the following tasks:

1. Iterates through all log files in a specified directory (default: `/root/log/`).
2. Parses each FFmpeg log file to extract metrics using regular expressions.
3. Creates a Prometheus Gauge metric named `ffmpeg_channel_metrics` with labels for `channel_name`, `fps`, `bitrate`, and `speed`.
4. Updates the Prometheus metrics for each channel with the extracted data.
5. Exposes the metrics via an HTTP server on port 8000, allowing Prometheus to scrape and store the metric values.

## Usage

1. Ensure you have the required Python library installed as mentioned in the requirements section.

2. Place your FFmpeg log files (e.g., `channel_name.log`) in the `/root/log/` directory, or specify a different directory by modifying the `log_directory` variable in the script.

3. Run the script using the following command:

   ```bash
   python main.py

4. The script will start an HTTP server on port 8000 and continuously monitor the FFmpeg log files in the specified directory.

5. You can access the Prometheus metrics at `http://localhost:8000/metrics`.

## Prometheus Configuration

To collect and store the metrics, configure Prometheus to scrape the metrics from `http://localhost:8000/metrics`. Here's an example `prometheus.yml` configuration:

```bash
scrape_configs:
  - job_name: 'ffmpeg_metrics'
    static_configs:
      - targets: ['localhost:8000']
```
- Make sure to reload or restart Prometheus after updating the configuration.

## Log File Naming Convention

The script assumes a naming convention where each FFmpeg log file represents a separate channel and follows the format `channel_name.log`. The `channel_name` portion of the log file name will be used as the label in Prometheus metrics.