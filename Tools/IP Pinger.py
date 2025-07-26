import socket
import threading
import time
import random
import os
import sys
import subprocess
import platform
from colorama import Fore, Style, init

init(autoreset=True)

class AdvancedIPPinger:
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.ping_mode = "tcp"
        self.threads = 10
        self.duration = 60
        self.is_pinging = False
        self.stats = {
            'successful_pings': 0,
            'failed_pings': 0,
            'start_time': 0,
            'total_packets': 0
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
        print(f"{Fore.CYAN}║                            ADVANCED IP PINGER                                ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Select ping mode:")
        print(f"{Fore.WHITE}    1. TCP Ping (Port connection)")
        print(f"{Fore.WHITE}    2. ICMP Ping (Traditional ping)")
        print(f"{Fore.WHITE}    3. UDP Ping (UDP port check)")
        print(f"{Fore.WHITE}    4. HTTP Ping (Web server check)")
        print(f"{Fore.WHITE}    5. Multi-Port Scan")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[*] Enter choice (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    modes = {
                        '1': 'tcp',
                        '2': 'icmp',
                        '3': 'udp',
                        '4': 'http',
                        '5': 'multiport'
                    }
                    self.ping_mode = modes[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-5.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        print(f"{Fore.YELLOW}[*] Enter target IP: ", end="")
        self.target_ip = input().strip()
        
        if self.ping_mode == 'multiport':
            print(f"{Fore.YELLOW}[*] Enter port range (e.g., 80-443 or 22,80,443): ", end="")
            port_input = input().strip()
            if '-' in port_input:
                start, end = map(int, port_input.split('-'))
                self.ports = list(range(start, end + 1))
            else:
                self.ports = [int(p) for p in port_input.split(',')]
        else:
            print(f"{Fore.YELLOW}[*] Enter target port (default 80): ", end="")
            port_input = input().strip()
            self.target_port = int(port_input) if port_input else 80

        print(f"{Fore.YELLOW}[*] Enter number of threads (default 10): ", end="")
        threads_input = input().strip()
        self.threads = int(threads_input) if threads_input else 10

        print(f"{Fore.YELLOW}[*] Enter ping duration in seconds (default 60): ", end="")
        duration_input = input().strip()
        self.duration = int(duration_input) if duration_input else 60

        return True

    def tcp_ping(self, ip, port):
        """TCP ping to check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            start_time = time.time()
            result = sock.connect_ex((ip, port))
            end_time = time.time()
            sock.close()
            
            if result == 0:
                latency = (end_time - start_time) * 1000
                self.stats['successful_pings'] += 1
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def icmp_ping(self, ip):
        """ICMP ping using system ping command"""
        try:
            if platform.system().lower() == "windows":
                cmd = f"ping -n 1 -w 1000 {ip}"
            else:
                cmd = f"ping -c 1 -W 1 {ip}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract latency from ping output
                output = result.stdout
                if "time=" in output:
                    latency_str = output.split("time=")[1].split()[0]
                    latency = float(latency_str.replace("ms", ""))
                else:
                    latency = 0
                
                self.stats['successful_pings'] += 1
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def udp_ping(self, ip, port):
        """UDP ping to check if port responds"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            start_time = time.time()
            sock.sendto(b"ping", (ip, port))
            try:
                data, addr = sock.recvfrom(1024)
                end_time = time.time()
                latency = (end_time - start_time) * 1000
                sock.close()
                self.stats['successful_pings'] += 1
                return True, latency
            except socket.timeout:
                sock.close()
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def http_ping(self, ip, port):
        """HTTP ping to check web server"""
        try:
            import requests
            url = f"http://{ip}:{port}"
            start_time = time.time()
            response = requests.get(url, timeout=2, verify=False)
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            
            if response.status_code < 500:
                self.stats['successful_pings'] += 1
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def ping_thread(self):
        """Main ping thread"""
        while self.is_pinging:
            try:
                if self.ping_mode == 'tcp':
                    success, latency = self.tcp_ping(self.target_ip, self.target_port)
                    if success:
                        print(f"{Fore.GREEN}[+] TCP {self.target_ip}:{self.target_port} - {latency:.1f}ms")
                    else:
                        print(f"{Fore.RED}[-] TCP {self.target_ip}:{self.target_port} - TIMEOUT")
                
                elif self.ping_mode == 'icmp':
                    success, latency = self.icmp_ping(self.target_ip)
                    if success:
                        print(f"{Fore.GREEN}[+] ICMP {self.target_ip} - {latency:.1f}ms")
                    else:
                        print(f"{Fore.RED}[-] ICMP {self.target_ip} - TIMEOUT")
                
                elif self.ping_mode == 'udp':
                    success, latency = self.udp_ping(self.target_ip, self.target_port)
                    if success:
                        print(f"{Fore.GREEN}[+] UDP {self.target_ip}:{self.target_port} - {latency:.1f}ms")
                    else:
                        print(f"{Fore.RED}[-] UDP {self.target_ip}:{self.target_port} - TIMEOUT")
                
                elif self.ping_mode == 'http':
                    success, latency = self.http_ping(self.target_ip, self.target_port)
                    if success:
                        print(f"{Fore.GREEN}[+] HTTP {self.target_ip}:{self.target_port} - {latency:.1f}ms")
                    else:
                        print(f"{Fore.RED}[-] HTTP {self.target_ip}:{self.target_port} - TIMEOUT")
                
                elif self.ping_mode == 'multiport':
                    for port in self.ports:
                        success, latency = self.tcp_ping(self.target_ip, port)
                        if success:
                            print(f"{Fore.GREEN}[+] TCP {self.target_ip}:{port} - {latency:.1f}ms")
                        else:
                            print(f"{Fore.RED}[-] TCP {self.target_ip}:{port} - TIMEOUT")
                
                self.stats['total_packets'] += 1
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}")
                time.sleep(1)

    def print_stats(self):
        """Print real-time statistics"""
        while self.is_pinging:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                pings_per_sec = self.stats['total_packets'] / elapsed
                success_rate = (self.stats['successful_pings'] / (self.stats['successful_pings'] + self.stats['failed_pings'])) * 100 if (self.stats['successful_pings'] + self.stats['failed_pings']) > 0 else 0
                
                print(f"\r{Fore.CYAN}[*] Mode: {self.ping_mode.upper()} | "
                      f"Target: {self.target_ip} | "
                      f"Success: {self.stats['successful_pings']} | "
                      f"Failed: {self.stats['failed_pings']} | "
                      f"Rate: {pings_per_sec:.1f} pkt/s | "
                      f"Success: {success_rate:.1f}% | "
                      f"Time: {int(elapsed)}s", end='', flush=True)
            
            time.sleep(1)

    def start_ping(self):
        """Start the ping attack"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return

        if not self.get_user_input():
            return

        print(f"\n{Fore.GREEN}[+] Starting {self.ping_mode.upper()} ping to {self.target_ip}")
        if self.ping_mode == 'multiport':
            print(f"{Fore.GREEN}[+] Ports: {self.ports}")
        else:
            print(f"{Fore.GREEN}[+] Port: {self.target_port}")
        print(f"{Fore.GREEN}[+] Threads: {self.threads} | Duration: {self.duration}s")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop\n")

        self.is_pinging = True
        self.stats['start_time'] = time.time()

        # Start ping threads
        ping_threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.ping_thread)
            thread.daemon = True
            thread.start()
            ping_threads.append(thread)

        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()

        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            pass

        self.is_pinging = False
        time.sleep(1)

        # Final statistics
        total_time = time.time() - self.stats['start_time']
        success_rate = (self.stats['successful_pings'] / (self.stats['successful_pings'] + self.stats['failed_pings'])) * 100 if (self.stats['successful_pings'] + self.stats['failed_pings']) > 0 else 0

        print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              PING COMPLETED                                  ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}[*] Ping Mode: {self.ping_mode.upper()}")
        print(f"{Fore.YELLOW}[*] Target: {self.target_ip}")
        if self.ping_mode == 'multiport':
            print(f"{Fore.YELLOW}[*] Ports Scanned: {len(self.ports)}")
        else:
            print(f"{Fore.YELLOW}[*] Port: {self.target_port}")
        print(f"{Fore.YELLOW}[*] Duration: {total_time:.1f} seconds")
        print(f"{Fore.YELLOW}[*] Successful Pings: {self.stats['successful_pings']:,}")
        print(f"{Fore.YELLOW}[*] Failed Pings: {self.stats['failed_pings']:,}")
        print(f"{Fore.YELLOW}[*] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.YELLOW}[*] Average Speed: {self.stats['total_packets']/total_time:.1f} pings/sec")

def main():
    pinger = AdvancedIPPinger()
    pinger.print_banner()
    pinger.start_ping()

if __name__ == '__main__':
    main()