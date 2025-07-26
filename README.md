# QuantumKit - Enhanced Toolkit

## 🚀 Overview

QuantumKit is an enhanced toolkit with improved architecture, better UI, and enhanced functionality.

## 📁 Project Structure

```
QuantumKit/
├── src/
│   ├── config/
│   │   └── settings.py          # Application settings
│   ├── utils/
│   │   ├── logger.py            # Logging system
│   │   ├── tool_manager.py      # Tool management
│   │   ├── ui.py                # UI components
│   │   └── image_logger_enhanced.py  # Enhanced ImageLogger
│   └── main.py                  # Main application
├── Tools/                       # Original tools
├── generated_images/            # ImageLogger output
├── logs/                        # Application logs
├── SETUP.bat                    # Setup script
├── START.bat                    # Launcher
└── requirements.txt             # Dependencies
```

## 🛠️ Installation

### Quick Setup
```bash
# Run the setup script
SETUP.bat

# Or manually install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Enhanced Version
```bash
# Start the enhanced version
START.bat

# Or run directly
python src/main.py
```

### Original Version
```bash
# Run the original menu
python menu.py
```

## 🔧 Features

### Enhanced ImageLogger
- **Multiple Hosting Options**: Local server, file system, custom URL, ngrok
- **Improved UI**: Better user experience with clear instructions
- **Automatic Setup**: Smart detection of ngrok and other tools
- **Error Handling**: Comprehensive error messages and recovery

### Tool Management
- **Centralized Control**: Manage all tools from one interface
- **Status Monitoring**: Track running tools and their status
- **Result Management**: View and export tool results
- **System Information**: Display system details and compatibility

## 📊 Available Tools

### Main Tools
1. **WebhookSpam** - Discord webhook spam tool
2. **Server Nuker** - Server management tool
3. **ImageLogger** - Enhanced image logger with multiple hosting options
4. **DDOS** - DDoS testing tool
5. **Discord Spam** - Discord spam utilities
6. **IP Pinger** - IP ping utility
7. **Token Checker** - Discord token validator
8. **Token Nuker** - Token management tool

### Enhanced Features
- **S. Show Tool Status** - View running tools
- **R. Show Recent Results** - View recent tool executions
- **E. Export Results** - Export results to file
- **C. Clear Results** - Clear all stored results
- **I. System Info** - Show system information

## 🔒 Security & Legal

### Important Notice
This toolkit is provided for **educational purposes only**. Users are responsible for:

- **Legal Compliance**: Ensure all activities comply with local laws
- **Ethical Use**: Use tools responsibly and ethically
- **Permission**: Only test systems you own or have explicit permission to test
- **Data Protection**: Protect any collected data appropriately

### Disclaimer
The authors are not responsible for any misuse of these tools.

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Check Python version (requires 3.7+)
python --version

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies manually
pip install colorama requests psutil
```

#### Permission Errors
```bash
# Run as administrator (Windows)
# Or use sudo (Linux/Mac)
sudo python src/main.py
```

### Getting Help
1. Check the logs in the `logs/` directory
2. Run system compatibility check: `python src/utils/system_checker.py`

## 📈 Performance

### System Requirements
- **Python**: 3.7 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space
- **Network**: Internet connection for some features

## 🔄 Updates

### Version History
- **v2.0**: Enhanced architecture and UI
- **v1.5**: Added ImageLogger improvements
- **v1.0**: Initial release

## 🤝 Contributing

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-repo/QuantumKit.git

# Install development dependencies
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for all functions

## 📞 Support

### Getting Help
- **Documentation**: Check the README and guides
- **Issues**: Report bugs on GitHub

### Contact
- **Author**: Sqrilizz
- **Project**: QuantumKit Enhanced
- **Version**: 2.0

---

**Remember**: Use responsibly and ethically! 🛡️ 