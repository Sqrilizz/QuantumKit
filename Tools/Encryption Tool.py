#!/usr/bin/env python3
"""
Advanced Encryption Tool
Part of QuantumKit v6.0
"""
import os
import sys
import time
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init

init(autoreset=True)

class EncryptionTool:
    def __init__(self):
        self.operation = "encrypt"
        self.input_text = ""
        self.input_file = ""
        self.output_file = ""
        self.password = ""
        self.key = None
        self.algorithm = "fernet"
        self.hash_algorithm = "sha256"
        self.output_dir = "output"

    def print_banner(self):
        """Выводит баннер"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Fore.MAGENTA}   ██████╗  █████╗ ███████╗███████╗██╗  ██╗██╗   ██╗██████╗  ██████╗ ███████╗██████╗ 
{Fore.MAGENTA}   ██╔══██╗██╔══██╗██╔════╝██╔════╝██║  ██║██║   ██║██╔══██╗██╔═══██╗██╔════╝██╔══██╗
{Fore.MAGENTA}   ██████╔╝███████║███████╗███████╗███████║██║   ██║██║  ██║██║   ██║█████╗  ██████╔╝
{Fore.MAGENTA}   ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══██║██║   ██║██║  ██║██║   ██║██╔══╝  ██╔══██╗
{Fore.MAGENTA}   ██║     ██║  ██║███████║███████║██║  ██║╚██████╔╝██████╔╝╚██████╔╝███████╗██║  ██║
{Fore.MAGENTA}   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
{Fore.MAGENTA}                                                                                            
{Fore.MAGENTA}                              ENCRYPTION TOOL
{Fore.MAGENTA}                              by Sqrilizz
"""
        print(banner)
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          ADVANCED ENCRYPTION TOOL                            ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Получает настройки от пользователя"""
        print(f"{Fore.CYAN}[*] Encryption Tool Configuration")
        print(f"{Fore.CYAN}[*] ==============================")
        
        # Выбор операции
        print(f"\n{Fore.YELLOW}[*] Select Operation:")
        print(f"{Fore.WHITE}    1. Encrypt Text")
        print(f"{Fore.WHITE}    2. Decrypt Text")
        print(f"{Fore.WHITE}    3. Encrypt File")
        print(f"{Fore.WHITE}    4. Decrypt File")
        print(f"{Fore.WHITE}    5. Generate Key")
        print(f"{Fore.WHITE}    6. Hash Text")
        print(f"{Fore.WHITE}    7. Hash File")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    self.operation = {
                        '1': 'encrypt_text',
                        '2': 'decrypt_text',
                        '3': 'encrypt_file',
                        '4': 'decrypt_file',
                        '5': 'generate_key',
                        '6': 'hash_text',
                        '7': 'hash_file'
                    }[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-7.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Получение данных в зависимости от операции
        if self.operation in ['encrypt_text', 'decrypt_text', 'hash_text']:
            self.get_text_input()
        elif self.operation in ['encrypt_file', 'decrypt_file', 'hash_file']:
            self.get_file_input()
        elif self.operation == 'generate_key':
            self.get_key_settings()

        # Получение пароля/ключа
        if self.operation not in ['generate_key', 'hash_text', 'hash_file']:
            self.get_password_input()

        # Настройки алгоритма
        if self.operation in ['hash_text', 'hash_file']:
            self.get_hash_settings()

        return True

    def get_text_input(self):
        """Получает текстовый ввод"""
        print(f"\n{Fore.CYAN}[*] Text Input:")
        
        if self.operation == 'encrypt_text':
            while True:
                text = input(f"{Fore.YELLOW}[?] Enter text to encrypt: ").strip()
                if text:
                    self.input_text = text
                    break
                else:
                    print(f"{Fore.RED}[!] Text cannot be empty!")
        elif self.operation == 'decrypt_text':
            while True:
                text = input(f"{Fore.YELLOW}[?] Enter text to decrypt: ").strip()
                if text:
                    self.input_text = text
                    break
                else:
                    print(f"{Fore.RED}[!] Text cannot be empty!")
        elif self.operation == 'hash_text':
            while True:
                text = input(f"{Fore.YELLOW}[?] Enter text to hash: ").strip()
                if text:
                    self.input_text = text
                    break
                else:
                    print(f"{Fore.RED}[!] Text cannot be empty!")

    def get_file_input(self):
        """Получает файловый ввод"""
        print(f"\n{Fore.CYAN}[*] File Input:")
        
        while True:
            file_path = input(f"{Fore.YELLOW}[?] Enter file path: ").strip()
            if file_path and os.path.exists(file_path):
                self.input_file = file_path
                break
            else:
                print(f"{Fore.RED}[!] File not found!")

    def get_password_input(self):
        """Получает пароль"""
        print(f"\n{Fore.CYAN}[*] Password/Key Settings:")
        
        while True:
            password = input(f"{Fore.YELLOW}[?] Enter password: ").strip()
            if password:
                self.password = password
                break
            else:
                print(f"{Fore.RED}[!] Password cannot be empty!")

    def get_key_settings(self):
        """Получает настройки для генерации ключа"""
        print(f"\n{Fore.CYAN}[*] Key Generation Settings:")
        
        # Размер ключа
        while True:
            try:
                key_size_input = input(f"{Fore.YELLOW}[?] Enter key size in bytes (16-64, default 32): ").strip()
                if key_size_input:
                    key_size = int(key_size_input)
                    if 16 <= key_size <= 64:
                        self.key_size = key_size
                        break
                    else:
                        print(f"{Fore.RED}[!] Key size must be between 16 and 64!")
                else:
                    self.key_size = 32
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid key size!")

    def get_hash_settings(self):
        """Получает настройки хеширования"""
        print(f"\n{Fore.CYAN}[*] Hash Algorithm Settings:")
        
        print(f"{Fore.YELLOW}[*] Available algorithms:")
        print(f"{Fore.WHITE}    1. MD5")
        print(f"{Fore.WHITE}    2. SHA1")
        print(f"{Fore.WHITE}    3. SHA256")
        print(f"{Fore.WHITE}    4. SHA512")
        print(f"{Fore.WHITE}    5. BLAKE2b")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-5, default 3): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    self.hash_algorithm = {
                        '1': 'md5',
                        '2': 'sha1',
                        '3': 'sha256',
                        '4': 'sha512',
                        '5': 'blake2b'
                    }[choice]
                    break
                else:
                    self.hash_algorithm = 'sha256'
                    break
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

    def generate_key_from_password(self, password, salt=None):
        """Генерирует ключ из пароля"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_text(self):
        """Шифрует текст"""
        try:
            key, salt = self.generate_key_from_password(self.password)
            fernet = Fernet(key)
            
            encrypted_data = fernet.encrypt(self.input_text.encode())
            result = base64.b64encode(salt + encrypted_data).decode()
            
            return result
        except Exception as e:
            print(f"{Fore.RED}[!] Encryption error: {e}")
            return None

    def decrypt_text(self):
        """Расшифровывает текст"""
        try:
            # Декодируем из base64
            data = base64.b64decode(self.input_text.encode())
            
            # Извлекаем salt и зашифрованные данные
            salt = data[:16]
            encrypted_data = data[16:]
            
            key, _ = self.generate_key_from_password(self.password, salt)
            fernet = Fernet(key)
            
            decrypted_data = fernet.decrypt(encrypted_data)
            result = decrypted_data.decode()
            
            return result
        except Exception as e:
            print(f"{Fore.RED}[!] Decryption error: {e}")
            return None

    def encrypt_file(self):
        """Шифрует файл"""
        try:
            with open(self.input_file, 'rb') as f:
                file_data = f.read()
            
            key, salt = self.generate_key_from_password(self.password)
            fernet = Fernet(key)
            
            encrypted_data = fernet.encrypt(file_data)
            result = salt + encrypted_data
            
            # Сохраняем результат
            output_path = self.save_result(result, "encrypted")
            return output_path
        except Exception as e:
            print(f"{Fore.RED}[!] File encryption error: {e}")
            return None

    def decrypt_file(self):
        """Расшифровывает файл"""
        try:
            with open(self.input_file, 'rb') as f:
                data = f.read()
            
            # Извлекаем salt и зашифрованные данные
            salt = data[:16]
            encrypted_data = data[16:]
            
            key, _ = self.generate_key_from_password(self.password, salt)
            fernet = Fernet(key)
            
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Сохраняем результат
            output_path = self.save_result(decrypted_data, "decrypted")
            return output_path
        except Exception as e:
            print(f"{Fore.RED}[!] File decryption error: {e}")
            return None

    def generate_key(self):
        """Генерирует новый ключ"""
        try:
            key = Fernet.generate_key()
            return key.decode()
        except Exception as e:
            print(f"{Fore.RED}[!] Key generation error: {e}")
            return None

    def hash_text(self):
        """Хеширует текст"""
        try:
            if self.hash_algorithm == 'md5':
                hash_obj = hashlib.md5()
            elif self.hash_algorithm == 'sha1':
                hash_obj = hashlib.sha1()
            elif self.hash_algorithm == 'sha256':
                hash_obj = hashlib.sha256()
            elif self.hash_algorithm == 'sha512':
                hash_obj = hashlib.sha512()
            elif self.hash_algorithm == 'blake2b':
                hash_obj = hashlib.blake2b()
            
            hash_obj.update(self.input_text.encode())
            result = hash_obj.hexdigest()
            
            return result
        except Exception as e:
            print(f"{Fore.RED}[!] Hashing error: {e}")
            return None

    def hash_file(self):
        """Хеширует файл"""
        try:
            if self.hash_algorithm == 'md5':
                hash_obj = hashlib.md5()
            elif self.hash_algorithm == 'sha1':
                hash_obj = hashlib.sha1()
            elif self.hash_algorithm == 'sha256':
                hash_obj = hashlib.sha256()
            elif self.hash_algorithm == 'sha512':
                hash_obj = hashlib.sha512()
            elif self.hash_algorithm == 'blake2b':
                hash_obj = hashlib.blake2b()
            
            with open(self.input_file, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            result = hash_obj.hexdigest()
            return result
        except Exception as e:
            print(f"{Fore.RED}[!] File hashing error: {e}")
            return None

    def save_result(self, data, operation_type):
        """Сохраняет результат"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        timestamp = int(time.time())
        filename = f"{operation_type}_{timestamp}.bin"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(data)
        
        print(f"{Fore.GREEN}[+] Result saved: {filepath}")
        return filepath

    def run(self):
        """Основной метод запуска"""
        try:
            print(f"{Fore.CYAN}[*] Processing...")
            
            result = None
            
            if self.operation == 'encrypt_text':
                result = self.encrypt_text()
                if result:
                    print(f"{Fore.GREEN}[+] Encrypted text: {result}")
            elif self.operation == 'decrypt_text':
                result = self.decrypt_text()
                if result:
                    print(f"{Fore.GREEN}[+] Decrypted text: {result}")
            elif self.operation == 'encrypt_file':
                result = self.encrypt_file()
                if result:
                    print(f"{Fore.GREEN}[+] File encrypted: {result}")
            elif self.operation == 'decrypt_file':
                result = self.decrypt_file()
                if result:
                    print(f"{Fore.GREEN}[+] File decrypted: {result}")
            elif self.operation == 'generate_key':
                result = self.generate_key()
                if result:
                    print(f"{Fore.GREEN}[+] Generated key: {result}")
            elif self.operation == 'hash_text':
                result = self.hash_text()
                if result:
                    print(f"{Fore.GREEN}[+] Hash ({self.hash_algorithm}): {result}")
            elif self.operation == 'hash_file':
                result = self.hash_file()
                if result:
                    print(f"{Fore.GREEN}[+] File hash ({self.hash_algorithm}): {result}")
            
            if result:
                print(f"{Fore.GREEN}[+] Operation completed successfully!")
                return True
            else:
                print(f"{Fore.RED}[!] Operation failed!")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")
            return False

def main():
    """Главная функция"""
    tool = EncryptionTool()
    
    try:
        tool.print_banner()
        
        if tool.get_user_input():
            tool.run()
        else:
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation interrupted")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}")

if __name__ == "__main__":
    main() 