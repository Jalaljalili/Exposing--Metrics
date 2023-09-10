# Multi-IP Curl Metrics Exporter with PyCurl

This Python script is designed to export metrics to Prometheus for multiple IP addresses on a local network interface using the `pycurl` library. It allows you to monitor the availability of various IP addresses from your local machine.

## Requirements

- Python 3.x
- `prometheus_client` library (`pip install prometheus_client`)
- `pycurl` library (`pip install pycurl`)
- `netifaces` library (`pip install netifaces`)

## Functionality

The script performs the following tasks:

1. Identifies a local network interface with multiple assigned IP addresses.
2. Retrieves all IP addresses associated with the selected network interface.
3. Creates a Prometheus Gauge metric for each IP address with labels for the destination and broadcast IP.
4. Uses `pycurl` to make HTTP requests to two destinations: `http://icanhazip.com` and `8.8.8.8`.
5. Updates the Prometheus metrics with the success or failure status (1 for success, 0 for failure) of each HTTP request.

The metrics are exposed via an HTTP server on port 8000, which Prometheus can scrape to collect and store the metric values.

## Usage

1. Ensure you have the required Python libraries installed as mentioned in the requirements section.

2. Run the script using the following command:

   ```bash
   python main.py
