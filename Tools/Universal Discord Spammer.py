import requests
import time
import random
import string
import threading
import json
import os
import sys
from colorama import Fore, Style, init
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Добавляем src в путь для импорта UI компонентов
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.utils.ui import (
        print_banner, print_header, print_separator, print_success, 
        print_error, print_warning, print_info, Spinner, ProgressBar, 
        Notification, confirm_action
    )
    from src.utils.logo import QuantumKitLogo
    NEW_UI_AVAILABLE = True
except ImportError:
    NEW_UI_AVAILABLE = False

init(autoreset=True)

class UniversalDiscordSpammer:
    def __init__(self):
        self.token = None
        self.webhook_url = None
        self.channel_id = None
        self.message = None
        self.count = 1000
        self.delay = 0.01
        self.spam_mode = "normal"
        self.spam_type = "webhook"
        self.is_spamming = False
        self.proxies = []
        self.load_proxies()
        self.stats = {
            'sent': 0,
            'failed': 0,
            'servers_processed': 0,
            'start_time': 0,
            'total_bytes': 0
        }
        self.session = requests.Session()
        self.servers = []
        self.channels = []
        
        # Performance settings
        self.max_workers = 100
        self.batch_size = 50
        self.connection_pool_size = 100
        self.retry_attempts = 3

    def load_proxies(self):
        """Load proxies from proxies.txt"""
        try:
            if os.path.exists('Tools/proxies.txt'):
                with open('Tools/proxies.txt', 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                if NEW_UI_AVAILABLE:
                    print_success(f"Loaded {len(self.proxies)} proxies")
                else:
                    print(f"{Fore.CYAN}[*] Loaded {len(self.proxies)} proxies")
        except:
            pass

    def print_banner(self):
        """Print modern banner"""
        if NEW_UI_AVAILABLE:
            print_banner()
            print_header("Universal Discord Spammer v7.0")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(QuantumKitLogo.get_main_logo())
            print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                    UNIVERSAL DISCORD SPAMMER v7.0                          ║")
            print(f"{Fore.CYAN}║                           🚀 MAXIMUM PERFORMANCE MODE 🚀                    ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Get user input with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Configuration")
        else:
            print(f"{Fore.CYAN}[*] Universal Discord Spammer Configuration")
            print(f"{Fore.CYAN}[*] ========================================\n")
        
        # Spam Type Selection
        print(f"{Fore.CYAN}[*] Spam Types:")
        print(f"{Fore.WHITE}    1. Webhook Spam - спам через вебхуки")
        print(f"{Fore.WHITE}    2. Token Single - спам в один канал через токен")
        print(f"{Fore.WHITE}    3. Token Mass - спам на все серверы через токен")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Choose type (1-3): ").strip()
                if choice == '1':
                    self.spam_type = "webhook"
                    break
                elif choice == '2':
                    self.spam_type = "token_single"
                    break
                elif choice == '3':
                    self.spam_type = "token_mass"
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Invalid choice. Please enter 1-3.")
                    else:
                        print(f"{Fore.RED}[!] Invalid choice. Please enter 1-3.")
            except KeyboardInterrupt:
                if NEW_UI_AVAILABLE:
                    print_warning("Operation cancelled")
                else:
                    print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Get specific inputs based on type
        if self.spam_type == "webhook":
            return self.get_webhook_input()
        else:
            return self.get_token_input()

    def get_webhook_input(self):
        """Get webhook input with modern UI"""
        if NEW_UI_AVAILABLE:
            print_info("Webhook Configuration")
        else:
            print(f"\n{Fore.CYAN}[*] Webhook Configuration")
        
        while True:
            webhook = input(f"{Fore.YELLOW}[?] Enter Discord webhook URL: ").strip()
            if webhook:
                if webhook.startswith('https://discord.com/api/webhooks/'):
                    self.webhook_url = webhook
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Invalid Discord webhook URL!")
                    else:
                        print(f"{Fore.RED}[!] Invalid Discord webhook URL!")
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Webhook URL cannot be empty!")
                else:
                    print(f"{Fore.RED}[!] Webhook URL cannot be empty!")

        # Message configuration
        print(f"\n{Fore.CYAN}[*] Message Configuration:")
        print(f"{Fore.WHITE}    1. Custom message")
        print(f"{Fore.WHITE}    2. Random messages")
        print(f"{Fore.WHITE}    3. Embed message")
        print(f"{Fore.WHITE}    4. Mention spam")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Choose message type (1-4): ").strip()
                if choice == '1':
                    self.message = input(f"{Fore.YELLOW}[?] Enter custom message: ").strip()
                    break
                elif choice == '2':
                    self.message = "random"
                    break
                elif choice == '3':
                    self.message = "embed"
                    break
                elif choice == '4':
                    self.message = "mention"
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Invalid choice. Please enter 1-4.")
                    else:
                        print(f"{Fore.RED}[!] Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                return False

        # Performance settings
        print(f"\n{Fore.CYAN}[*] Performance Settings:")
        self.count = int(input(f"{Fore.YELLOW}[?] Number of messages (default 1000): ").strip() or "1000")
        self.delay = float(input(f"{Fore.YELLOW}[?] Delay between messages in seconds (default 0.01): ").strip() or "0.01")
        
        return True

    def get_token_input(self):
        """Get token input with modern UI"""
        if NEW_UI_AVAILABLE:
            print_info("Token Configuration")
        else:
            print(f"\n{Fore.CYAN}[*] Token Configuration")
        
        while True:
            token = input(f"{Fore.YELLOW}[?] Enter Discord token: ").strip()
            if token:
                self.token = token
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Token cannot be empty!")
                else:
                    print(f"{Fore.RED}[!] Token cannot be empty!")

        if self.spam_type == "token_single":
            while True:
                channel_id = input(f"{Fore.YELLOW}[?] Enter channel ID: ").strip()
                if channel_id:
                    self.channel_id = channel_id
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Channel ID cannot be empty!")
                    else:
                        print(f"{Fore.RED}[!] Channel ID cannot be empty!")

        # Message configuration (same as webhook)
        print(f"\n{Fore.CYAN}[*] Message Configuration:")
        print(f"{Fore.WHITE}    1. Custom message")
        print(f"{Fore.WHITE}    2. Random messages")
        print(f"{Fore.WHITE}    3. Embed message")
        print(f"{Fore.WHITE}    4. Mention spam")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Choose message type (1-4): ").strip()
                if choice == '1':
                    self.message = input(f"{Fore.YELLOW}[?] Enter custom message: ").strip()
                    break
                elif choice == '2':
                    self.message = "random"
                    break
                elif choice == '3':
                    self.message = "embed"
                    break
                elif choice == '4':
                    self.message = "mention"
                    break
                else:
                    if NEW_UI_AVAILABLE:
                        print_error("Invalid choice. Please enter 1-4.")
                    else:
                        print(f"{Fore.RED}[!] Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                return False

        # Performance settings
        print(f"\n{Fore.CYAN}[*] Performance Settings:")
        self.count = int(input(f"{Fore.YELLOW}[?] Number of messages (default 1000): ").strip() or "1000")
        self.delay = float(input(f"{Fore.YELLOW}[?] Delay between messages in seconds (default 0.01): ").strip() or "0.01")
        
        return True

    def setup_session(self):
        """Setup session with modern UI"""
        if NEW_UI_AVAILABLE:
            spinner = Spinner("Setting up session...")
            spinner.start()
            time.sleep(1)
            spinner.stop()
        else:
            print(f"{Fore.CYAN}[*] Setting up session...")
            time.sleep(1)

        # Configure session
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        if self.proxies:
            proxy = random.choice(self.proxies)
            self.session.proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }

        if NEW_UI_AVAILABLE:
            print_success("Session configured successfully")
        else:
            print(f"{Fore.GREEN}[+] Session configured successfully")

    def test_token(self):
        """Test token with modern UI"""
        if not self.token:
            return True

        if NEW_UI_AVAILABLE:
            spinner = Spinner("Testing token...")
            spinner.start()
        else:
            print(f"{Fore.CYAN}[*] Testing token...")

        try:
            response = self.session.get('https://discord.com/api/v9/users/@me', headers={'Authorization': self.token})
            if response.status_code == 200:
                user_data = response.json()
                if NEW_UI_AVAILABLE:
                    spinner.stop()
                    print_success(f"Token valid! Logged in as: {user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}")
                else:
                    print(f"{Fore.GREEN}[+] Token valid! Logged in as: {user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}")
                return True
            else:
                if NEW_UI_AVAILABLE:
                    spinner.stop()
                    print_error("Invalid token!")
                else:
                    print(f"{Fore.RED}[!] Invalid token!")
                return False
        except Exception as e:
            if NEW_UI_AVAILABLE:
                spinner.stop()
                print_error(f"Error testing token: {str(e)}")
            else:
                print(f"{Fore.RED}[!] Error testing token: {str(e)}")
            return False

    def generate_random_message(self):
        """Generate random message"""
        messages = [
            "Hello World!",
            "Discord is amazing!",
            "Spam spam spam!",
            "Universal Discord Spammer!",
            "QuantumKit is the best!",
            "🚀 Maximum Performance Mode! 🚀",
            "Advanced Security Toolkit",
            "Modern UI Design",
            "Beautiful Interface",
            "Professional Tools"
        ]
        return random.choice(messages)

    def create_embed(self):
        """Create embed message"""
        embed = {
            "embeds": [{
                "title": "Universal Discord Spammer",
                "description": "Advanced spam tool with modern UI",
                "color": 0x00ff00,
                "fields": [
                    {"name": "Version", "value": "7.0", "inline": True},
                    {"name": "Mode", "value": "Maximum Performance", "inline": True},
                    {"name": "Status", "value": "Active", "inline": True}
                ],
                "footer": {"text": "Made with ❤️ by Sqrilizz"}
            }]
        }
        return embed

    def create_mention_message(self):
        """Create mention spam message"""
        return "@everyone @here Universal Discord Spammer is here! 🚀"

    def send_webhook_message(self, payload):
        """Send webhook message with modern UI"""
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            if response.status_code in [200, 204]:
                self.stats['sent'] += 1
                self.stats['total_bytes'] += len(str(payload))
                return True
            else:
                self.stats['failed'] += 1
                return False
        except Exception:
            self.stats['failed'] += 1
            return False

    def send_token_message(self, channel_id, payload):
        """Send token message with modern UI"""
        try:
            headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
            response = self.session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                       json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                self.stats['sent'] += 1
                self.stats['total_bytes'] += len(str(payload))
                return True
            else:
                self.stats['failed'] += 1
                return False
        except Exception:
            self.stats['failed'] += 1
            return False

    def get_user_guilds(self):
        """Get user guilds with modern UI"""
        try:
            headers = {'Authorization': self.token}
            response = self.session.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            if response.status_code == 200:
                self.servers = response.json()
                if NEW_UI_AVAILABLE:
                    print_success(f"Found {len(self.servers)} servers")
                else:
                    print(f"{Fore.GREEN}[+] Found {len(self.servers)} servers")
                return True
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Failed to get servers")
                else:
                    print(f"{Fore.RED}[!] Failed to get servers")
                return False
        except Exception as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Error getting servers: {str(e)}")
            else:
                print(f"{Fore.RED}[!] Error getting servers: {str(e)}")
            return False

    def get_server_channels(self, guild_id):
        """Get server channels with modern UI"""
        try:
            headers = {'Authorization': self.token}
            response = self.session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
            if response.status_code == 200:
                channels = response.json()
                text_channels = [ch for ch in channels if ch['type'] == 0]  # Text channels only
                return text_channels
            else:
                return []
        except Exception:
            return []

    def webhook_spam_thread(self):
        """Webhook spam thread with modern UI"""
        if NEW_UI_AVAILABLE:
            progress = ProgressBar(self.count, title="Webhook Spam Progress")
        else:
            print(f"{Fore.CYAN}[*] Starting webhook spam...")

        def send_batch(batch_data):
            for payload in batch_data:
                if not self.is_spamming:
                    break
                
                success = self.send_webhook_message(payload)
                if success and NEW_UI_AVAILABLE:
                    progress.update(self.stats['sent'])
                
                time.sleep(self.delay)

        # Prepare payloads
        payloads = []
        for i in range(self.count):
            if self.message == "random":
                payload = {"content": self.generate_random_message()}
            elif self.message == "embed":
                payload = self.create_embed()
            elif self.message == "mention":
                payload = {"content": self.create_mention_message()}
            else:
                payload = {"content": self.message}
            
            payloads.append(payload)

        # Send in batches
        batch_size = min(self.batch_size, len(payloads))
        for i in range(0, len(payloads), batch_size):
            if not self.is_spamming:
                break
            batch = payloads[i:i + batch_size]
            send_batch(batch)

        if NEW_UI_AVAILABLE:
            progress.finish()

    def token_single_spam_thread(self):
        """Token single spam thread with modern UI"""
        if NEW_UI_AVAILABLE:
            progress = ProgressBar(self.count, title="Token Single Spam Progress")
        else:
            print(f"{Fore.CYAN}[*] Starting token single spam...")

        def send_message_batch(batch_data):
            for payload in batch_data:
                if not self.is_spamming:
                    break
                
                success = self.send_token_message(self.channel_id, payload)
                if success and NEW_UI_AVAILABLE:
                    progress.update(self.stats['sent'])
                
                time.sleep(self.delay)

        # Prepare payloads
        payloads = []
        for i in range(self.count):
            if self.message == "random":
                payload = {"content": self.generate_random_message()}
            elif self.message == "embed":
                payload = self.create_embed()
            elif self.message == "mention":
                payload = {"content": self.create_mention_message()}
            else:
                payload = {"content": self.message}
            
            payloads.append(payload)

        # Send in batches
        batch_size = min(self.batch_size, len(payloads))
        for i in range(0, len(payloads), batch_size):
            if not self.is_spamming:
                break
            batch = payloads[i:i + batch_size]
            send_message_batch(batch)

        if NEW_UI_AVAILABLE:
            progress.finish()

    def token_mass_spam_thread(self):
        """Token mass spam thread with modern UI"""
        if NEW_UI_AVAILABLE:
            progress = ProgressBar(self.count, title="Token Mass Spam Progress")
        else:
            print(f"{Fore.CYAN}[*] Starting token mass spam...")

        def process_server(server):
            if not self.is_spamming:
                return
            
            guild_id = server['id']
            channels = self.get_server_channels(guild_id)
            
            def send_to_channel(channel):
                if not self.is_spamming:
                    return
                
                channel_id = channel['id']
                for i in range(min(10, self.count // len(channels))):  # Limit per channel
                    if not self.is_spamming:
                        break
                    
                    if self.message == "random":
                        payload = {"content": self.generate_random_message()}
                    elif self.message == "embed":
                        payload = self.create_embed()
                    elif self.message == "mention":
                        payload = {"content": self.create_mention_message()}
                    else:
                        payload = {"content": self.message}
                    
                    success = self.send_token_message(channel_id, payload)
                    if success and NEW_UI_AVAILABLE:
                        progress.update(self.stats['sent'])
                    
                    time.sleep(self.delay)
            
            # Process channels in parallel
            with ThreadPoolExecutor(max_workers=min(10, len(channels))) as executor:
                executor.map(send_to_channel, channels)
            
            self.stats['servers_processed'] += 1

        # Process servers in parallel
        with ThreadPoolExecutor(max_workers=min(5, len(self.servers))) as executor:
            executor.map(process_server, self.servers)

        if NEW_UI_AVAILABLE:
            progress.finish()

    def print_stats(self):
        """Print stats with modern UI"""
        if NEW_UI_AVAILABLE:
            print_separator()
            print_header("Spam Statistics")
        else:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}[*] Spam Statistics")
            print(f"{Fore.CYAN}{'='*60}")

        elapsed_time = time.time() - self.stats['start_time']
        
        stats_data = [
            ("Messages Sent", str(self.stats['sent'])),
            ("Messages Failed", str(self.stats['failed'])),
            ("Servers Processed", str(self.stats['servers_processed'])),
            ("Elapsed Time", f"{elapsed_time:.2f}s"),
            ("Messages/Second", f"{self.stats['sent']/elapsed_time:.2f}" if elapsed_time > 0 else "0"),
            ("Total Data", f"{self.stats['total_bytes']/1024:.2f} KB")
        ]

        if NEW_UI_AVAILABLE:
            from src.utils.ui import create_table
            headers = ["Metric", "Value"]
            rows = stats_data
            table = create_table(headers, rows, "Performance Metrics")
            print(table)
        else:
            for metric, value in stats_data:
                print(f"{Fore.WHITE}    {metric}: {Fore.CYAN}{value}")

    def start_spam(self):
        """Start spam with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Starting Spam Operation")
        else:
            print(f"\n{Fore.CYAN}[*] Starting spam operation...")

        self.is_spamming = True
        self.stats['start_time'] = time.time()

        try:
            if self.spam_type == "webhook":
                self.webhook_spam_thread()
            elif self.spam_type == "token_single":
                self.token_single_spam_thread()
            elif self.spam_type == "token_mass":
                if not self.get_user_guilds():
                    return
                self.token_mass_spam_thread()
        except KeyboardInterrupt:
            if NEW_UI_AVAILABLE:
                print_warning("Spam operation interrupted by user")
            else:
                print(f"\n{Fore.YELLOW}[!] Spam operation interrupted by user")
        finally:
            self.is_spamming = False

    def print_final_stats(self):
        """Print final stats with modern UI"""
        if NEW_UI_AVAILABLE:
            print_separator()
            print_header("Final Results")
        else:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}[*] Final Results")
            print(f"{Fore.CYAN}{'='*60}")

        self.print_stats()

        if NEW_UI_AVAILABLE:
            if self.stats['sent'] > 0:
                print_success("Spam operation completed successfully!")
            else:
                print_error("Spam operation failed!")
        else:
            if self.stats['sent'] > 0:
                print(f"{Fore.GREEN}[+] Spam operation completed successfully!")
            else:
                print(f"{Fore.RED}[!] Spam operation failed!")

    def run(self):
        """Main run method with modern UI"""
        try:
            self.print_banner()
            
            if not self.get_user_input():
                return
            
            self.setup_session()
            
            if self.spam_type != "webhook" and not self.test_token():
                return
            
            if NEW_UI_AVAILABLE:
                if confirm_action("Start spam operation?"):
                    self.start_spam()
                    self.print_final_stats()
            else:
                start = input(f"\n{Fore.YELLOW}[?] Start spam operation? (y/N): ").strip().lower()
                if start in ['y', 'yes']:
                    self.start_spam()
                    self.print_final_stats()
            
        except KeyboardInterrupt:
            if NEW_UI_AVAILABLE:
                print_warning("Operation cancelled by user")
            else:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled by user")
        except Exception as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Unexpected error: {str(e)}")
            else:
                print(f"{Fore.RED}[!] Unexpected error: {str(e)}")

def main():
    """Main function"""
    spammer = UniversalDiscordSpammer()
    spammer.run()

if __name__ == "__main__":
    main() 