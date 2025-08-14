import os
import time
import subprocess
import sys
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# Импорт новых UI компонентов
try:
    from src.utils.ui import (
        print_banner, print_success, print_error, print_warning, print_info, 
        print_separator, Notification, Menu, Spinner, ProgressBar, 
        print_header, confirm_action, animate_loading
    )
    from src.utils.logger import get_logger
    NEW_UI_AVAILABLE = True
except ImportError:
    NEW_UI_AVAILABLE = False
    print(f"{Fore.YELLOW}Warning: New UI components not available, using fallback")

def set_console_color():
    """Устанавливает цвет консоли"""
    try:
        os.system("color 5")
    except:
        pass

def load_proxies():
    """Загружает прокси с анимацией"""
    if NEW_UI_AVAILABLE:
        spinner = Spinner("Loading proxies...")
        spinner.start()
        time.sleep(1.0)
        spinner.stop()
        print_success("Proxies loaded successfully!")
    else:
        print(f"{Fore.CYAN}Loading proxies...")
        time.sleep(1.0)
        print(f"{Fore.GREEN}Proxies loaded successfully!")

def load_proxies_file():
    """Загружает файл с прокси"""
    try:
        with open('Tools/proxies.txt', 'r', encoding='utf-8') as f:
            proxies = f.readlines()
        load_proxies()
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except FileNotFoundError:
        if NEW_UI_AVAILABLE:
            print_warning("Proxies file not found, continuing without proxies...")
        else:
            print(f"{Fore.YELLOW}Proxies file not found, continuing without proxies...")
        return []
    except Exception as e:
        if NEW_UI_AVAILABLE:
            print_error(f"Error loading proxies: {e}")
        else:
            print(f"{Fore.RED}Error loading proxies: {e}")
        return []

def run_tool(script_name):
    """Запускает выбранный инструмент"""
    tool_paths = {
        # Discord Tools
        "Universal Discord Spammer": "Tools/Universal Discord Spammer.py",
        "Universal Nuker": "Tools/Universal Nuker.py",
        "Universal Image Logger": "Tools/Universal Image Logger.py",
        "Token Checker": "Tools/Token Checker.py",
        
        # Network Tools
        "Universal Network Tool": "Tools/Universal Network Tool.py",
        "BotNet": "Tools/BotNet.py",
        
        # Security Tools
        "Brute Force": "Tools/Brute Force.py",
        "Encryption Tool": "Tools/Encryption Tool.py",
        "Link Bridge Generator": "Tools/Link Bridge Generator.py",
        
        # Utility Tools
        "Password Generator": "Tools/Password Generator.py",
        "QR Generator": "Tools/QR Generator.py",
        "Web Scraper": "Tools/Web Scraper.py",
        "Clipboard Manager": "Tools/Clipboard Manager.py",
        
        # Reporting Tools
        "Telegram Report": "Tools/Telegram Report.py"
    }
    
    if script_name in tool_paths:
        script_path = tool_paths[script_name]
        try:
            if NEW_UI_AVAILABLE:
                print_header(f"Starting {script_name}")
                print_info(f"Executing {script_name}...")
                result = subprocess.run(["python", script_path], check=True)
                print_success(f"{script_name} completed successfully!")
            else:
                print(f"{Fore.CYAN}Starting {script_name}...")
                result = subprocess.run(["python", script_path], check=True)
                print(f"{Fore.GREEN}{script_name} completed successfully!")
        except subprocess.CalledProcessError as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Error running {script_name}: {e}")
            else:
                print(f"{Fore.RED}Error running {script_name}: {e}")
        except FileNotFoundError:
            if NEW_UI_AVAILABLE:
                print_error(f"Script not found: {script_path}")
            else:
                print(f"{Fore.RED}Script not found: {script_path}")
        except KeyboardInterrupt:
            if NEW_UI_AVAILABLE:
                print_warning(f"{script_name} interrupted by user")
            else:
                print(f"{Fore.YELLOW}{script_name} interrupted by user")
        except Exception as e:
            if NEW_UI_AVAILABLE:
                print_error(f"Unexpected error running {script_name}: {e}")
            else:
                print(f"{Fore.RED}Unexpected error running {script_name}: {e}")
    else:
        if NEW_UI_AVAILABLE:
            print_error(f"Unknown tool: {script_name}")
        else:
            print(f"{Fore.RED}Unknown tool: {script_name}")

