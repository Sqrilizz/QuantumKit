import requests
import time
from .assetsManager import *
from .color import color
from .channelFinder import get_all_available_channels
from .tokenManager import add_token, get_all_tokens

def send_message_to_channel(token: str, channel_id: str, message: str, userAgent: str, proxies: str, channel_name: str = "Unknown") -> bool:
    """Отправляет сообщение в конкретный канал"""
    headers = {
        "content-type": "application/json",
        "authorization": token,
        "User-Agent": userAgent
    }
    data = {
        "content": message,
        "tts": False
    }
    proxy_dict = {"http": proxies, "https": proxies}
    
    try:
        response = requests.post(
            f"https://discordapp.com/api/v7/channels/{channel_id}/messages",
            headers=headers,
            json=data,
            proxies=proxy_dict
        )
        
        if response.status_code == 200:
            print(f"{color.GREEN}[+] Message sent to #{channel_name} successfully{color.RESET_ALL}")
            return True
        else:
            print(f"{color.RED}[-] Failed to send to #{channel_name}: {response.status_code}{color.RESET_ALL}")
            return False
            
    except Exception as err:
        print(f"{color.RED}[-] ERROR sending to #{channel_name}: {err}{color.RESET_ALL}")
        return False

def mass_message_spam(token: str, message: str, userAgent: str, proxies: str) -> dict:
    """Отправляет сообщение во все доступные каналы"""
    print(f"{color.YELLOW}[*] Getting all available channels for token...{color.RESET_ALL}")
    
    # Получаем все доступные каналы
    channels = get_all_available_channels(token, userAgent, proxies)
    
    if not channels:
        print(f"{color.RED}[-] No channels found for this token{color.RESET_ALL}")
        return {"success": 0, "failed": 0, "total": 0}
    
    success_count = 0
    failed_count = 0
    
    print(f"{color.CYAN}[*] Starting mass message spam to {len(channels)} channels...{color.RESET_ALL}")
    
    for i, channel in enumerate(channels, 1):
        channel_id = channel.get('id')
        channel_name = channel.get('name', 'Unknown')
        guild_name = channel.get('guild_name', 'Unknown')
        
        print(f"{color.YELLOW}[{i}/{len(channels)}] Sending to #{channel_name} in {guild_name}{color.RESET_ALL}")
        
        if send_message_to_channel(token, channel_id, message, userAgent, proxies, channel_name):
            success_count += 1
        else:
            failed_count += 1
        
        # Небольшая задержка между сообщениями чтобы избежать rate limit
        time.sleep(0.5)
    
    return {
        "success": success_count,
        "failed": failed_count,
        "total": len(channels)
    }

def multi_token_mass_spam(tokens: list, message: str, userAgents: list, proxies_list: list) -> dict:
    """Отправляет сообщения от всех токенов во все доступные каналы с возможностью добавления токенов"""
    total_success = 0
    total_failed = 0
    total_channels = 0
    
    print(f"{color.CYAN}[*] Starting multi-token mass spam with {len(tokens)} tokens{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'add' to add new token during spam{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'skip' to skip current token{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'quit' to stop spam{color.RESET_ALL}")
    
    for i, token in enumerate(tokens, 1):
        print(f"\n{color.BLUE}[Token {i}/{len(tokens)}]{color.RESET_ALL}")
        
        # Выбираем случайные userAgent и proxy для каждого токена
        userAgent = userAgents[i % len(userAgents)] if userAgents else ""
        proxy = proxies_list[i % len(proxies_list)] if proxies_list else ""
        
        # Проверяем команды пользователя
        user_input = input(f"{color.CYAN}[?] Press Enter to continue, 'add' to add token, 'skip' to skip, 'quit' to stop > {color.RESET_ALL}").lower().strip()
        
        if user_input == "quit":
            print(f"{color.YELLOW}[*] Spam stopped by user{color.RESET_ALL}")
            break
        elif user_input == "skip":
            print(f"{color.YELLOW}[*] Skipping token {i}{color.RESET_ALL}")
            continue
        elif user_input == "add":
            new_token = input(f"{color.YELLOW}[?] Enter new Discord token > {color.RESET_ALL}")
            if new_token.strip():
                if add_token(new_token.strip()):
                    # Добавляем новый токен в текущий список
                    tokens.append(new_token.strip())
                    print(f"{color.GREEN}[+] Token added and will be used{color.RESET_ALL}")
                else:
                    print(f"{color.RED}[-] Failed to add token{color.RESET_ALL}")
            else:
                print(f"{color.RED}[-] Token cannot be empty{color.RESET_ALL}")
        
        # Выполняем спам с текущим токеном
        result = mass_message_spam(token, message, userAgent, proxy)
        
        total_success += result["success"]
        total_failed += result["failed"]
        total_channels += result["total"]
    
    return {
        "success": total_success,
        "failed": total_failed,
        "total_channels": total_channels
    } 