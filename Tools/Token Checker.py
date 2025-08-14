import requests
import json
import time
import threading
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

class AdvancedTokenChecker:
    def __init__(self):
        self.tokens = []
        self.valid_tokens = []
        self.invalid_tokens = []
        self.checked_tokens = 0
        self.total_tokens = 0
        self.is_checking = False
        self.threads = 200  # Увеличиваем до 200 потоков для максимальной скорости проверки
        self.delay = 0.1

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
        print(f"{Fore.CYAN}║                          ADVANCED TOKEN CHECKER                               ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Select input method:")
        print(f"{Fore.WHITE}    1. Single token")
        print(f"{Fore.WHITE}    2. Multiple tokens (one per line)")
        print(f"{Fore.WHITE}    3. Load from file")
        print(f"{Fore.WHITE}    4. Generate tokens")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[*] Enter choice (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    if choice == '1':
                        self.load_single_token()
                    elif choice == '2':
                        self.load_multiple_tokens()
                    elif choice == '3':
                        self.load_from_file()
                    elif choice == '4':
                        self.generate_tokens()
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        if not self.tokens:
            print(f"{Fore.RED}[!] No tokens loaded!")
            return False

        print(f"{Fore.YELLOW}[*] Enter number of threads (default 200): ", end="")
        threads_input = input().strip()
        self.threads = int(threads_input) if threads_input else 200

        print(f"{Fore.YELLOW}[*] Enter delay between checks in seconds (default 0.1): ", end="")
        delay_input = input().strip()
        self.delay = float(delay_input) if delay_input else 0.1

        return True

    def load_single_token(self):
        """Load a single token"""
        print(f"{Fore.YELLOW}[*] Enter Discord token: ", end="")
        token = input().strip()
        if token:
            self.tokens.append(token)
            print(f"{Fore.GREEN}[+] Loaded 1 token")

    def load_multiple_tokens(self):
        """Load multiple tokens"""
        print(f"{Fore.YELLOW}[*] Enter tokens (one per line, press Enter twice when done):")
        print(f"{Fore.WHITE}    (Press Enter on empty line to finish)")
        
        while True:
            token = input().strip()
            if not token:
                break
            self.tokens.append(token)
        
        print(f"{Fore.GREEN}[+] Loaded {len(self.tokens)} tokens")

    def load_from_file(self):
        """Load tokens from file"""
        print(f"{Fore.YELLOW}[*] Enter file path: ", end="")
        file_path = input().strip()
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    token = line.strip()
                    if token:
                        self.tokens.append(token)
            print(f"{Fore.GREEN}[+] Loaded {len(self.tokens)} tokens from {file_path}")
        except FileNotFoundError:
            print(f"{Fore.RED}[!] File not found: {file_path}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error reading file: {e}")

    def generate_tokens(self):
        """Generate random tokens for testing"""
        print(f"{Fore.YELLOW}[*] Enter number of tokens to generate: ", end="")
        count = int(input().strip())
        
        # Generate some example tokens (these won't be valid)
        for i in range(count):
            token = f"MT{''.join(['x' for _ in range(20)])}.{''.join(['y' for _ in range(6)])}.{''.join(['z' for _ in range(27)])}"
            self.tokens.append(token)
        
        print(f"{Fore.GREEN}[+] Generated {count} example tokens")

    def check_token(self, token):
        """Check if a token is valid"""
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        try:
            # Check user info
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('username', 'Unknown')
                user_id = user_data.get('id', 'Unknown')
                email = user_data.get('email', 'No email')
                phone = user_data.get('phone', 'No phone')
                nitro = user_data.get('premium_type', 0)
                
                # Check billing info
                billing_response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, timeout=10)
                billing_methods = len(billing_response.json()) if billing_response.status_code == 200 else 0
                
                # Check guilds
                guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, timeout=10)
                guilds = len(guilds_response.json()) if guilds_response.status_code == 200 else 0
                
                token_info = {
                    'token': token,
                    'username': username,
                    'user_id': user_id,
                    'email': email,
                    'phone': phone,
                    'nitro': nitro,
                    'billing_methods': billing_methods,
                    'guilds': guilds
                }
                
                self.valid_tokens.append(token_info)
                print(f"{Fore.GREEN}[+] VALID | {username}#{user_data.get('discriminator', '0000')} | ID: {user_id} | Nitro: {nitro} | Billing: {billing_methods} | Guilds: {guilds}")
                return True
            else:
                self.invalid_tokens.append(token)
                print(f"{Fore.RED}[-] INVALID | {token[:20]}...")
                return False
                
        except Exception as e:
            self.invalid_tokens.append(token)
            print(f"{Fore.RED}[-] ERROR | {token[:20]}... | {str(e)}")
            return False

    def check_thread(self):
        """Оптимизированный token checking thread с rate limiting"""
        while self.is_checking and self.tokens:
            try:
                token = self.tokens.pop(0)
                self.check_token(token)
                self.checked_tokens += 1
                
                # Интеллектуальная задержка для rate limiting
                if self.checked_tokens % 50 == 0:  # Каждые 50 токенов
                    time.sleep(0.1)  # Небольшая пауза
                else:
                    time.sleep(self.delay)
                    
            except IndexError:
                break
            except Exception as e:
                print(f"{Fore.RED}[!] Thread error: {e}")

    def print_stats(self):
        """Print real-time statistics"""
        while self.is_checking:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                speed = self.checked_tokens / elapsed
                progress = (self.checked_tokens / self.total_tokens) * 100 if self.total_tokens > 0 else 0
                
                print(f"\r{Fore.CYAN}[*] Progress: {self.checked_tokens}/{self.total_tokens} ({progress:.1f}%) | "
                      f"Valid: {len(self.valid_tokens)} | "
                      f"Invalid: {len(self.invalid_tokens)} | "
                      f"Speed: {speed:.1f} tokens/sec | "
                      f"Time: {int(elapsed)}s", end='', flush=True)
            
            time.sleep(1)

    def save_results(self):
        """Save results to files"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save valid tokens
        if self.valid_tokens:
            valid_file = f"valid_tokens_{timestamp}.txt"
            with open(valid_file, 'w') as f:
                for token_info in self.valid_tokens:
                    f.write(f"Token: {token_info['token']}\n")
                    f.write(f"Username: {token_info['username']}\n")
                    f.write(f"User ID: {token_info['user_id']}\n")
                    f.write(f"Email: {token_info['email']}\n")
                    f.write(f"Phone: {token_info['phone']}\n")
                    f.write(f"Nitro: {token_info['nitro']}\n")
                    f.write(f"Billing Methods: {token_info['billing_methods']}\n")
                    f.write(f"Guilds: {token_info['guilds']}\n")
                    f.write("-" * 50 + "\n")
            print(f"{Fore.GREEN}[+] Valid tokens saved to: {valid_file}")
        
        # Save invalid tokens
        if self.invalid_tokens:
            invalid_file = f"invalid_tokens_{timestamp}.txt"
            with open(invalid_file, 'w') as f:
                for token in self.invalid_tokens:
                    f.write(f"{token}\n")
            print(f"{Fore.YELLOW}[+] Invalid tokens saved to: {invalid_file}")

    def start_checking(self):
        """Start the token checking process"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return

        if not self.get_user_input():
            return

        self.total_tokens = len(self.tokens)
        print(f"\n{Fore.GREEN}[+] Starting token check")
        print(f"{Fore.GREEN}[+] Total tokens: {self.total_tokens}")
        print(f"{Fore.GREEN}[+] Threads: {self.threads}")
        print(f"{Fore.GREEN}[+] Delay: {self.delay}s")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop\n")

        self.is_checking = True
        self.start_time = time.time()

        # Start checking threads
        check_threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.check_thread)
            thread.daemon = True
            thread.start()
            check_threads.append(thread)

        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()

        try:
            # Wait for all threads to complete
            for thread in check_threads:
                thread.join()
        except KeyboardInterrupt:
            pass

        self.is_checking = False
        time.sleep(1)

        # Final statistics
        total_time = time.time() - self.start_time
        success_rate = (len(self.valid_tokens) / self.total_tokens) * 100 if self.total_tokens > 0 else 0

        print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              CHECK COMPLETED                                  ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}[*] Total Tokens: {self.total_tokens}")
        print(f"{Fore.YELLOW}[*] Valid Tokens: {len(self.valid_tokens)}")
        print(f"{Fore.YELLOW}[*] Invalid Tokens: {len(self.invalid_tokens)}")
        print(f"{Fore.YELLOW}[*] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.YELLOW}[*] Duration: {total_time:.1f} seconds")
        print(f"{Fore.YELLOW}[*] Average Speed: {self.total_tokens/total_time:.1f} tokens/sec")

        # Save results
        if self.valid_tokens or self.invalid_tokens:
            print(f"\n{Fore.YELLOW}[?] Save results to files? (y/n): ", end="")
            if input().lower() == 'y':
                self.save_results()

def main():
    checker = AdvancedTokenChecker()
    checker.print_banner()
    checker.start_checking()

if __name__ == '__main__':
    main() 