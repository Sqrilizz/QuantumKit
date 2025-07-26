# QuantumKit - Advanced Discord Toolkit

A comprehensive toolkit for Discord-related operations with enhanced features and modular architecture.

## 🚀 Features

### Core Features
- **Enhanced ImageLogger** - Multiple hosting options (local server, ngrok, custom URL)
- **Webhook Management** - Spam and management tools
- **Token Operations** - Checker, nuker, and generator
- **Network Tools** - DDoS, IP pinger, server nuker
- **Security Tools** - Password generator, brute force
- **Discord Spam** - Advanced spam functionality

### Technical Features
- **Modular Architecture** - Clean, organized code structure
- **Enhanced Logging** - Colored console output with file logging
- **Error Handling** - Robust error management and recovery
- **Tool Management** - Track running tools and results
- **System Integration** - Compatibility checks and system info

## 📁 Project Structure

```
QuantumKit/
├── src/
│   ├── config/
│   │   └── settings.py          # Application configuration
│   ├── utils/
│   │   ├── logger.py            # Enhanced logging system
│   │   ├── ui.py                # User interface components
│   │   ├── tool_manager.py      # Tool execution management
│   │   └── image_logger_enhanced.py  # Enhanced ImageLogger
│   └── main.py                  # Main application entry point
├── Tools/                       # Individual tool scripts
├── generated_images/            # ImageLogger output directory
├── logs/                        # Application logs
├── SETUP.bat                    # Automated setup script
├── START.bat                    # Application launcher
└── requirements.txt             # Python dependencies
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (primary support)

### Quick Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/QuantumKit.git
   cd QuantumKit
   ```

2. Run the automated setup:
   ```bash
   SETUP.bat
   ```

3. Launch the application:
   ```bash
   START.bat
   ```

### Manual Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main application:
   ```bash
   python src/main.py
   ```

## 🎯 Usage

### Enhanced Version (Recommended)
- Launch with `START.bat` and select "Enhanced Version"
- Features improved UI, logging, and tool management
- Better error handling and system integration

### Original Version
- Launch with `START.bat` and select "Original Version"
- Classic interface for backward compatibility

### ImageLogger Guide
See `IMAGE_LOGGER_GUIDE.md` for detailed ImageLogger usage instructions.

## 🔧 Configuration

### Settings
Main configuration is in `src/config/settings.py`:
- Tool paths and descriptions
- Logging configuration
- Default settings
- Color schemes

### Logging
- Console output with colors
- File logging in `logs/` directory
- Configurable log levels

## 🛡️ Security & Legal

**⚠️ DISCLAIMER: This tool is for educational purposes only. Users are responsible for complying with all applicable laws and terms of service.**

### Security Features
- Input validation
- Error handling
- Safe file operations
- Network request validation

## 📊 Features Overview

| Feature | Description | Category |
|---------|-------------|----------|
| ImageLogger | Enhanced with multiple hosting options | Discord |
| WebhookSpam | Webhook management and spam | Discord |
| Token Checker | Discord token validation | Discord |
| Token Nuker | Account management tool | Discord |
| DDOS | Network stress testing | Network |
| IP Pinger | Network connectivity testing | Network |
| Server Nuker | Server management tool | Network |
| Password Generator | Secure password creation | Security |
| Brute Force | Password cracking tool | Security |

## 🔄 Recent Updates

### Version 5.1 - Enhanced ImageLogger
- Multiple hosting options (local, ngrok, custom URL)
- Improved error handling
- Better user experience
- Removed personal hosting dependency

### Version 5.0 - Major Refactor
- Modular architecture
- Enhanced logging system
- Improved UI components
- Better tool management

## 🐛 Troubleshooting

### Common Issues
1. **Python not found**: Ensure Python is installed and in PATH
2. **Missing dependencies**: Run `SETUP.bat` or `pip install -r requirements.txt`
3. **Permission errors**: Run as administrator if needed
4. **ngrok issues**: See `check_ngrok.py` for diagnostics

### Getting Help
- Check the logs in `logs/` directory
- Review error messages in console
- Ensure all dependencies are installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Users must comply with all applicable laws and terms of service.

## ⚠️ Legal Notice

This software is provided "as is" without warranty. Users are responsible for ensuring their use complies with applicable laws and terms of service. The authors are not responsible for any misuse of this software.

---

**For educational purposes only. Use responsibly and legally.** 