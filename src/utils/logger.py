"""
QuantumKit Logger System
"""
import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from colorama import init, Fore, Style
from src.config.settings import LOGGING_CONFIG, LOGS_DIR

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        
        # Add timestamp with color
        timestamp = f"{Fore.CYAN}{datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}"
        record.msg = f"[{timestamp}] {record.msg}"
        
        return super().format(record)

class QuantumKitLogger:
    """Main logger class for QuantumKit"""
    
    def __init__(self, name: str = "quantumkit"):
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with file and console handlers"""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        colored_formatter = ColoredFormatter('%(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(LOGS_DIR / 'quantumkit.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(colored_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def success(self, message: str):
        """Log success message (custom level)"""
        colored_message = f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}"
        self.logger.info(colored_message)
    
    def failure(self, message: str):
        """Log failure message (custom level)"""
        colored_message = f"{Fore.RED}✗ {message}{Style.RESET_ALL}"
        self.logger.error(colored_message)

# Global logger instance
logger = QuantumKitLogger()

def get_logger(name: str = "quantumkit") -> QuantumKitLogger:
    """Get logger instance"""
    return QuantumKitLogger(name) 