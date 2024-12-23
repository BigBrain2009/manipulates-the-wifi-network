import socket
import threading
import random
import time

def send_packets(target_ip, target_port, duration):
    """
    Sends a large number of UDP packets to the specified IP and port for a defined duration.
    
    Args:
        target_ip (str): The target IP address.
        target_port (int): The target port.
        duration (int): The duration of the load test in seconds.
    """
    timeout = time.time() + duration  # Set the test duration
    packet = random._urandom(1024)  # Generate a random packet of 1 KB
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    packets_sent = 0

    print(f"Starting load test on {target_ip}:{target_port} for {duration} seconds...")
    
    while time.time() < timeout:
        try:
            sock.sendto(packet, (target_ip, target_port))  # Send a packet
            packets_sent += 1
            if packets_sent % 1000 == 0:
                print(f"[+] {packets_sent} packets sent...")
        except Exception as e:
            print(f"[-] Error: {e}")
            break

    print(f"Load test completed. Total packets sent: {packets_sent}")


if __name__ == "__main__":
    print("=== Network Load Test ===")
    
    try:
        target_ip = input("Enter the target IP address: ")
        target_port = int(input("Enter the target port (e.g., 80 for HTTP): "))
        duration = int(input("Enter the load test duration (in seconds): "))

        threads = []
        for _ in range(10):  # Create 10 threads to send packets in parallel
            thread = threading.Thread(target=send_packets, args=(target_ip, target_port, duration))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("Load test completed.")
    
    except KeyboardInterrupt:
        print("\n[!] Test interrupted by user.")
