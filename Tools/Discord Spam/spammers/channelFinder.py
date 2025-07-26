import requests
from .assetsManager import *
from .color import color

def get_user_guilds(token: str, userAgent: str, proxies: str) -> list:
    """Получает список всех серверов пользователя"""
    headers = {
        "authorization": token,
        "User-Agent": userAgent
    }
    proxy_dict = {"http": proxies, "https": proxies}
    
    try:
        response = requests.get(
            "https://discordapp.com/api/v7/users/@me/guilds",
            headers=headers,
            proxies=proxy_dict
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{color.RED}[-] Failed to get guilds: {response.status_code}{color.RESET_ALL}")
            return []
    except Exception as err:
        print(f"{color.RED}[-] ERROR getting guilds: {err}{color.RESET_ALL}")
        return []

def get_guild_channels(token: str, guild_id: str, userAgent: str, proxies: str) -> list:
    """Получает список всех каналов в сервере"""
    headers = {
        "authorization": token,
        "User-Agent": userAgent
    }
    proxy_dict = {"http": proxies, "https": proxies}
    
    try:
        response = requests.get(
            f"https://discordapp.com/api/v7/guilds/{guild_id}/channels",
            headers=headers,
            proxies=proxy_dict
        )
        if response.status_code == 200:
            channels = response.json()
            # Фильтруем только текстовые каналы
            text_channels = [ch for ch in channels if ch.get('type') == 0]
            return text_channels
        else:
            print(f"{color.RED}[-] Failed to get channels for guild {guild_id}: {response.status_code}{color.RESET_ALL}")
            return []
    except Exception as err:
        print(f"{color.RED}[-] ERROR getting channels: {err}{color.RESET_ALL}")
        return []

def get_all_available_channels(token: str, userAgent: str, proxies: str) -> list:
    """Получает все доступные каналы со всех серверов"""
    all_channels = []
    
    # Получаем все серверы пользователя
    guilds = get_user_guilds(token, userAgent, proxies)
    
    if not guilds:
        return []
    
    print(f"{color.CYAN}[+] Found {len(guilds)} guilds for token{color.RESET_ALL}")
    
    # Для каждого сервера получаем каналы
    for guild in guilds:
        guild_id = guild.get('id')
        guild_name = guild.get('name', 'Unknown')
        
        channels = get_guild_channels(token, guild_id, userAgent, proxies)
        
        for channel in channels:
            channel['guild_name'] = guild_name
            channel['guild_id'] = guild_id
            all_channels.append(channel)
    
    print(f"{color.GREEN}[+] Total available channels: {len(all_channels)}{color.RESET_ALL}")
    return all_channels 