#!/usr/bin/env python3
"""
Advanced Web Scraper
Part of QuantumKit v6.0
"""
import os
import sys
import time
import requests
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

class WebScraper:
    def __init__(self):
        self.url = ""
        self.scrape_type = "single"
        self.output_dir = "scraped_data"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.timeout = 30
        self.delay = 0.1  # Уменьшаем задержку для максимальной скорости
        self.max_pages = 1000  # Увеличиваем максимальное количество страниц
        self.extract_links = True
        self.extract_images = True
        self.extract_text = True
        self.extract_emails = True
        self.extract_phones = True
        self.session = requests.Session()

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
{Fore.MAGENTA}                              WEB SCRAPER
{Fore.MAGENTA}                              by Sqrilizz
"""
        print(banner)
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          ADVANCED WEB SCRAPER                               ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Получает настройки от пользователя"""
        print(f"{Fore.CYAN}[*] Web Scraper Configuration")
        print(f"{Fore.CYAN}[*] =========================")
        
        # URL для скрапинга
        while True:
            url = input(f"{Fore.YELLOW}[?] Enter URL to scrape: ").strip()
            if url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                self.url = url
                break
            else:
                print(f"{Fore.RED}[!] URL cannot be empty!")

        # Тип скрапинга
        print(f"\n{Fore.YELLOW}[*] Scraping Type:")
        print(f"{Fore.WHITE}    1. Single page")
        print(f"{Fore.WHITE}    2. Multiple pages (follow links)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-2): ").strip()
                if choice in ['1', '2']:
                    self.scrape_type = 'single' if choice == '1' else 'multiple'
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-2.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Настройки для множественного скрапинга
        if self.scrape_type == 'multiple':
            while True:
                try:
                    max_pages_input = input(f"{Fore.YELLOW}[?] Maximum pages to scrape (1-100, default 10): ").strip()
                    if max_pages_input:
                        self.max_pages = int(max_pages_input)
                        if 1 <= self.max_pages <= 1000:
                            break
                        else:
                            print(f"{Fore.RED}[!] Max pages must be between 1 and 1000!")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}[!] Invalid number!")

        # Что извлекать
        print(f"\n{Fore.YELLOW}[*] What to extract:")
        print(f"{Fore.WHITE}    1. All data")
        print(f"{Fore.WHITE}    2. Custom selection")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-2): ").strip()
                if choice == '1':
                    break
                elif choice == '2':
                    self.get_extraction_settings()
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-2.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Настройки запросов
        self.get_request_settings()

        return True

    def get_extraction_settings(self):
        """Получает настройки извлечения данных"""
        print(f"\n{Fore.CYAN}[*] Extraction Settings:")
        
        # Ссылки
        links_input = input(f"{Fore.YELLOW}[?] Extract links? (y/n, default y): ").strip().lower()
        self.extract_links = links_input != 'n'
        
        # Изображения
        images_input = input(f"{Fore.YELLOW}[?] Extract images? (y/n, default y): ").strip().lower()
        self.extract_images = images_input != 'n'
        
        # Текст
        text_input = input(f"{Fore.YELLOW}[?] Extract text? (y/n, default y): ").strip().lower()
        self.extract_text = text_input != 'n'
        
        # Email
        emails_input = input(f"{Fore.YELLOW}[?] Extract emails? (y/n, default y): ").strip().lower()
        self.extract_emails = emails_input != 'n'
        
        # Телефоны
        phones_input = input(f"{Fore.YELLOW}[?] Extract phone numbers? (y/n, default y): ").strip().lower()
        self.extract_phones = phones_input != 'n'

    def get_request_settings(self):
        """Получает настройки запросов"""
        print(f"\n{Fore.CYAN}[*] Request Settings:")
        
        # User Agent
        user_agent_input = input(f"{Fore.YELLOW}[?] Custom User Agent (or Enter for default): ").strip()
        if user_agent_input:
            self.user_agent = user_agent_input
        
        # Timeout
        while True:
            try:
                timeout_input = input(f"{Fore.YELLOW}[?] Request timeout in seconds (5-60, default 30): ").strip()
                if timeout_input:
                    self.timeout = int(timeout_input)
                    if 5 <= self.timeout <= 60:
                        break
                    else:
                        print(f"{Fore.RED}[!] Timeout must be between 5 and 60!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid timeout!")
        
        # Delay
        while True:
            try:
                delay_input = input(f"{Fore.YELLOW}[?] Delay between requests in seconds (0-10, default 1): ").strip()
                if delay_input:
                    self.delay = float(delay_input)
                    if 0 <= self.delay <= 10:
                        break
                    else:
                        print(f"{Fore.RED}[!] Delay must be between 0 and 10!")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}[!] Invalid delay!")

    def setup_session(self):
        """Оптимизированная настройка сессии с connection pooling"""
        # Настройка connection pooling для максимальной производительности
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=100,
            max_retries=3,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def get_page_content(self, url):
        """Получает содержимое страницы"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text, response.url
        except requests.RequestException as e:
            print(f"{Fore.RED}[!] Error fetching {url}: {e}")
            return None, None

    def extract_links_from_page(self, soup, base_url):
        """Извлекает ссылки со страницы"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Фильтруем только HTTP/HTTPS ссылки
            if absolute_url.startswith(('http://', 'https://')):
                links.append({
                    'url': absolute_url,
                    'text': link.get_text(strip=True),
                    'title': link.get('title', '')
                })
        
        return links

    def extract_images_from_page(self, soup, base_url):
        """Извлекает изображения со страницы"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                absolute_url = urljoin(base_url, src)
                images.append({
                    'url': absolute_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                })
        
        return images

    def extract_text_from_page(self, soup):
        """Извлекает текст со страницы"""
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Получаем текст
        text = soup.get_text()
        
        # Очищаем текст
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text

    def extract_emails_from_text(self, text):
        """Извлекает email адреса из текста"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Убираем дубликаты

    def extract_phones_from_text(self, text):
        """Извлекает номера телефонов из текста"""
        # Паттерны для разных форматов телефонов
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890
            r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (123) 456-7890
            r'\b\+\d{1,3}\s*\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # +1 123-456-7890
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        
        return list(set(phones))  # Убираем дубликаты

    def scrape_single_page(self, url):
        """Скрапит одну страницу"""
        print(f"{Fore.CYAN}[*] Scraping: {url}")
        
        content, final_url = self.get_page_content(url)
        if not content:
            return None
        
        soup = BeautifulSoup(content, 'html.parser')
        
        data = {
            'url': final_url,
            'title': soup.title.string if soup.title else '',
            'links': [],
            'images': [],
            'text': '',
            'emails': [],
            'phones': []
        }
        
        # Извлекаем данные в зависимости от настроек
        if self.extract_links:
            data['links'] = self.extract_links_from_page(soup, final_url)
            print(f"{Fore.GREEN}[+] Found {len(data['links'])} links")
        
        if self.extract_images:
            data['images'] = self.extract_images_from_page(soup, final_url)
            print(f"{Fore.GREEN}[+] Found {len(data['images'])} images")
        
        if self.extract_text:
            data['text'] = self.extract_text_from_page(soup)
            print(f"{Fore.GREEN}[+] Extracted text ({len(data['text'])} characters)")
        
        if self.extract_emails:
            data['emails'] = self.extract_emails_from_text(data['text'])
            print(f"{Fore.GREEN}[+] Found {len(data['emails'])} emails")
        
        if self.extract_phones:
            data['phones'] = self.extract_phones_from_text(data['text'])
            print(f"{Fore.GREEN}[+] Found {len(data['phones'])} phone numbers")
        
        return data

    def scrape_multiple_pages(self, start_url):
        """Скрапит несколько страниц"""
        print(f"{Fore.CYAN}[*] Multi-page scraping started")
        
        visited_urls = set()
        urls_to_visit = [start_url]
        all_data = []
        
        page_count = 0
        
        while urls_to_visit and page_count < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in visited_urls:
                continue
            
            visited_urls.add(current_url)
            page_count += 1
            
            print(f"{Fore.CYAN}[*] Scraping page {page_count}/{self.max_pages}: {current_url}")
            
            data = self.scrape_single_page(current_url)
            if data:
                all_data.append(data)
                
                # Добавляем новые ссылки для посещения
                if self.extract_links and len(urls_to_visit) < self.max_pages:
                    for link in data['links']:
                        link_url = link['url']
                        if link_url not in visited_urls and link_url not in urls_to_visit:
                            urls_to_visit.append(link_url)
                            if len(urls_to_visit) >= self.max_pages:
                                break
            
            # Задержка между запросами
            if self.delay > 0 and page_count < self.max_pages:
                time.sleep(self.delay)
        
        return all_data

    def save_results(self, data, filename=None):
        """Сохраняет результаты"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not filename:
            timestamp = int(time.time())
            filename = f"scraped_data_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}[+] Results saved: {filepath}")
        return filepath

    def run(self):
        """Основной метод запуска"""
        try:
            print(f"{Fore.CYAN}[*] Starting web scraper...")
            
            # Настраиваем сессию
            self.setup_session()
            
            # Скрапим данные
            if self.scrape_type == 'single':
                data = self.scrape_single_page(self.url)
                if data:
                    results = [data]
                else:
                    print(f"{Fore.RED}[!] Failed to scrape page")
                    return False
            else:
                results = self.scrape_multiple_pages(self.url)
            
            if not results:
                print(f"{Fore.RED}[!] No data scraped")
                return False
            
            # Сохраняем результаты
            filepath = self.save_results(results)
            
            # Выводим статистику
            print(f"\n{Fore.CYAN}[*] Scraping completed!")
            print(f"{Fore.GREEN}[+] Total pages scraped: {len(results)}")
            
            total_links = sum(len(page.get('links', [])) for page in results)
            total_images = sum(len(page.get('images', [])) for page in results)
            total_emails = sum(len(page.get('emails', [])) for page in results)
            total_phones = sum(len(page.get('phones', [])) for page in results)
            
            print(f"{Fore.GREEN}[+] Total links found: {total_links}")
            print(f"{Fore.GREEN}[+] Total images found: {total_images}")
            print(f"{Fore.GREEN}[+] Total emails found: {total_emails}")
            print(f"{Fore.GREEN}[+] Total phone numbers found: {total_phones}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error during scraping: {e}")
            return False

def main():
    """Главная функция"""
    scraper = WebScraper()
    
    try:
        scraper.print_banner()
        
        if scraper.get_user_input():
            scraper.run()
        else:
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation interrupted")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}")

if __name__ == "__main__":
    main() 