import os
from .color import color

def add_token(token: str) -> bool:
    """Добавляет новый токен в файл tokens.txt"""
    try:
        # Проверяем, что токен не пустой
        if not token.strip():
            print(f"{color.RED}[-] Token cannot be empty{color.RESET_ALL}")
            return False
        
        # Проверяем, что токен еще не существует
        existing_tokens = get_all_tokens()
        if token.strip() in existing_tokens:
            print(f"{color.YELLOW}[!] Token already exists{color.RESET_ALL}")
            return False
        
        # Добавляем токен в файл
        with open("./assets/tokens.txt", "a", encoding="utf-8") as f:
            f.write(f"{token.strip()}\n")
        
        print(f"{color.GREEN}[+] Token added successfully{color.RESET_ALL}")
        return True
        
    except Exception as err:
        print(f"{color.RED}[-] Error adding token: {err}{color.RESET_ALL}")
        return False

def remove_token(token: str) -> bool:
    """Удаляет токен из файла tokens.txt"""
    try:
        # Читаем все токены
        tokens = get_all_tokens()
        
        if token.strip() not in tokens:
            print(f"{color.RED}[-] Token not found{color.RESET_ALL}")
            return False
        
        # Удаляем токен
        tokens.remove(token.strip())
        
        # Перезаписываем файл
        with open("./assets/tokens.txt", "w", encoding="utf-8") as f:
            for t in tokens:
                f.write(f"{t}\n")
        
        print(f"{color.GREEN}[+] Token removed successfully{color.RESET_ALL}")
        return True
        
    except Exception as err:
        print(f"{color.RED}[-] Error removing token: {err}{color.RESET_ALL}")
        return False

def get_all_tokens() -> list:
    """Получает список всех токенов"""
    try:
        if not os.path.exists("./assets/tokens.txt"):
            return []
        
        with open("./assets/tokens.txt", "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f.readlines() if line.strip()]
        return tokens
        
    except Exception as err:
        print(f"{color.RED}[-] Error reading tokens: {err}{color.RESET_ALL}")
        return []

def show_tokens() -> None:
    """Показывает все токены"""
    tokens = get_all_tokens()
    
    if not tokens:
        print(f"{color.YELLOW}[!] No tokens found{color.RESET_ALL}")
        return
    
    print(f"{color.CYAN}[*] Found {len(tokens)} tokens:{color.RESET_ALL}")
    print("-" * 50)
    
    for i, token in enumerate(tokens, 1):
        # Показываем только первые и последние символы токена для безопасности
        masked_token = token[:10] + "..." + token[-10:] if len(token) > 20 else token
        print(f"{color.YELLOW}{i:2d}.{color.RESET_ALL} {masked_token}")
    
    print("-" * 50)

def clear_all_tokens() -> bool:
    """Очищает все токены"""
    try:
        with open("./assets/tokens.txt", "w", encoding="utf-8") as f:
            f.write("")
        print(f"{color.GREEN}[+] All tokens cleared{color.RESET_ALL}")
        return True
        
    except Exception as err:
        print(f"{color.RED}[-] Error clearing tokens: {err}{color.RESET_ALL}")
        return False

def validate_token(token: str) -> bool:
    """Проверяет валидность токена (базовая проверка)"""
    # Базовая проверка формата токена Discord
    if not token or len(token) < 50:
        return False
    
    # Проверяем, что токен содержит только допустимые символы
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
    return all(c in valid_chars for c in token) 