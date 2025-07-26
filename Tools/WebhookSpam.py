import time
import requests
import random
import string
import threading
import os
from colorama import Fore, Style, init

init(autoreset=True)

class AdvancedWebhookSpammer:
    def __init__(self):
        self.webhook_url = None
        self.message = None
        self.count = 1000
        self.delay = 0.1
        self.spam_mode = "normal"
        self.is_spamming = False
        self.stats = {
            'sent': 0,
            'failed': 0,
            'start_time': 0
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
        print(f"{Fore.CYAN}║                          ADVANCED WEBHOOK SPAMMER                           ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        print(f"{Fore.YELLOW}[*] Enter Discord webhook URL: ", end="")
        self.webhook_url = input().strip()
        
        if not (self.webhook_url.startswith("https://discord.com/api/webhooks/") or 
                self.webhook_url.startswith("https://discordapp.com/api/webhooks/")):
            print(f"{Fore.RED}[!] Invalid webhook URL format!")
            return False

        print(f"{Fore.YELLOW}[*] Select spam mode:")
        print(f"{Fore.WHITE}    1. Normal (Single message)")
        print(f"{Fore.WHITE}    2. Random (Random messages)")
        print(f"{Fore.WHITE}    3. Embed (Rich embeds)")
        print(f"{Fore.WHITE}    4. Mention (With mentions)")
        print(f"{Fore.WHITE}    5. File (With file attachments)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[*] Enter choice (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    modes = {
                        '1': 'normal',
                        '2': 'random',
                        '3': 'embed',
                        '4': 'mention',
                        '5': 'file'
                    }
                    self.spam_mode = modes[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-5.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        if self.spam_mode == 'normal':
            print(f"{Fore.YELLOW}[*] Enter message to spam: ", end="")
            self.message = input().strip()
        elif self.spam_mode == 'random':
            print(f"{Fore.YELLOW}[*] Enter base message (will be randomized): ", end="")
            self.message = input().strip()

        print(f"{Fore.YELLOW}[*] Enter number of messages (default 1000): ", end="")
        count_input = input().strip()
        self.count = int(count_input) if count_input else 1000

        print(f"{Fore.YELLOW}[*] Enter delay between messages in seconds (default 0.1): ", end="")
        delay_input = input().strip()
        self.delay = float(delay_input) if delay_input else 0.1

        return True

    def generate_random_message(self):
        """Generate random message variations"""
        random_words = [
            "Hello", "World", "Test", "Spam", "Message", "Random", "Cool", "Awesome",
            "Amazing", "Incredible", "Fantastic", "Wonderful", "Great", "Good", "Nice"
        ]
        
        if self.message:
            base = self.message
        else:
            base = random.choice(random_words)
        
        # Add random elements
        variations = [
            f"{base} {random.randint(1, 999)}",
            f"{base} {'!' * random.randint(1, 5)}",
            f"{base} {'?' * random.randint(1, 3)}",
            f"{base} {'*' * random.randint(1, 3)}",
            f"{base} {'~' * random.randint(1, 3)}",
            f"{base} {random.choice(random_words)}",
            f"{base} {'💀' * random.randint(1, 3)}",
            f"{base} {'🔥' * random.randint(1, 3)}",
            f"{base} {'😎' * random.randint(1, 3)}"
        ]
        
        return random.choice(variations)

    def create_embed(self):
        """Create rich embed message"""
        colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0xFFA500, 0x800080]
        
        embed = {
            "title": f"Spam Message {random.randint(1, 999)}",
            "description": self.message or "Random spam message",
            "color": random.choice(colors),
            "fields": [
                {
                    "name": "Spam Counter",
                    "value": f"Message #{self.stats['sent'] + 1}",
                    "inline": True
                },
                {
                    "name": "Random ID",
                    "value": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Advanced Webhook Spammer by Sqrilizz"
            },
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
        
        return {"embeds": [embed]}

    def create_mention_message(self):
        """Create message with mentions"""
        mentions = [
            "@everyone", "@here", "<@&123456789>", "<@123456789>",
            "👋 @everyone", "🚨 @here", "📢 @everyone"
        ]
        
        base_msg = self.message or "Spam message"
        return f"{random.choice(mentions)} {base_msg} {random.randint(1, 999)}"

    def send_message(self, payload):
        """Send message to webhook"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.post(self.webhook_url, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 204:
                self.stats['sent'] += 1
                return True
            else:
                self.stats['failed'] += 1
                return False
                
        except Exception as e:
            self.stats['failed'] += 1
            return False

    def spam_thread(self):
        """Main spam thread"""
        while self.is_spamming and self.stats['sent'] < self.count:
            try:
                if self.spam_mode == 'normal':
                    payload = {'content': self.message}
                elif self.spam_mode == 'random':
                    payload = {'content': self.generate_random_message()}
                elif self.spam_mode == 'embed':
                    payload = self.create_embed()
                elif self.spam_mode == 'mention':
                    payload = {'content': self.create_mention_message()}
                elif self.spam_mode == 'file':
                    payload = {
                        'content': self.message or "File spam",
                        'file': {
                            'name': f'spam_{random.randint(1, 999)}.txt',
                            'content': f'Spam file content {random.randint(1, 999)}'
                        }
                    }
                
                if self.send_message(payload):
                    elapsed = time.time() - self.stats['start_time']
                    speed = self.stats['sent'] / elapsed if elapsed > 0 else 0
                    
                    print(f"\r{Fore.GREEN}[+] Sent: {self.stats['sent']}/{self.count} | "
                          f"Failed: {self.stats['failed']} | "
                          f"Speed: {speed:.1f} msg/s | "
                          f"Time: {int(elapsed)}s", end='', flush=True)
                
                time.sleep(self.delay)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n{Fore.RED}[!] Error: {e}")
                time.sleep(1)

    def print_stats(self):
        """Print real-time statistics"""
        while self.is_spamming:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                speed = self.stats['sent'] / elapsed
                success_rate = (self.stats['sent'] / (self.stats['sent'] + self.stats['failed'])) * 100 if (self.stats['sent'] + self.stats['failed']) > 0 else 0
                
                print(f"\r{Fore.CYAN}[*] Mode: {self.spam_mode} | "
                      f"Sent: {self.stats['sent']}/{self.count} | "
                      f"Failed: {self.stats['failed']} | "
                      f"Speed: {speed:.1f} msg/s | "
                      f"Success: {success_rate:.1f}% | "
                      f"Time: {int(elapsed)}s", end='', flush=True)
            
            time.sleep(1)

    def start_spam(self):
        """Start the webhook spam"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return

        if not self.get_user_input():
            return

        print(f"\n{Fore.GREEN}[+] Starting {self.spam_mode} spam attack")
        print(f"{Fore.GREEN}[+] Target: {self.webhook_url}")
        print(f"{Fore.GREEN}[+] Count: {self.count} | Delay: {self.delay}s")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop\n")

        self.is_spamming = True
        self.stats['start_time'] = time.time()

        # Start spam thread
        spam_thread = threading.Thread(target=self.spam_thread)
        spam_thread.daemon = True
        spam_thread.start()

        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()

        try:
            spam_thread.join()
        except KeyboardInterrupt:
            pass

        self.is_spamming = False
        time.sleep(1)

        # Final statistics
        total_time = time.time() - self.stats['start_time']
        success_rate = (self.stats['sent'] / (self.stats['sent'] + self.stats['failed'])) * 100 if (self.stats['sent'] + self.stats['failed']) > 0 else 0

        print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              SPAM COMPLETED                                 ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}[*] Spam Mode: {self.spam_mode}")
        print(f"{Fore.YELLOW}[*] Target Webhook: {self.webhook_url}")
        print(f"{Fore.YELLOW}[*] Duration: {total_time:.1f} seconds")
        print(f"{Fore.YELLOW}[*] Messages Sent: {self.stats['sent']:,}")
        print(f"{Fore.YELLOW}[*] Messages Failed: {self.stats['failed']:,}")
        print(f"{Fore.YELLOW}[*] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.YELLOW}[*] Average Speed: {self.stats['sent']/total_time:.1f} messages/sec")

def main():
    spammer = AdvancedWebhookSpammer()
    spammer.print_banner()
    spammer.start_spam()

if __name__ == '__main__':
    main()
