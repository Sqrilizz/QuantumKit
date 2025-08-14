"""
QuantumKit Configuration Settings
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
TOOLS_DIR = BASE_DIR / "Tools"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
GENERATED_IMAGES_DIR = BASE_DIR / "generated_images"

# Create directories if they don't exist
for directory in [OUTPUT_DIR, LOGS_DIR, GENERATED_IMAGES_DIR]:
    directory.mkdir(exist_ok=True)

# Application settings
APP_NAME = "QuantumKit"
APP_VERSION = "6.1"
APP_AUTHOR = "Sqrilizz"

# Console colors
COLORS = {
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'WHITE': '\033[97m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

# Tool configurations
TOOL_CONFIGS = {
    "WebhookSpam": {
        "path": "Tools/WebhookSpam.py",
        "description": "Advanced Discord webhook spammer",
        "category": "Discord"
    },
    "Server Nuker": {
        "path": "Tools/Server Nuker.py",
        "description": "Discord server nuker tool",
        "category": "Discord"
    },
    "ImageLogger": {
        "path": "src/utils/image_logger_enhanced.py",
        "description": "Enhanced image logger with multiple hosting options",
        "category": "Discord"
    },
    "Universal Image Logger": {
        "path": "Tools/Universal Image Logger.py",
        "description": "All-in-one image logger combining Local and Pro functionality",
        "category": "Discord"
    },
    "Universal Token Spammer": {
        "path": "Tools/Universal Token Spammer.py",
        "description": "Universal token spammer - single channel or mass server spam",
        "category": "Discord"
    },
    "DDOS": {
        "path": "Tools/DDOS.py",
        "description": "DDoS attack tool",
        "category": "Network"
    },
    "Discord Spam": {
        "path": "Tools/Discord Spam/DiscordSpam.py",
        "description": "Discord spam tool",
        "category": "Discord"
    },

    "IP Pinger": {
        "path": "Tools/IP Pinger.py",
        "description": "IP ping tool",
        "category": "Network"
    },
    "Token Checker": {
        "path": "Tools/Token Checker.py",
        "description": "Discord token checker",
        "category": "Discord"
    },
    "Token Nuker": {
        "path": "Tools/Token Nuker.py",
        "description": "Discord token nuker",
        "category": "Discord"
    },
    "Password Generator": {
        "path": "Tools/Password Generator.py",
        "description": "Password generator tool",
        "category": "Utility"
    },
    "Brute Force": {
        "path": "Tools/Brute Force.py",
        "description": "Brute force tool",
        "category": "Security"
    },
    "QR Generator": {
        "path": "Tools/QR Generator.py",
        "description": "Advanced QR code generator with multiple options",
        "category": "Utility"
    },
    "Encryption Tool": {
        "path": "Tools/Encryption Tool.py",
        "description": "Advanced encryption and decryption tool",
        "category": "Security"
    },
    "Web Scraper": {
        "path": "Tools/Web Scraper.py",
        "description": "Advanced web scraping tool with multiple features",
        "category": "Utility"
    },
    "Clipboard Manager": {
        "path": "Tools/Clipboard Manager.py",
        "description": "Advanced clipboard management with history and formatting",
        "category": "Utility"
    },
    "Trojan Image Generator": {
        "path": "Tools/Trojan Image Generator.py",
        "description": "Create trojan images that collect system information when opened",
        "category": "Discord"
    },
    "Censored Image Logger": {
        "path": "Tools/Censored Image Logger.py",
        "description": "Create censored images that collect data when clicked to reveal",
        "category": "Discord"
    },
    "SMALL Report": {
        "path": "Tools/SMALL Report.py",
        "description": "Advanced Telegram reporting tool with modern UI",
        "category": "Reporting"
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'quantumkit.log',
            'level': 'INFO'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO'
        }
    },
    'loggers': {
        'quantumkit': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Default settings
DEFAULT_SETTINGS = {
    'max_retries': 3,
    'timeout': 30,
    'delay_between_requests': 0.1,
    'max_concurrent_requests': 10,
    'enable_proxies': True,
    'proxy_file': 'Tools/proxies.txt'
} 