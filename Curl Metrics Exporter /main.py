from prometheus_client import start_http_server, Gauge
import pycurl
import re
import time
import socket
import netifaces as ni

# Find the local interface with multiple IP addresses
def find_local_interface_with_ips():
    for interface in ni.interfaces():
        addrs = ni.ifaddresses(interface)
        if ni.AF_INET in addrs and len(addrs[ni.AF_INET]) > 1:
            return interface
    return None

local_interface = find_local_interface_with_ips()

if local_interface is None:
    raise Exception("No interface with multiple IP addresses found")

# Find all IP addresses associated with the local interface
def get_local_ips(interface):
    addrs = ni.ifaddresses(interface)
    return [(addr_info['addr'], addr_info['broadcast']) for addr_info in addrs[ni.AF_INET]]

local_ips = get_local_ips(local_interface)

# Create a Prometheus Gauge metric with labels for each destination and IP address
curl_success_metric = Gauge(
    'curl_success', 'Curl success status (1 for success, 0 for failure)', ['destination', 'ip_address', 'broadcast_ip']
)

# Function to run the curl command for a specific destination and IP
def curl_command(destination, ip, broadcast_ip):
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, f"http://{destination}")
        c.setopt(pycurl.INTERFACE, local_interface)
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
        c.setopt(pycurl.NOBODY, 1)
        c.perform()
        
        # Check if the curl command was successful (HTTP status code 200)
        if c.getinfo(pycurl.RESPONSE_CODE) == 200:
            return 1, broadcast_ip
        else:
            return 0, broadcast_ip
    except Exception as e:
        print(str(e))
        return 0, broadcast_ip
    finally:
        c.close()

if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000 (for exposing metrics)
    start_http_server(8000)

    while True:
        # Iterate through each IP address and get the result of the curl command for each destination
        for ip, broadcast_ip in local_ips:
            # Gather metrics for http://icanhazip.com
            curl_result, broadcast_ip = curl_command("icanhazip.com", ip, broadcast_ip)
            curl_success_metric.labels(destination="icanhazip.com", ip_address=ip, broadcast_ip=broadcast_ip).set(curl_result)

            # Gather metrics for 8.8.8.8
            curl_result, broadcast_ip = curl_command("8.8.8.8", ip, broadcast_ip)
            curl_success_metric.labels(destination="8.8.8.8", ip_address=ip, broadcast_ip=broadcast_ip).set(curl_result)

        # Sleep for a specified interval before running the curl command again
        time.sleep(60)  # Adjust the interval as needed
