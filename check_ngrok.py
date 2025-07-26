#!/usr/bin/env python3
"""
Check ngrok status
"""
import requests
import subprocess
import os
import sys

def check_ngrok_installation():
    """Check if ngrok is installed"""
    print("🔍 Checking ngrok installation...")
    
    ngrok_paths = [
        "ngrok",
        "ngrok.exe",
        "C:\\ngrok\\ngrok.exe",
        "C:\\Program Files\\ngrok\\ngrok.exe",
        "C:\\Program Files (x86)\\ngrok\\ngrok.exe"
    ]
    
    for path in ngrok_paths:
        try:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                result = subprocess.run([expanded_path, 'version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ ngrok found: {expanded_path}")
                    print(f"   Version: {result.stdout.strip()}")
                    return True
        except:
            continue
    
    print("❌ ngrok not found in common locations")
    return False

def check_ngrok_running():
    """Check if ngrok is running"""
    print("\n🌐 Checking if ngrok is running...")
    
    try:
        # Check ngrok API
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            if tunnels:
                print("✅ ngrok is running!")
                for tunnel in tunnels:
                    print(f"   URL: {tunnel['public_url']}")
                    print(f"   Local: {tunnel['config']['addr']}")
                    print(f"   Protocol: {tunnel['proto']}")
                return True
            else:
                print("⚠️ ngrok is running but no tunnels found")
                return False
        else:
            print(f"❌ ngrok API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ngrok API not accessible: {e}")
        return False

def check_ngrok_dashboard():
    """Check ngrok dashboard"""
    print("\n📊 Checking ngrok dashboard...")
    
    try:
        response = requests.get('http://localhost:4040', timeout=5)
        if response.status_code == 200:
            print("✅ ngrok dashboard is accessible")
            print("   URL: http://localhost:4040")
            return True
        else:
            print(f"❌ ngrok dashboard returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ngrok dashboard not accessible: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("NGROK STATUS CHECK")
    print("=" * 50)
    
    # Check installation
    installed = check_ngrok_installation()
    
    # Check if running
    running = check_ngrok_running()
    
    # Check dashboard
    dashboard = check_ngrok_dashboard()
    
    # Summary
    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print(f"{'=' * 50}")
    print(f"Installation: {'✅ OK' if installed else '❌ NOT FOUND'}")
    print(f"Running: {'✅ YES' if running else '❌ NO'}")
    print(f"Dashboard: {'✅ ACCESSIBLE' if dashboard else '❌ NOT ACCESSIBLE'}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if not installed:
        print("   - Install ngrok: winget install ngrok")
        print("   - Or download from: https://ngrok.com/download")
    
    if not running:
        print("   - Start ngrok: ngrok http 8080")
        print("   - Make sure it's running in another terminal")
    
    if not dashboard:
        print("   - Check if ngrok is running on port 4040")
        print("   - Try accessing: http://localhost:4040")
    
    if running and dashboard:
        print("   ✅ ngrok is working correctly!")
        print("   You can now use it in ImageLogger")

if __name__ == "__main__":
    main() 