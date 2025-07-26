import requests
import time
from .assetsManager import *
from .color import color
from .tokenManager import add_token

def no_proxy_message_spam(token: str, channel_id: str, message: str, userAgent: str) -> bool:
    """Отправка сообщения без прокси"""
    headers = {
        "content-type": "application/json",
        "authorization": token,
        "User-Agent": userAgent
    }
    data = {
        "content": message,
        "tts": False
    }
    
    try:
        response = requests.post(
            f"https://discordapp.com/api/v7/channels/{channel_id}/messages",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"{color.GREEN}[+] Message sent successfully{color.RESET_ALL}")
            return True
        else:
            print(f"{color.RED}[-] Failed to send: {response.status_code}{color.RESET_ALL}")
            return False
            
    except Exception as err:
        print(f"{color.RED}[-] ERROR: {err}{color.RESET_ALL}")
        return False

def multi_token_no_proxy_spam(tokens: list, channel_id: str, message: str, userAgents: list) -> dict:
    """Спам от всех токенов без прокси"""
    success_count = 0
    failed_count = 0
    
    print(f"{color.CYAN}[*] Starting no-proxy spam with {len(tokens)} tokens{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'add' to add new token during spam{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'skip' to skip current token{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'quit' to stop spam{color.RESET_ALL}")
    
    for i, token in enumerate(tokens, 1):
        print(f"\n{color.BLUE}[Token {i}/{len(tokens)}]{color.RESET_ALL}")
        
        # Выбираем случайный userAgent для каждого токена
        userAgent = userAgents[i % len(userAgents)] if userAgents else ""
        
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
        
        # Отправляем сообщение с текущим токеном
        if no_proxy_message_spam(token, channel_id, message, userAgent):
            success_count += 1
        else:
            failed_count += 1
        
        # Небольшая задержка между сообщениями
        time.sleep(0.5)
    
    return {
        "success": success_count,
        "failed": failed_count,
        "total": len(tokens)
    }

def mass_no_proxy_spam(tokens: list, message: str, userAgents: list) -> dict:
    """Массовый спам без прокси в популярные каналы"""
    success_count = 0
    failed_count = 0
    
    # Список популярных каналов для спама
    popular_channels = [
        "1234567890123456789",  # Замените на реальные ID каналов
        "9876543210987654321",
        "1111111111111111111",
        "2222222222222222222",
        "3333333333333333333"
    ]
    
    print(f"{color.CYAN}[*] Starting mass no-proxy spam with {len(tokens)} tokens{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'add' to add new token during spam{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'skip' to skip current token{color.RESET_ALL}")
    print(f"{color.YELLOW}[*] Type 'quit' to stop spam{color.RESET_ALL}")
    
    for i, token in enumerate(tokens, 1):
        print(f"\n{color.BLUE}[Token {i}/{len(tokens)}]{color.RESET_ALL}")
        
        # Выбираем случайный userAgent для каждого токена
        userAgent = userAgents[i % len(userAgents)] if userAgents else ""
        
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
        
        # Отправляем сообщение в случайные каналы
        for j, channel_id in enumerate(popular_channels):
            print(f"{color.YELLOW}[*] Sending to channel {j+1}/{len(popular_channels)}{color.RESET_ALL}")
            
            if no_proxy_message_spam(token, channel_id, message, userAgent):
                success_count += 1
            else:
                failed_count += 1
            
            time.sleep(0.5)
    
    return {
        "success": success_count,
        "failed": failed_count,
        "total_channels": len(popular_channels) * len(tokens)
    } 