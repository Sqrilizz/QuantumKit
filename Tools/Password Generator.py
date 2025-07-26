import random
import string
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.count = 10
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True
        self.exclude_similar = False
        self.exclude_ambiguous = False

    def print_banner(self):
        """Выводит баннер"""
        banner = f"""
{Fore.MAGENTA}   ██████╗  █████╗ ███████╗███████╗██╗  ██╗██╗   ██╗██████╗  ██████╗ ███████╗██████╗ 
{Fore.MAGENTA}   ██╔══██╗██╔══██╗██╔════╝██╔════╝██║  ██║██║   ██║██╔══██╗██╔═══██╗██╔════╝██╔══██╗
{Fore.MAGENTA}   ██████╔╝███████║███████╗███████╗███████║██║   ██║██║  ██║██║   ██║█████╗  ██████╔╝
{Fore.MAGENTA}   ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══██║██║   ██║██║  ██║██║   ██║██╔══╝  ██╔══██╗
{Fore.MAGENTA}   ██║     ██║  ██║███████║███████║██║  ██║╚██████╔╝██████╔╝╚██████╔╝███████╗██║  ██║
{Fore.MAGENTA}   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
{Fore.MAGENTA}                                                                                            
{Fore.MAGENTA}                              GENERATOR
{Fore.MAGENTA}                              by Sqrilizz
"""
        print(banner)

    def get_user_input(self):
        """Получает настройки от пользователя"""
        print(f"{Fore.CYAN}[*] Password Generator Configuration")
        print(f"{Fore.CYAN}[*] ================================")
        
        # Длина пароля
        while True:
            try:
                length_input = input(f"{Fore.YELLOW}[?] Enter password length (default 12): ").strip()
                if length_input:
                    self.length = int(length_input)
                    if 4 <= self.length <= 100:
                        break
                    else:
                        print(f"{Fore.RED}[!] Length must be between 4 and 100!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid length!")
        
        # Количество паролей
        while True:
            try:
                count_input = input(f"{Fore.YELLOW}[?] Enter number of passwords to generate (default 10): ").strip()
                if count_input:
                    self.count = int(count_input)
                    if 1 <= self.count <= 1000:
                        break
                    else:
                        print(f"{Fore.RED}[!] Count must be between 1 and 1000!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid count!")
        
        # Настройки символов
        print(f"\n{Fore.CYAN}[*] Character Settings:")
        
        # Верхний регистр
        uppercase_input = input(f"{Fore.YELLOW}[?] Include uppercase letters (A-Z)? (y/n, default y): ").strip().lower()
        self.include_uppercase = uppercase_input != 'n'
        
        # Нижний регистр
        lowercase_input = input(f"{Fore.YELLOW}[?] Include lowercase letters (a-z)? (y/n, default y): ").strip().lower()
        self.include_lowercase = lowercase_input != 'n'
        
        # Цифры
        numbers_input = input(f"{Fore.YELLOW}[?] Include numbers (0-9)? (y/n, default y): ").strip().lower()
        self.include_numbers = numbers_input != 'n'
        
        # Символы
        symbols_input = input(f"{Fore.YELLOW}[?] Include symbols (!@#$%^&*)? (y/n, default y): ").strip().lower()
        self.include_symbols = symbols_input != 'n'
        
        # Исключить похожие символы
        similar_input = input(f"{Fore.YELLOW}[?] Exclude similar characters (l, 1, I, O, 0)? (y/n, default n): ").strip().lower()
        self.exclude_similar = similar_input == 'y'
        
        # Исключить неоднозначные символы
        ambiguous_input = input(f"{Fore.YELLOW}[?] Exclude ambiguous characters ({'{}[]()/\\\'"`~,;:.<>'}? (y/n, default n): ").strip().lower()
        self.exclude_ambiguous = ambiguous_input == 'y'
        
        return True

    def generate_password(self):
        """Генерирует один пароль"""
        # Определяем доступные символы
        chars = ""
        
        if self.include_uppercase:
            chars += string.ascii_uppercase
        if self.include_lowercase:
            chars += string.ascii_lowercase
        if self.include_numbers:
            chars += string.digits
        if self.include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Исключаем похожие символы
        if self.exclude_similar:
            chars = chars.replace('l', '').replace('1', '').replace('I', '').replace('O', '').replace('0', '')
        
        # Исключаем неоднозначные символы
        if self.exclude_ambiguous:
            chars = chars.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '')
            chars = chars.replace('/', '').replace('\\', '').replace("'", '').replace('"', '').replace('`', '').replace('~', '')
            chars = chars.replace(',', '').replace(';', '').replace(':', '').replace('.', '').replace('<', '').replace('>', '')
        
        # Проверяем, что есть символы для генерации
        if not chars:
            return "ERROR: No characters available for generation"
        
        # Генерируем пароль
        password = ''.join(random.choice(chars) for _ in range(self.length))
        return password

    def generate_passwords(self):
        """Генерирует пароли"""
        print(f"\n{Fore.CYAN}[*] Generating {self.count} passwords...")
        print(f"{Fore.CYAN}[*] Length: {self.length}")
        print(f"{Fore.CYAN}[*] Settings: Uppercase={self.include_uppercase}, Lowercase={self.include_lowercase}, Numbers={self.include_numbers}, Symbols={self.include_symbols}")
        print(f"{Fore.CYAN}[*] Exclude similar: {self.exclude_similar}, Exclude ambiguous: {self.exclude_ambiguous}")
        print(f"{Fore.CYAN}[*] ================================\n")
        
        passwords = []
        start_time = time.time()
        
        for i in range(self.count):
            password = self.generate_password()
            passwords.append(password)
            
            # Выводим с цветовой индикацией
            if len(password) == self.length:
                print(f"{Fore.GREEN}[{i+1:3d}] {password}")
            else:
                print(f"{Fore.RED}[{i+1:3d}] {password}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{Fore.CYAN}[*] Generation completed in {duration:.2f} seconds")
        return passwords

    def analyze_password(self, password):
        """Анализирует безопасность пароля"""
        score = 0
        feedback = []
        
        # Длина
        if len(password) >= 12:
            score += 2
            feedback.append("Good length")
        elif len(password) >= 8:
            score += 1
            feedback.append("Acceptable length")
        else:
            feedback.append("Too short")
        
        # Разнообразие символов
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        # Оценка
        if score >= 5:
            strength = "Very Strong"
            color = Fore.GREEN
        elif score >= 4:
            strength = "Strong"
            color = Fore.GREEN
        elif score >= 3:
            strength = "Good"
            color = Fore.YELLOW
        elif score >= 2:
            strength = "Weak"
            color = Fore.RED
        else:
            strength = "Very Weak"
            color = Fore.RED
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'has_upper': has_upper,
            'has_lower': has_lower,
            'has_digit': has_digit,
            'has_symbol': has_symbol
        }

    def save_passwords(self, passwords):
        """Сохраняет пароли в файл"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"output/passwords_{timestamp}.txt"
        
        try:
            os.makedirs("output", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Password Generator Results\n")
                f.write(f"========================\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Count: {len(passwords)}\n")
                f.write(f"Length: {self.length}\n")
                f.write(f"Settings: Uppercase={self.include_uppercase}, Lowercase={self.include_lowercase}, Numbers={self.include_numbers}, Symbols={self.include_symbols}\n")
                f.write(f"Exclude similar: {self.exclude_similar}, Exclude ambiguous: {self.exclude_ambiguous}\n")
                f.write(f"\nPasswords:\n")
                f.write(f"=========\n")
                
                for i, password in enumerate(passwords, 1):
                    analysis = self.analyze_password(password)
                    f.write(f"{i:3d}. {password} | Strength: {analysis['strength']} (Score: {analysis['score']}/6)\n")
            
            print(f"{Fore.GREEN}[+] Passwords saved to: {filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to save passwords: {e}")

    def run(self):
        """Запускает генератор паролей"""
        self.print_banner()
        
        if not self.get_user_input():
            return
        
        passwords = self.generate_passwords()
        
        # Анализируем первый пароль как пример
        if passwords:
            print(f"\n{Fore.CYAN}[*] Password Analysis Example:")
            analysis = self.analyze_password(passwords[0])
            print(f"{Fore.CYAN}[*] First password: {passwords[0]}")
            print(f"{analysis['color']}[*] Strength: {analysis['strength']} (Score: {analysis['score']}/6)")
            print(f"{Fore.CYAN}[*] Feedback: {', '.join(analysis['feedback'])}")
            print(f"{Fore.CYAN}[*] Contains: Uppercase={analysis['has_upper']}, Lowercase={analysis['has_lower']}, Numbers={analysis['has_digit']}, Symbols={analysis['has_symbol']}")
        
        self.save_passwords(passwords)

def main():
    """Главная функция"""
    try:
        generator = PasswordGenerator()
        generator.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting...")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {e}")

if __name__ == "__main__":
    main() 