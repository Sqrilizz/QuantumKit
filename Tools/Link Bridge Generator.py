#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Bridge Generator - Генератор публичных ссылок-мостов
Автор: Sqrilizz
Версия: 1.0
"""

import os
import sys
import time
import json
import uuid
import hashlib
import threading
import subprocess
import tempfile
import shutil
import secrets
import logging
import base64
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs, quote
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from colorama import init, Fore, Style
import socket

# Инициализация colorama
init(autoreset=True)

class LinkBridgeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Обрабатывает POST запросы"""
        try:
            # Парсим путь
            path_parts = self.path.split('/')
            if len(path_parts) < 4 or path_parts[1] != 'bridge':
                self.send_error(404, "Invalid bridge path")
                return
                
            bridge_id = path_parts[2]
            bridge_hash = path_parts[3]
            
            # Отслеживаем посещение
            user_agent = self.headers.get('User-Agent', 'Unknown')
            self.server.bridge._track_visit(bridge_id, self, user_agent)
            
            # Читаем данные запроса
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Обрабатываем запрос
            result = self.server.bridge.process_bridge_request(bridge_id, request_data)
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(result, default=str).encode('utf-8')
            self.wfile.write(response)
            
        except Exception as e:
            self.server.bridge.logger.error(f"Link bridge handler error: {e}")
            self.send_error(500, str(e))
            
    def do_GET(self):
        """Обрабатывает GET запросы"""
        if self.path.startswith('/l/'):
            # Короткие ссылки
            short_code = self.path[3:]  # Убираем '/l/'
            
            try:
                # Находим мост по короткому коду
                bridge_id = self.server.bridge.get_bridge_by_short_code(short_code)
                if bridge_id and self.server.bridge.validate_bridge(bridge_id, "dummy_hash"):
                    bridge = self.server.bridge.active_bridges[bridge_id]
                    
                    # Отслеживаем посещение по короткой ссылке
                    user_agent = self.headers.get('User-Agent', 'Unknown')
                    self.server.bridge._track_visit(bridge_id, self, user_agent)
                    
                    # Создаем HTML страницу с редиректом
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Redirecting...</title>
                        <meta http-equiv="refresh" content="0;url={bridge['target_url']}">
                        <style>
                            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                            .loader {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }}
                            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                        </style>
                    </head>
                    <body>
                        <h2>Redirecting to target...</h2>
                        <div class="loader"></div>
                        <p>If you are not redirected automatically, <a href="{bridge['target_url']}">click here</a></p>
                    </body>
                    </html>
                    """
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))
                else:
                    self.send_error(404, "Link not found")
            except Exception as e:
                self.send_error(500, str(e))
                
        elif self.path == '/status':
            # Отслеживаем посещение статуса
            user_agent = self.headers.get('User-Agent', 'Unknown')
            self.server.bridge._track_visit('status_check', self, user_agent)
            
            # Статус моста
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            status_data = {
                'bridge_id': self.server.bridge.session_id,
                'active_bridges': len(self.server.bridge.active_bridges),
                'uptime': time.time() - self.server.bridge.start_time,
                'status': 'running'
            }
            
            response = json.dumps(status_data).encode('utf-8')
            self.wfile.write(response)
        elif self.path == '/stats':
            # Отслеживаем посещение статистики
            user_agent = self.headers.get('User-Agent', 'Unknown')
            self.server.bridge._track_visit('stats_check', self, user_agent)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            stats_data = self.server.bridge.get_stats_summary()
            response = json.dumps(stats_data, default=str).encode('utf-8')
            self.wfile.write(response)
        else:
            self.send_error(404, "Not found")
            
    def log_message(self, format, *args):
        """Отключаем стандартное логирование"""
        pass

class LinkBridgeGenerator:
    def __init__(self):
        self.session_id = secrets.token_hex(8)
        self.active_bridges = {}
        self.bridge_timeout = 7200  # 2 часа
        self.max_bridges = 20
        self.rate_limit = 200  # запросов в минуту
        self.allowed_domains = set()
        self.start_time = time.time()
        self.is_running = False
        
        # Система отслеживания и статистики
        self.visitor_stats = {
            'total_visits': 0,
            'unique_ips': set(),
            'ip_details': {},  # IP -> {count, first_seen, last_seen, user_agent, country}
            'bridge_activity': {},  # bridge_id -> [visits]
            'hourly_stats': {},  # hour -> count
            'daily_stats': {}   # date -> count
        }
        
        # Настройки сервера
        self.host = '0.0.0.0'  # Слушаем на всех интерфейсах
        self.port = 8081
        self.server = None
        self.ngrok_process = None
        self.localtunnel_process = None
        self.public_url = None
        
        # Логирование
        self.output_dir = Path("output/link_bridges")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / f"link_bridge_{self.session_id}.log"
        self.stats_file = self.output_dir / f"link_stats_{self.session_id}.json"
        self._setup_logging()
        
        # Запускаем Ngrok для публичного доступа
        self._start_ngrok()
    
    def _start_ngrok(self):
        """Запускает Ngrok для публичного доступа"""
        try:
            # Проверяем, установлен ли ngrok
            result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Fore.CYAN}Starting Ngrok tunnel...")
                
                # Запускаем ngrok в фоне
                self.ngrok_process = subprocess.Popen(
                    ['ngrok', 'http', str(self.port)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Ждем немного для запуска
                time.sleep(3)
                
                # Получаем публичный URL
                try:
                    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                    if response.status_code == 200:
                        tunnels = response.json()['tunnels']
                        if tunnels:
                            self.public_url = tunnels[0]['public_url']
                            print(f"{Fore.GREEN}✓ Ngrok tunnel started: {self.public_url}")
                            self.logger.info(f"Ngrok tunnel started: {self.public_url}")
                        else:
                            print(f"{Fore.YELLOW}⚠ Ngrok started but no tunnels found")
                    else:
                        print(f"{Fore.YELLOW}⚠ Could not get Ngrok tunnel info")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠ Could not get Ngrok URL: {e}")
            else:
                print(f"{Fore.YELLOW}⚠ Ngrok not found. Install from: https://ngrok.com/")
                self._setup_localtunnel()
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Error starting Ngrok: {e}")
            self._setup_localtunnel()

    def _check_nodejs(self):
        """Проверяет установлен ли Node.js"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"{Fore.GREEN}✓ Node.js найден: {version}")
                return True
            else:
                print(f"{Fore.RED}✗ Node.js не найден")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"{Fore.RED}✗ Node.js не установлен")
            return False

    def _check_localtunnel(self):
        """Проверяет установлен ли LocalTunnel"""
        # Проверяем команду lt в PATH
        try:
            result = subprocess.run(['lt', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"{Fore.GREEN}✓ LocalTunnel найден: {version}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Проверяем через npm
        try:
            result = subprocess.run(['npm', 'list', '-g', 'localtunnel'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and 'localtunnel' in result.stdout:
                print(f"{Fore.GREEN}✓ LocalTunnel установлен через npm")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Проверяем в стандартных местах установки npm
        npm_paths = [
            os.path.expanduser("~\\AppData\\Roaming\\npm\\lt.cmd"),
            os.path.expanduser("~\\AppData\\Roaming\\npm\\lt"),
            "C:\\Program Files\\nodejs\\lt.cmd",
            "C:\\Program Files\\nodejs\\lt"
        ]
        
        for path in npm_paths:
            if os.path.exists(path):
                print(f"{Fore.GREEN}✓ LocalTunnel найден: {path}")
                return True
        
        print(f"{Fore.RED}✗ LocalTunnel не найден")
        return False

    def _install_localtunnel(self):
        """Устанавливает LocalTunnel"""
        print(f"{Fore.YELLOW}Устанавливаем LocalTunnel...")
        try:
            result = subprocess.run(['npm', 'install', '-g', 'localtunnel'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"{Fore.GREEN}✓ LocalTunnel успешно установлен!")
                return True
            else:
                print(f"{Fore.RED}✗ Ошибка установки LocalTunnel:")
                print(f"{Fore.RED}{result.stderr}")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"{Fore.RED}✗ Ошибка установки: {e}")
            return False

    def _start_localtunnel(self):
        """Автоматически запускает LocalTunnel и захватывает публичный URL"""
        try:
            # Находим путь к LocalTunnel
            lt_path = None
            
            # Проверяем в PATH
            try:
                result = subprocess.run(['where', 'lt'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lt_path = 'lt'
            except:
                pass
            
            # Проверяем в стандартных местах
            if not lt_path:
                npm_paths = [
                    os.path.expanduser("~\\AppData\\Roaming\\npm\\lt.cmd"),
                    os.path.expanduser("~\\AppData\\Roaming\\npm\\lt"),
                    "C:\\Program Files\\nodejs\\lt.cmd",
                    "C:\\Program Files\\nodejs\\lt"
                ]
                
                for path in npm_paths:
                    if os.path.exists(path):
                        lt_path = path
                        break
            
            # Если не нашли lt, используем npx
            if not lt_path:
                npx_path = "C:\\Program Files\\nodejs\\npx.cmd"
                if os.path.exists(npx_path):
                    cmd = [npx_path, 'localtunnel', '--port', str(self.port)]
                else:
                    cmd = ['npx', 'localtunnel', '--port', str(self.port)]
            else:
                cmd = [lt_path, '--port', str(self.port)]
            
            print(f"{Fore.CYAN}Запускаем LocalTunnel: {' '.join(cmd)}")
            
            # Запускаем LocalTunnel в фоне
            self.localtunnel_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Ждем немного для запуска
            time.sleep(3)
            
            # Проверяем что процесс запущен
            if self.localtunnel_process.poll() is None:
                print(f"{Fore.GREEN}✓ LocalTunnel процесс запущен (PID: {self.localtunnel_process.pid})")
                
                # Пытаемся получить публичный URL из вывода
                try:
                    # Читаем вывод процесса
                    if self.localtunnel_process.stdout:
                        output = self.localtunnel_process.stdout.read().decode('utf-8', errors='ignore')
                        # Ищем URL в выводе (обычно выглядит как "https://something.loca.lt")
                        import re
                        url_match = re.search(r'https://[a-zA-Z0-9\-]+\.loca\.lt', output)
                        if url_match:
                            self.public_url = url_match.group(0)
                            print(f"{Fore.GREEN}✓ Публичный URL: {self.public_url}")
                        else:
                            # Если не нашли в stdout, пробуем stderr
                            if self.localtunnel_process.stderr:
                                stderr_output = self.localtunnel_process.stderr.read().decode('utf-8', errors='ignore')
                                url_match = re.search(r'https://[a-zA-Z0-9\-]+\.loca\.lt', stderr_output)
                                if url_match:
                                    self.public_url = url_match.group(0)
                                    print(f"{Fore.GREEN}✓ Публичный URL: {self.public_url}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠ Не удалось получить публичный URL: {e}")
                
                return True
            else:
                print(f"{Fore.RED}✗ LocalTunnel процесс завершился")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Ошибка запуска LocalTunnel: {e}")
            return False

    def _setup_localtunnel(self):
        """Настраивает LocalTunnel"""
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                              LOCALTUNNEL SETUP                              ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Проверяем Node.js
        if not self._check_nodejs():
            print(f"\n{Fore.RED}Node.js не найден!")
            print(f"{Fore.YELLOW}Скачайте и установите Node.js с: https://nodejs.org/")
            print(f"{Fore.YELLOW}После установки перезапустите инструмент.")
            return False
        
        # Проверяем LocalTunnel
        if not self._check_localtunnel():
            print(f"\n{Fore.YELLOW}LocalTunnel не найден. Устанавливаем...")
            if not self._install_localtunnel():
                print(f"{Fore.RED}Не удалось установить LocalTunnel!")
                return False
        
        # Автоматически запускаем LocalTunnel
        print(f"\n{Fore.GREEN}=== АВТОМАТИЧЕСКИЙ ЗАПУСК LOCALTUNNEL ===")
        if self._start_localtunnel():
            print(f"{Fore.GREEN}✓ LocalTunnel запущен автоматически!")
        else:
            print(f"{Fore.YELLOW}⚠ Не удалось запустить LocalTunnel автоматически")
            print(f"{Fore.CYAN}Выполните команду вручную в новом терминале:")
            print(f"{Fore.YELLOW}lt --port {self.port}")
        
        # Показываем локальный доступ как резервный
        local_ip = self._get_local_ip()
        print(f"\n{Fore.GREEN}=== ЛОКАЛЬНЫЙ ДОСТУП (РЕЗЕРВНЫЙ) ===")
        print(f"{Fore.CYAN}Ваш локальный IP: {local_ip}")
        print(f"{Fore.CYAN}Локальный URL: http://{local_ip}:{self.port}")
        print(f"{Fore.YELLOW}Делитесь этим URL с людьми в той же сети")
        
        return True

    def _show_localtunnel_setup(self):
        """Показывает настройку LocalTunnel"""
        self._setup_localtunnel()

    def _get_local_ip(self):
        """Получает локальный IP адрес"""
        try:
            import socket
            # Подключаемся к внешнему серверу чтобы узнать наш IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return None

    def _save_access_info(self, local_ip):
        """Сохраняет информацию о способах доступа"""
        access_info = {
            'timestamp': datetime.now().isoformat(),
            'local_access': f"http://localhost:{self.port}",
            'network_access': f"http://{local_ip}:{self.port}" if local_ip else None,
            'port': self.port,
            'local_ip': local_ip,
            'instructions': {
                'local_network': f"Share http://{local_ip}:{self.port} with people on same network",
                'port_forwarding': f"Forward port {self.port} in router for internet access",
                'alternatives': [
                    "Cloudflare Tunnel: cloudflared tunnel --url http://localhost:8081",
                    "LocalTunnel: lt --port 8081",
                    "Serveo: ssh -R 80:localhost:8081 serveo.net"
                ]
            }
        }
        
        access_file = self.output_dir / f"access_info_{self.session_id}.json"
        with open(access_file, 'w', encoding='utf-8') as f:
            json.dump(access_info, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{Fore.CYAN}Access info saved to: {access_file}")

    def _stop_ngrok(self):
        """Останавливает Ngrok"""
        if self.ngrok_process:
            try:
                self.ngrok_process.terminate()
                self.ngrok_process.wait(timeout=5)
                print(f"{Fore.GREEN}✓ Ngrok tunnel stopped")
            except:
                self.ngrok_process.kill()
                print(f"{Fore.YELLOW}⚠ Ngrok process killed")
    
    def _setup_logging(self):
        """Настройка логирования"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Создаем handler для файла
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Создаем handler для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Создаем форматтер
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Добавляем handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def _get_client_ip(self, request_handler) -> str:
        """Получает реальный IP клиента"""
        # Проверяем различные заголовки для получения реального IP
        headers_to_check = [
            'X-Forwarded-For',
            'X-Real-IP', 
            'X-Client-IP',
            'CF-Connecting-IP',  # Cloudflare
            'True-Client-IP'
        ]
        
        for header in headers_to_check:
            ip = request_handler.headers.get(header)
            if ip:
                # Берем первый IP из списка (если несколько)
                return ip.split(',')[0].strip()
        
        # Если заголовки не найдены, используем адрес клиента
        return request_handler.client_address[0]
    
    def _get_ip_info(self, ip: str) -> Dict[str, str]:
        """Получает информацию об IP (страна, город и т.д.)"""
        try:
            # Используем бесплатный API для получения информации об IP
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown')
                }
        except:
            pass
        return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown', 'timezone': 'Unknown'}
    
    def _track_visit(self, bridge_id: str, request_handler, user_agent: str = "Unknown"):
        """Отслеживает посещение и обновляет статистику"""
        client_ip = self._get_client_ip(request_handler)
        current_time = datetime.now()
        
        # Обновляем общую статистику
        self.visitor_stats['total_visits'] += 1
        self.visitor_stats['unique_ips'].add(client_ip)
        
        # Обновляем статистику по IP
        if client_ip not in self.visitor_stats['ip_details']:
            ip_info = self._get_ip_info(client_ip)
            self.visitor_stats['ip_details'][client_ip] = {
                'count': 1,
                'first_seen': current_time.isoformat(),
                'last_seen': current_time.isoformat(),
                'user_agent': user_agent,
                'country': ip_info['country'],
                'city': ip_info['city'],
                'isp': ip_info['isp'],
                'timezone': ip_info['timezone']
            }
        else:
            self.visitor_stats['ip_details'][client_ip]['count'] += 1
            self.visitor_stats['ip_details'][client_ip]['last_seen'] = current_time.isoformat()
            if user_agent != "Unknown":
                self.visitor_stats['ip_details'][client_ip]['user_agent'] = user_agent
        
        # Обновляем статистику по мостам
        if bridge_id not in self.visitor_stats['bridge_activity']:
            self.visitor_stats['bridge_activity'][bridge_id] = []
        
        visit_data = {
            'timestamp': current_time.isoformat(),
            'ip': client_ip,
            'user_agent': user_agent,
            'bridge_id': bridge_id
        }
        self.visitor_stats['bridge_activity'][bridge_id].append(visit_data)
        
        # Обновляем почасовую статистику
        hour_key = current_time.strftime('%Y-%m-%d %H:00')
        self.visitor_stats['hourly_stats'][hour_key] = self.visitor_stats['hourly_stats'].get(hour_key, 0) + 1
        
        # Обновляем дневную статистику
        day_key = current_time.strftime('%Y-%m-%d')
        self.visitor_stats['daily_stats'][day_key] = self.visitor_stats['daily_stats'].get(day_key, 0) + 1
        
        # Логируем посещение
        self.logger.info(f"Visit tracked: IP={client_ip}, Bridge={bridge_id}, UA={user_agent[:50]}")
        
        # Сохраняем статистику в файл
        self._save_stats()
    
    def _save_stats(self):
        """Сохраняет статистику в JSON файл"""
        try:
            # Конвертируем set в list для JSON сериализации
            stats_to_save = self.visitor_stats.copy()
            stats_to_save['unique_ips'] = list(self.visitor_stats['unique_ips'])
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_to_save, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Error saving stats: {e}")
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Возвращает краткую сводку статистики"""
        return {
            'total_visits': self.visitor_stats['total_visits'],
            'unique_visitors': len(self.visitor_stats['unique_ips']),
            'active_bridges': len(self.active_bridges),
            'top_ips': sorted(
                self.visitor_stats['ip_details'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:5],
            'recent_activity': {
                'last_hour': self.visitor_stats['hourly_stats'].get(
                    datetime.now().strftime('%Y-%m-%d %H:00'), 0
                ),
                'today': self.visitor_stats['daily_stats'].get(
                    datetime.now().strftime('%Y-%m-%d'), 0
                )
            }
        }
        
    def print_banner(self):
        """Выводит баннер Link Bridge Generator"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.MAGENTA}")
        print(" ██╗     ██╗███╗   ██╗██╗  ██╗    ██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗")
        print(" ██║     ██║████╗  ██║██║ ██╔╝    ██╔══██╗██╔══██╗██║██╔══██╗██╔═══██╗██╔════╝")
        print(" ██║     ██║██╔██╗ ██║█████╔╝     ██████╔╝██████╔╝██║██║  ██║██║   ██║███████╗")
        print(" ██║     ██║██║╚██╗██║██╔═██╗     ██╔══██╗██╔══██╗██║██║  ██║██║   ██║╚════██║")
        print(" ███████╗██║██║ ╚████║██║  ██╗    ██║  ██║██████╔╝██║██████╔╝╚██████╔╝███████║")
        print(" ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═════╝ ╚═╝╚═════╝  ╚═════╝ ╚══════╝")
        print(f"{Fore.MAGENTA}                                by Sqrilizz\n")
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                LINK BRIDGE GENERATOR v1.0 - SMART LINK PROXY                ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
    def generate_bridge_id(self) -> str:
        """Генерирует уникальный ID для моста"""
        timestamp = int(time.time())
        random_bytes = os.urandom(8)
        bridge_id = hashlib.sha256(f"{self.session_id}{timestamp}{random_bytes}".encode()).hexdigest()[:16]
        return bridge_id
        
    def create_link_bridge(self, target_url: str, bridge_type: str = "auto") -> Dict[str, Any]:
        """Создает новый мост для ссылки"""
        bridge_id = self.generate_bridge_id()
        bridge_hash = hashlib.md5(f"{bridge_id}{target_url}".encode()).hexdigest()[:8]
        
        # Создаем уникальный URL моста
        bridge_url = f"http://localhost:{self.port}/bridge/{bridge_id}/{bridge_hash}"
        
        # Генерируем публичную ссылку
        public_link = self._generate_public_link(bridge_id, bridge_hash)
        
        bridge_data = {
            'bridge_id': bridge_id,
            'bridge_hash': bridge_hash,
            'target_url': target_url,
            'bridge_url': bridge_url,
            'public_link': public_link,
            'bridge_type': bridge_type,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.bridge_timeout),
            'status': 'active',
            'requests_count': 0,
            'last_activity': datetime.now(),
            'redirect_count': 0
        }
        
        self.active_bridges[bridge_id] = bridge_data
        self.logger.info(f"Created bridge {bridge_id} for target {target_url}")
        
        return bridge_data
        
    def _generate_public_link(self, bridge_id: str, bridge_hash: str) -> str:
        """Генерирует публичную ссылку для моста"""
        # Создаем короткую ссылку
        short_code = base64.urlsafe_b64encode(f"{bridge_id}:{bridge_hash}".encode()).decode()[:12]
        if self.public_url:
            return f"{self.public_url}/l/{short_code}"
        else:
            return f"http://localhost:{self.port}/l/{short_code}"
        
    def validate_bridge(self, bridge_id: str, bridge_hash: str) -> bool:
        """Проверяет валидность моста"""
        if bridge_id not in self.active_bridges:
            return False
            
        bridge = self.active_bridges[bridge_id]
        if bridge['bridge_hash'] != bridge_hash:
            return False
            
        if datetime.now() > bridge['expires_at']:
            del self.active_bridges[bridge_id]
            return False
            
        bridge['last_activity'] = datetime.now()
        bridge['requests_count'] += 1
        return True
        
    def process_bridge_request(self, bridge_id: str, request_data: Dict) -> Dict[str, Any]:
        """Обрабатывает запрос через мост ссылок"""
        if bridge_id not in self.active_bridges:
            return {'error': 'Bridge not found'}
            
        bridge = self.active_bridges[bridge_id]
        if not self.validate_bridge(bridge_id, bridge['bridge_hash']):
            return {'error': 'Invalid or expired bridge'}
            
        target_url = bridge['target_url']
        
        try:
            # Подготавливаем данные для передачи
            headers = request_data.get('headers', {})
            payload = request_data.get('payload', {})
            method = request_data.get('method', 'POST')
            
            # Добавляем заголовки моста
            headers.update({
                'X-Bridge-ID': bridge_id,
                'X-Bridge-Timestamp': str(int(time.time())),
                'User-Agent': 'Link-Bridge/1.0',
                'Referer': bridge['public_link']
            })
            
            # Отправляем запрос к целевому URL
            if method.upper() == 'GET':
                response = requests.get(
                    target_url,
                    params=payload,
                    headers=headers,
                    timeout=30
                )
            else:
                response = requests.post(
                    target_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
            
            bridge['redirect_count'] += 1
            
            return {
                'status': 'success',
                'response_data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'bridge_id': bridge_id,
                'redirect_count': bridge['redirect_count']
            }
            
        except Exception as e:
            self.logger.error(f"Error processing bridge request for {bridge_id}: {e}")
            return {'error': str(e)}
            
    def start_bridge_server(self):
        """Запускает HTTP сервер моста ссылок"""
        # Создаем кастомный handler
        def handler_factory(bridge_instance):
            def create_handler(*args, **kwargs):
                return LinkBridgeHandler(*args, server=bridge_instance, **kwargs)
            return create_handler
            
        try:
            server = HTTPServer(('localhost', self.port), handler_factory(self))
            self.server = server # Сохраняем ссылку на сервер
            self.is_running = True
            self.start_time = time.time()
            
            self.logger.info(f"Link bridge server started on http://localhost:{self.port}")
            print(f"{Fore.GREEN}✓ Link bridge server started on http://localhost:{self.port}")
            
            # Настраиваем LocalTunnel
            self._setup_localtunnel()
            
            # Показываем доступ
            if self.public_url:
                print(f"{Fore.GREEN}✓ Public access: {self.public_url}")
            else:
                print(f"{Fore.YELLOW}⚠ LocalTunnel URL not captured, using localhost")
            
            # Запускаем сервер в отдельном потоке
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            
            return server
            
        except Exception as e:
            self.logger.error(f"Failed to start link bridge server: {e}")
            print(f"{Fore.RED}✗ Failed to start link bridge server: {e}")
            return None
            
    def create_bridge_script(self, bridge_data: Dict) -> str:
        """Создает клиентский скрипт для использования моста ссылок"""
        script_template = f'''
import requests
import json
import time

class LinkBridgeClient:
    def __init__(self, bridge_url, bridge_id):
        self.bridge_url = bridge_url
        self.bridge_id = bridge_id
        self.session = requests.Session()
        
    def send_request(self, method="POST", data=None, headers=None):
        """Отправляет запрос через мост ссылок"""
        payload = {{
            'method': method,
            'payload': data or {{}},
            'headers': headers or {{}},
            'timestamp': int(time.time())
        }}
        
        try:
            response = self.session.post(
                f"{{self.bridge_url}}/bridge/{{self.bridge_id}}/{{bridge_data['bridge_hash']}}",
                json=payload,
                headers={{'Content-Type': 'application/json'}}
            )
            return response.json()
        except Exception as e:
            return {{'error': str(e)}}
            
    def get_public_link(self):
        """Получает публичную ссылку"""
        return "{bridge_data['public_link']}"
        
    def get_status(self):
        """Получает статус моста"""
        try:
            response = self.session.get(f"{{self.bridge_url}}/status")
            return response.json()
        except Exception as e:
            return {{'error': str(e)}}

# Пример использования:
# client = LinkBridgeClient("{bridge_data['bridge_url']}", "{bridge_data['bridge_id']}")
# result = client.send_request("POST", {{"message": "Hello Bridge!"}})
# print(result)
# print("Public link:", client.get_public_link())
'''
        return script_template
        
    def save_bridge_info(self, bridge_data: Dict):
        """Сохраняет информацию о мосте"""
        bridge_file = self.output_dir / f"bridge_{bridge_data['bridge_id']}.json"
        
        bridge_info = {
            'bridge_data': bridge_data,
            'created_at': datetime.now().isoformat(),
            'bridge_url': f"http://localhost:{self.port}/bridge/{bridge_data['bridge_id']}/{bridge_data['bridge_hash']}",
            'instructions': [
                "1. Используйте bridge_url для прямого подключения",
                "2. Используйте public_link для публичного доступа",
                "3. Отправляйте POST запросы на /bridge/{bridge_data['bridge_id']}/{hash}",
                "4. Мост автоматически истечет через 2 часа",
                "5. Мониторьте статус через GET /status"
            ]
        }
        
        with open(bridge_file, 'w', encoding='utf-8') as f:
            json.dump(bridge_info, f, indent=2, default=str)
            
        self.logger.info(f"Bridge info saved to {bridge_file}")
        
    def cleanup_expired_bridges(self):
        """Очищает истекшие мосты"""
        current_time = datetime.now()
        expired_bridges = []
        
        for bridge_id, bridge in self.active_bridges.items():
            if current_time > bridge['expires_at']:
                expired_bridges.append(bridge_id)
                
        for bridge_id in expired_bridges:
            del self.active_bridges[bridge_id]
            self.logger.info(f"Cleaned up expired bridge {bridge_id}")
            
    def print_bridge_info(self, bridge_data: Dict):
        """Выводит информацию о созданном мосте"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                           BRIDGE CREATED SUCCESSFULLY                        ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
        
        print(f"\n{Fore.GREEN}Bridge ID: {Fore.WHITE}{bridge_data['bridge_id']}")
        print(f"{Fore.GREEN}Bridge Hash: {Fore.WHITE}{bridge_data['bridge_hash']}")
        print(f"{Fore.GREEN}Bridge URL: {Fore.WHITE}{bridge_data['bridge_url']}")
        print(f"{Fore.GREEN}Public Link: {Fore.WHITE}{bridge_data['public_link']}")
        print(f"{Fore.GREEN}Target URL: {Fore.WHITE}{bridge_data['target_url']}")
        print(f"{Fore.GREEN}Bridge Type: {Fore.WHITE}{bridge_data['bridge_type']}")
        print(f"{Fore.GREEN}Expires: {Fore.WHITE}{bridge_data['expires_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n{Fore.YELLOW}Usage Instructions:")
        print(f"{Fore.WHITE}1. Direct API: POST to {bridge_data['bridge_url']}")
        print(f"{Fore.WHITE}2. Public Access: Visit {bridge_data['public_link']}")
        print(f"{Fore.WHITE}3. Include JSON payload with 'method', 'payload', and 'headers' fields")
        print(f"{Fore.WHITE}4. Monitor bridge status at: {bridge_data['bridge_url']}/status")
        
    def run(self):
        """Основной цикл работы генератора мостов ссылок"""
        self.print_banner()
        
        # Запускаем сервер моста
        server = self.start_bridge_server()
        if not server:
            return
            
        try:
            while True:
                print(f"\n{Fore.CYAN}=== LINK BRIDGE GENERATOR CONTROL PANEL ===")
                print(f"{Fore.WHITE}1. Create new link bridge")
                print(f"{Fore.WHITE}2. List active bridges")
                print(f"{Fore.WHITE}3. Show bridge status")
                print(f"{Fore.WHITE}4. Show visitor statistics")
                print(f"{Fore.WHITE}5. Cleanup expired bridges")
                print(f"{Fore.WHITE}6. Generate bridge script")
                print(f"{Fore.WHITE}7. Test bridge connection")
                print(f"{Fore.WHITE}0. Exit")
                
                choice = input(f"\n{Fore.YELLOW}Enter your choice: ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    target_url = input(f"{Fore.CYAN}Enter target URL: ").strip()
                    if target_url:
                        bridge_type = input(f"{Fore.CYAN}Enter bridge type (auto/redirect/api): ").strip() or "auto"
                        bridge_data = self.create_link_bridge(target_url, bridge_type)
                        self.save_bridge_info(bridge_data)
                        self.print_bridge_info(bridge_data)
                    else:
                        print(f"{Fore.RED}Invalid URL!")
                        
                elif choice == "2":
                    if not self.active_bridges:
                        print(f"{Fore.YELLOW}No active bridges")
                    else:
                        print(f"\n{Fore.CYAN}Active Bridges:")
                        for bridge_id, bridge in self.active_bridges.items():
                            print(f"{Fore.GREEN}• {bridge_id} -> {bridge['target_url']}")
                            print(f"  Type: {bridge['bridge_type']}")
                            print(f"  Expires: {bridge['expires_at'].strftime('%H:%M:%S')}")
                            print(f"  Requests: {bridge['requests_count']}")
                            print(f"  Redirects: {bridge['redirect_count']}")
                            
                elif choice == "3":
                    status_data = {
                        'bridge_id': self.session_id,
                        'active_bridges': len(self.active_bridges),
                        'uptime': time.time() - self.start_time,
                        'status': 'running'
                    }
                    print(f"\n{Fore.CYAN}Bridge Status:")
                    print(f"{Fore.GREEN}• Bridge ID: {status_data['bridge_id']}")
                    print(f"{Fore.GREEN}• Active Bridges: {status_data['active_bridges']}")
                    print(f"{Fore.GREEN}• Uptime: {status_data['uptime']:.1f}s")
                    print(f"{Fore.GREEN}• Status: {status_data['status']}")
                    
                elif choice == "4":
                    # Показываем статистику посетителей
                    stats = self.get_stats_summary()
                    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
                    print(f"{Fore.CYAN}║                           VISITOR STATISTICS                                 ║")
                    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
                    
                    print(f"\n{Fore.GREEN}Total Visits: {Fore.WHITE}{stats['total_visits']}")
                    print(f"{Fore.GREEN}Unique Visitors: {Fore.WHITE}{stats['unique_visitors']}")
                    print(f"{Fore.GREEN}Active Bridges: {Fore.WHITE}{stats['active_bridges']}")
                    print(f"{Fore.GREEN}Recent Activity (Last Hour): {Fore.WHITE}{stats['recent_activity']['last_hour']}")
                    print(f"{Fore.GREEN}Today's Visits: {Fore.WHITE}{stats['recent_activity']['today']}")
                    
                    if stats['top_ips']:
                        print(f"\n{Fore.YELLOW}Top 5 IP Addresses:")
                        for i, (ip, details) in enumerate(stats['top_ips'], 1):
                            print(f"{Fore.WHITE}{i}. {ip} ({details['count']} visits)")
                            print(f"   Country: {details['country']}, City: {details['city']}")
                            print(f"   ISP: {details['isp']}")
                            print(f"   Last seen: {details['last_seen']}")
                    
                    print(f"\n{Fore.CYAN}Detailed stats saved to: {self.stats_file}")
                    
                elif choice == "5":
                    self.cleanup_expired_bridges()
                    print(f"{Fore.GREEN}Cleanup completed!")
                    
                elif choice == "6":
                    if self.active_bridges:
                        bridge_id = list(self.active_bridges.keys())[0]
                        bridge_data = self.active_bridges[bridge_id]
                        bridge_script = self.create_bridge_script(bridge_data)
                        
                        script_file = self.output_dir / f"bridge_script_{bridge_id}.py"
                        with open(script_file, 'w', encoding='utf-8') as f:
                            f.write(bridge_script)
                            
                        print(f"{Fore.GREEN}Bridge script saved to: {script_file}")
                    else:
                        print(f"{Fore.YELLOW}No active bridges to generate script for")
                        
                elif choice == "7":
                    if self.active_bridges:
                        bridge_id = list(self.active_bridges.keys())[0]
                        bridge_data = self.active_bridges[bridge_id]
                        
                        print(f"{Fore.CYAN}Testing bridge connection...")
                        test_data = {
                            'method': 'POST',
                            'payload': {'test': 'connection'},
                            'headers': {'X-Test': 'true'}
                        }
                        
                        result = self.process_bridge_request(bridge_id, test_data)
                        if 'error' in result:
                            print(f"{Fore.RED}Test failed: {result['error']}")
                        else:
                            print(f"{Fore.GREEN}Test successful! Status: {result.get('status_code', 'N/A')}")
                    else:
                        print(f"{Fore.YELLOW}No active bridges to test")
                        
                else:
                    print(f"{Fore.RED}Invalid choice!")
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Shutting down link bridge generator...")
        finally:
            self.is_running = False
            if server:
                server.shutdown()
            self._stop_ngrok() # Останавливаем Ngrok при выходе
            print(f"{Fore.GREEN}Link bridge generator stopped")

def main():
    """Главная функция"""
    try:
        generator = LinkBridgeGenerator()
        generator.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 