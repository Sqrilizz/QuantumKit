import os
import time
import subprocess
import sys
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

def set_console_color():
    """Устанавливает цвет консоли"""
    try:
        os.system("color 5")
    except:
        pass

def load_proxies():
    """Загружает прокси с анимацией"""
    print(f"{Fore.CYAN}Loading proxies...")
    for i in range(5):
        time.sleep(0.1)
        print(".", end='', flush=True)
    time.sleep(0.5)
    print(f"\n{Fore.GREEN}Proxies loaded successfully!")
    time.sleep(0.3)
    print(f"{Fore.CYAN}Activating proxies...")
    for i in range(5):
        time.sleep(0.1)
        print(".", end='', flush=True)
    time.sleep(0.5)
    print(f"\n{Fore.GREEN}Proxies activated!")

def load_proxies_file():
    """Загружает файл с прокси"""
    try:
        with open('Tools/proxies.txt', 'r', encoding='utf-8') as f:
            proxies = f.readlines()
        load_proxies()
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except FileNotFoundError:
        print(f"{Fore.YELLOW}Proxies file not found, continuing without proxies...")
        return []
    except Exception as e:
        print(f"{Fore.RED}Error loading proxies: {e}")
        return []

def print_banner():
    """Выводит баннер QuantumKit"""
    banner = [
        "   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓",
        " ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒",
        " ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░",
        " ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ ",
        " ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒",
        " ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░",
        "  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░",
        "    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   ",
        "     ░       ░           ░  ░         ░             ░            ░   ",
        "",
        "                                by Sqrilizz"
    ]
    
    for line in banner:
        print(f"{Fore.MAGENTA}{line}")
    
    time.sleep(1)

def run_tool(script_name):
    """Запускает выбранный инструмент"""
    tool_paths = {
        "WebhookSpam": "Tools/WebhookSpam.py",
        "Server Nuker": "Tools/Server Nuker.py",
        "ImageLogger": "src/utils/image_logger_enhanced.py",
        "DDOS": "Tools/DDOS.py",
        "Discord Spam": "Tools/Discord Spam/DiscordSpam.py",

        "IP Pinger": "Tools/IP Pinger.py",
        "Token Checker": "Tools/Token Checker.py",
        "Token Nuker": "Tools/Token Nuker.py",
        "Password Generator": "Tools/Password Generator.py",
        "Brute Force": "Tools/Brute Force.py"
    }
    
    if script_name in tool_paths:
        script_path = tool_paths[script_name]
        try:
            print(f"{Fore.CYAN}Starting {script_name}...")
            result = subprocess.run(["python", script_path], check=True)
            print(f"{Fore.GREEN}{script_name} completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error running {script_name}: {e}")
        except FileNotFoundError:
            print(f"{Fore.RED}Script not found: {script_path}")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}{script_name} interrupted by user")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error running {script_name}: {e}")
    else:
        print(f"{Fore.RED}Unknown tool: {script_name}")

def main_menu():
    """Главное меню"""
    page1_options = [
        "WebhookSpam",
        "Server Nuker",
        "ImageLogger",
        "DDOS",
        "Discord Spam",

        "IP Pinger",
        "Token Checker",
        "Token Nuker"
    ]
    
    page2_options = [
        "Password Generator",
        "Brute Force"
    ]
    
    current_page = 1
    
    while True:
        try:
            if current_page == 1:
                options = page1_options
                print(f"\n{Fore.MAGENTA}=== PAGE 1 - MAIN TOOLS ===\n")
            else:
                options = page2_options
                print(f"\n{Fore.MAGENTA}=== PAGE 2 - UTILITY TOOLS ===\n")
            
            for i, option in enumerate(options, 1):
                print(f"{Fore.MAGENTA}{i}. {option}")
            
            print(f"{Fore.MAGENTA}0. Exit")
            if current_page == 1:
                print(f"{Fore.MAGENTA}N. Next Page")
            else:
                print(f"{Fore.MAGENTA}P. Previous Page")
            
            choice = input(f"\n{Fore.MAGENTA}Enter your choice: ").strip().upper()
            
            if choice == "0":
                print(f"{Fore.GREEN}Goodbye!")
                break
            elif choice == "N" and current_page == 1:
                current_page = 2
                continue
            elif choice == "P" and current_page == 2:
                current_page = 1
                continue
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    script_name = options[choice_num - 1]
                    run_tool(script_name)
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(options)}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Returning to menu...")
                continue
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Exiting...")
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}")

def main():
    """Главная функция"""
    try:
        set_console_color()
        print_banner()
        
        # Загружаем прокси
        proxies = load_proxies_file()
        
        print(f"{Fore.MAGENTA}If you're done using a tool, press Ctrl+C to return to menu")
        print(f"{Fore.MAGENTA}Made by Sqrilizz")
        
        # Запускаем главное меню
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting...")
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