def show_system_info():
    """Показать информацию о системе"""
    if NEW_UI_AVAILABLE:
        print_header("System Information")
        
        import platform
        import psutil
        
        info_data = [
            ["Property", "Value"],
            ["OS", platform.system() + " " + platform.release()],
            ["Python Version", platform.python_version()],
            ["CPU Cores", str(psutil.cpu_count())],
            ["Memory", f"{psutil.virtual_memory().total // (1024**3)} GB"],
            ["Available Tools", "14"],
            ["QuantumKit Version", "6.2"]
        ]
        
        # Создаем таблицу
        headers = info_data[0]
        rows = info_data[1:]
        
        from src.utils.ui import create_table
        table = create_table(headers, rows, "System Information")
        print(table)
    else:
        print(f"{Fore.CYAN}System Information:")
        print(f"{Fore.WHITE}OS: {platform.system()}")
        print(f"{Fore.WHITE}Python: {platform.python_version()}")

def show_tool_categories():
    """Показать категории инструментов"""
    if NEW_UI_AVAILABLE:
        print_header("Tool Categories")
        
        categories = [
            ["Category", "Tools", "Description"],
            ["Discord Tools", "4", "Discord automation and management tools"],
            ["Network Tools", "2", "Network analysis and monitoring"],
            ["Security Tools", "3", "Security and encryption utilities"],
            ["Utility Tools", "4", "General purpose utilities"],
            ["Reporting Tools", "1", "System reporting and analysis"]
        ]
        
        headers = categories[0]
        rows = categories[1:]
        
        from src.utils.ui import create_table
        table = create_table(headers, rows, "Available Categories")
        print(table)
    else:
        print(f"{Fore.CYAN}Tool Categories:")
        print(f"{Fore.WHITE}Discord Tools: 4 tools")
        print(f"{Fore.WHITE}Network Tools: 2 tools")
        print(f"{Fore.WHITE}Security Tools: 3 tools")
        print(f"{Fore.WHITE}Utility Tools: 4 tools")
        print(f"{Fore.WHITE}Reporting Tools: 1 tool")

