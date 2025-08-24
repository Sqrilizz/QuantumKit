# QuantumKit v6.2

**Advanced Security Toolkit** - A collection of security and network tools for professionals and researchers.

*by Sqrilizz*

---

## What is QuantumKit?

QuantumKit is a comprehensive toolkit that combines multiple security tools into one easy-to-use interface. It's designed for security researchers, penetration testers, and network administrators who need reliable tools for their work.

## Tools Included

### Discord Tools
- **Universal Discord Spammer** - Message automation tool
- **Universal Nuker** - Server management utility  

### Network & Security
- **Universal Network Tool** - Network analysis and monitoring
- **BotNet** - Bot network management
- **Brute Force** - Password cracking utility
- **Encryption Tool** - File and text encryption
- **Link Bridge Generator** - Secure link creation

### Utilities
- **Password Generator** - Create secure passwords
- **Web Scraper** - Extract data from websites
- **Telegram Report** - System reporting via Telegram

## Installation

### Requirements
- Python 3.12 or higher
- Windows/Linux/macOS

### Setup
```bash
# Download the project
git clone https://github.com/sqrilizz/QuantumKit.git
cd QuantumKit

# Install required packages
pip install -r requirements.txt

# Run the main menu
python menu.py
```

## Usage

1. **Start the toolkit:**
   ```bash
   python menu.py
   ```

2. **Navigate the menu:**
   - Use number keys to select tools
   - Press Enter to confirm
   - Use P/N for page navigation

3. **Tool categories:**
   - Discord tools (1-4)
   - Network tools (5-6) 
   - Security tools (7-9)
   - Utilities (10-11)
   - Reporting (12)

## Features

### Clean Interface
- Simple terminal-based UI
- Color-coded menus and status messages
- Progress bars for long operations
- Easy navigation between tools

### Design System
- **Color Scheme**: Magenta (primary), Blue (secondary), Green (success), Red (error), Yellow (warning), Cyan (info)
- **Icons**: Clear status indicators (✓ ✗ ⚠ ℹ)
- **Animations**: Simple spinners and progress bars
- **Layout**: Consistent borders and readable formatting

### Performance
- Fast startup and loading
- Optimized for resource usage
- Cross-platform compatibility
- Minimal dependencies

### Security
- All tools include safety checks
- Error handling and validation
- Configurable settings
- Logging for audit trails

## Configuration

### Telegram Report Setup
1. Create a bot with @BotFather
2. Get your bot token
3. Get your chat ID from @userinfobot
4. Configure in the tool settings
## File Structure

```
QuantumKit/
├── menu.py              # Main menu interface
├── src/                 # Core UI components
│   └── utils/
│       ├── ui.py        # UI functions
│       └── logo.py      # Logos and banners
├── Tools/               # All security tools
│   ├── Telegram Report.py
│   ├── Universal Discord Spammer.py
│   └── ... (other tools)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Troubleshooting

### Common Issues

**Import errors:**
```bash
pip install -r requirements.txt
```

**Permission errors:**
- Run as administrator (Windows)
- Use sudo (Linux/macOS)

**Tool not working:**
- Check Python version (3.7+)
- Verify all dependencies installed
- Check tool-specific requirements

### Getting Help

1. Check the tool's built-in help
2. Review error messages carefully
3. Ensure all requirements are met
4. Check file permissions

## Updates

### Version 6.2 Changes
- Simplified UI design
- Improved performance
- Added pagination to menu
- Updated tool categories
- Better error handling

### Previous Versions
- See CHANGELOG.md for full history

## Legal Notice

This toolkit is for educational and authorized security testing purposes only. Users are responsible for complying with all applicable laws and regulations. The authors are not liable for any misuse of these tools.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Remember:** Always use these tools responsibly and only on systems you own or have explicit permission to test. 
