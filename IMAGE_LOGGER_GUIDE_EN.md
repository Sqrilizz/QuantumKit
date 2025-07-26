# Enhanced ImageLogger Guide

A comprehensive guide for the enhanced ImageLogger with multiple hosting options and improved functionality.

## 🚀 Overview

The Enhanced ImageLogger is a powerful tool that creates malicious image files to capture user data. It now supports multiple hosting options, making it more versatile and user-friendly.

## ✨ Features

### Hosting Options
- **Local HTTP Server** - Host files locally with automatic server setup
- **ngrok Tunnel** - Secure tunneling with automatic URL detection
- **Custom URL** - Use any external hosting service
- **Manual Setup** - Complete control over hosting configuration

### Enhanced Functionality
- **Automatic Server Management** - Start/stop local servers automatically
- **URL Validation** - Verify hosting URLs before use
- **Multiple File Types** - Support for HTML and image files
- **Batch File Generation** - Automatic shortcut creation
- **Error Handling** - Robust error management and recovery

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Required packages: `requests`, `colorama`
- Optional: `ngrok` for tunneling

### Setup
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. For ngrok support, install ngrok and add to PATH

## 📖 Usage

### Running the Enhanced ImageLogger

1. **Launch the application**:
   ```bash
   python src/main.py
   ```

2. **Select ImageLogger** from the main menu

3. **Choose hosting option**:
   - Local Server (recommended for testing)
   - ngrok Tunnel (for external access)
   - Custom URL (for existing hosting)

### Hosting Options Guide

#### 1. Local HTTP Server
- **Best for**: Testing and local development
- **Setup**: Automatic
- **Access**: `http://localhost:8000`
- **Features**:
  - Automatic server startup
  - File serving from `generated_images/`
  - Easy testing environment

#### 2. ngrok Tunnel
- **Best for**: External access without hosting
- **Setup**: Automatic detection or manual
- **Access**: `https://your-ngrok-url.ngrok.io`
- **Features**:
  - Secure HTTPS tunneling
  - Automatic URL detection
  - Real-time access logs

#### 3. Custom URL
- **Best for**: Existing hosting services
- **Setup**: Manual URL input
- **Access**: Your provided URL
- **Features**:
  - Use any hosting service
  - URL validation
  - Accessibility testing

## 🔧 Configuration

### File Generation
- **Output Directory**: `generated_images/`
- **File Types**: HTML, PNG, JPG
- **Naming**: Random strings for security
- **Batch Files**: Automatic shortcut creation

### Server Settings
- **Local Port**: 8000 (configurable)
- **Timeout**: 30 seconds
- **Max Requests**: Unlimited
- **Logging**: Console and file

## 📁 File Structure

```
generated_images/
├── image_XXXXX.html          # Main image file
├── open_image_XXXXX.html.bat # Shortcut batch file
├── image_XXXXX.png           # Image file (if applicable)
└── open_image_XXXXX.png.bat  # Image shortcut
```

## 🎯 Step-by-Step Usage

### Step 1: Launch and Configure
1. Start the application
2. Select "ImageLogger"
3. Choose your hosting preference

### Step 2: Generate Files
1. Enter image name/description
2. Select file type (HTML/Image)
3. Wait for file generation

### Step 3: Setup Hosting
1. **Local Server**: Server starts automatically
2. **ngrok**: Tunnel creates automatically
3. **Custom URL**: Enter and validate URL

### Step 4: Distribute
1. Share the generated URL
2. Monitor access in console
3. Check logs for activity

## 🔍 Monitoring and Logs

### Console Output
- Real-time server status
- Access logs
- Error messages
- Success confirmations

### File Logs
- Location: `logs/quantumkit.log`
- Format: Timestamp + Level + Message
- Content: All operations and errors

## 🛡️ Security Considerations

### Best Practices
- Use HTTPS when possible
- Validate all URLs
- Monitor access logs
- Secure your hosting environment

### Legal Compliance
- **Educational use only**
- Respect privacy laws
- Follow hosting terms of service
- Use responsibly

## 🐛 Troubleshooting

### Common Issues

#### 1. Local Server Not Starting
- **Problem**: Port 8000 in use
- **Solution**: Change port in settings or kill existing process

#### 2. ngrok Not Detected
- **Problem**: ngrok not in PATH
- **Solution**: Install ngrok or provide manual URL

#### 3. Custom URL Not Accessible
- **Problem**: URL validation fails
- **Solution**: Check URL format and accessibility

#### 4. File Generation Errors
- **Problem**: Permission or disk space
- **Solution**: Check directory permissions and disk space

### Debug Tools
- Use `check_ngrok.py` for ngrok diagnostics
- Check logs in `logs/` directory
- Verify file permissions

## 📊 Advanced Features

### Custom Hosting Services
Supported services for custom URLs:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting

### File Customization
- Custom HTML templates
- Image manipulation
- Metadata injection
- Tracking integration

### Automation
- Batch processing
- Scheduled generation
- API integration
- Webhook notifications

## 🔄 Updates and Maintenance

### Version History
- **v5.1**: Enhanced hosting options
- **v5.0**: Major refactor and improvements
- **v4.x**: Original functionality

### Future Enhancements
- More hosting providers
- Advanced file types
- Better monitoring
- API improvements

## 📞 Support

### Getting Help
1. Check this guide first
2. Review error logs
3. Test with different hosting options
4. Verify system requirements

### Reporting Issues
- Include error messages
- Provide system information
- Describe steps to reproduce
- Attach relevant logs

---

**Remember: This tool is for educational purposes only. Use responsibly and legally.** 