def main_menu():
    """Главное меню с пагинацией по категориям"""
    if NEW_UI_AVAILABLE:
        menu = Menu("QuantumKit Main Menu")
        
        # Discord Tools (Page 1)
        menu.add_option("1", "Universal Discord Spammer", 
                       lambda: run_tool("Universal Discord Spammer"), 
                       "Advanced message automation", "discord")
        menu.add_option("2", "Universal Nuker", 
                       lambda: run_tool("Universal Nuker"), 
                       "Server management and control", "discord")
        menu.add_option("3", "Universal Image Logger", 
                       lambda: run_tool("Universal Image Logger"), 
                       "Image tracking and logging", "discord")
        menu.add_option("4", "Token Checker", 
                       lambda: run_tool("Token Checker"), 
                       "Discord token validation", "discord")
        
        # Network Tools (Page 2)
        menu.add_option("5", "Universal Network Tool", 
                       lambda: run_tool("Universal Network Tool"), 
                       "Network analysis and monitoring", "network")
        menu.add_option("6", "BotNet", 
                       lambda: run_tool("BotNet"), 
                       "Bot network management system", "network")
        
        # Security Tools (Page 2)
        menu.add_option("7", "Brute Force", 
                       lambda: run_tool("Brute Force"), 
                       "Password cracking utility", "security")
        menu.add_option("8", "Encryption Tool", 
                       lambda: run_tool("Encryption Tool"), 
                       "File and text encryption", "security")
        menu.add_option("9", "Link Bridge Generator", 
                       lambda: run_tool("Link Bridge Generator"), 
                       "Secure link generation", "security")
        
        # Utility Tools (Page 3)
        menu.add_option("10", "Password Generator", 
                       lambda: run_tool("Password Generator"), 
                       "Secure password creation", "utility")
        menu.add_option("11", "Web Scraper", 
                       lambda: run_tool("Web Scraper"), 
                       "Web data extraction", "utility")
        
        # Reporting Tools (Page 3)
        menu.add_option("12", "Telegram Report", 
                       lambda: run_tool("Telegram Report"), 
                       "System analysis and reporting", "reporting")
        
        # System Options (Page 4)
        menu.add_option("S", "System Information", 
                       show_system_info, 
                       "Display system information", "system")
        menu.add_option("C", "Tool Categories", 
                       show_tool_categories, 
                       "Show available tool categories", "system")
        
        menu.display()
    else:
        # Fallback to old menu system
        print_banner()
        print(f"{Fore.CYAN}Available Tools:")
        print(f"{Fore.WHITE}1. Universal Discord Spammer")
        print(f"{Fore.WHITE}2. Universal Nuker")
        print(f"{Fore.WHITE}3. Universal Image Logger")
        print(f"{Fore.WHITE}4. Token Checker")
        print(f"{Fore.WHITE}5. Universal Network Tool")
        print(f"{Fore.WHITE}6. BotNet")
        print(f"{Fore.WHITE}7. Brute Force")
        print(f"{Fore.WHITE}8. Encryption Tool")
        print(f"{Fore.WHITE}9. Link Bridge Generator")
        print(f"{Fore.WHITE}10. Password Generator")
        print(f"{Fore.WHITE}11. QR Generator")
        print(f"{Fore.WHITE}12. Web Scraper")
        print(f"{Fore.WHITE}13. Clipboard Manager")
        print(f"{Fore.WHITE}14. SMALL Report")
        print(f"{Fore.WHITE}0. Exit")
        
        while True:
            choice = input(f"{Fore.GREEN}>>> ").strip()
            
            if choice == "0":
                print(f"{Fore.GREEN}Exiting...")
                break
            elif choice == "1":
                run_tool("Universal Discord Spammer")
            elif choice == "2":
                run_tool("Universal Nuker")
            elif choice == "3":
                run_tool("Universal Image Logger")
            elif choice == "4":
                run_tool("Token Checker")
            elif choice == "5":
                run_tool("Universal Network Tool")
            elif choice == "6":
                run_tool("BotNet")
            elif choice == "7":
                run_tool("Brute Force")
            elif choice == "8":
                run_tool("Encryption Tool")
            elif choice == "9":
                run_tool("Link Bridge Generator")
            elif choice == "10":
                run_tool("Password Generator")
            elif choice == "11":
                run_tool("QR Generator")
            elif choice == "12":
                run_tool("Web Scraper")
            elif choice == "13":
                run_tool("Clipboard Manager")
            elif choice == "14":
                run_tool("SMALL Report")
            else:
                print(f"{Fore.RED}Invalid choice!")
                time.sleep(1)
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...")

def main():
    """Главная функция"""
    try:
        set_console_color()
        
        if NEW_UI_AVAILABLE:
            print_banner()
            
            # Загружаем прокси
            proxies = load_proxies_file()
            
            print_info("QuantumKit is ready!")
            print_warning("Press Ctrl+C to return to menu from any tool")
            print_separator()
            
            # Запускаем главное меню
            main_menu()
        else:
            # Fallback для старого UI
            print_banner()
            proxies = load_proxies_file()
            print(f"{Fore.MAGENTA}If you're done using a tool, press Ctrl+C to return to menu")
            print(f"{Fore.MAGENTA}Made by Sqrilizz")
            main_menu()
        
    except KeyboardInterrupt:
        if NEW_UI_AVAILABLE:
            print_warning("Exiting QuantumKit...")
        else:
            print(f"\n{Fore.YELLOW}Exiting...")
    except Exception as e:
        if NEW_UI_AVAILABLE:
            print_error(f"Fatal error: {e}")
        else:
            print(f"{Fore.RED}Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
