"""
QuantumKit Main Application
Enhanced version with improved architecture
"""
import os
import sys
import time
import signal
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_NAME, APP_VERSION, APP_AUTHOR, BASE_DIR
from src.utils.logger import get_logger
from src.utils.tool_manager import tool_manager
from src.utils.ui import Menu, print_status, print_header, confirm_action, Spinner
from colorama import Fore

class QuantumKit:
    """Main QuantumKit application class"""
    
    def __init__(self):
        self.logger = get_logger("main")
        self.running = True
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info("Received shutdown signal")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def startup(self):
        """Application startup sequence"""
        self.logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        
        # Check Python version
        if sys.version_info < (3, 7):
            self.logger.error("Python 3.7 or higher is required")
            return False
        
        # Check if tools directory exists
        if not (BASE_DIR / "Tools").exists():
            self.logger.error("Tools directory not found")
            return False
        
        # Load proxies
        self.load_proxies()
        
        self.logger.success(f"{APP_NAME} initialized successfully")
        return True
    
    def load_proxies(self):
        """Load proxy configuration"""
        proxy_file = BASE_DIR / "Tools" / "proxies.txt"
        if proxy_file.exists():
            try:
                with open(proxy_file, 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                self.logger.info(f"Loaded {len(proxies)} proxies")
            except Exception as e:
                self.logger.warning(f"Failed to load proxies: {e}")
        else:
            self.logger.info("No proxy file found, continuing without proxies")
    
    def show_main_menu(self):
        """Display main menu"""
        menu = Menu("QuantumKit Main Menu")
        
        # Get available tools by category
        tools_by_category = tool_manager.get_tools_by_category()
        
        # Add tool options by category
        option_number = 1
        for category, tools in tools_by_category.items():
            for tool in tools:
                menu.add_option(
                    str(option_number),
                    tool,
                    lambda t=tool: self.run_tool(t),
                    f"Category: {category}"
                )
                option_number += 1
        
        # Add utility options
        menu.add_option("S", "Show Tool Status", self.show_tool_status, "View running tools")
        menu.add_option("R", "Show Recent Results", self.show_recent_results, "View recent tool executions")
        menu.add_option("E", "Export Results", self.export_results, "Export results to file")
        menu.add_option("C", "Clear Results", self.clear_results, "Clear all stored results")
        menu.add_option("I", "System Info", self.show_system_info, "Show system information")
        
        menu.display()
    
    def run_tool(self, tool_name: str):
        """Run a specific tool"""
        print_header(f"Running {tool_name}")
        
        # Check if tool is already running
        if tool_name in tool_manager.get_running_tools():
            print_status(f"{tool_name} is already running", "warning")
            if not confirm_action(f"Stop running {tool_name}?"):
                return
            tool_manager.stop_tool(tool_name)
        
        # Run the tool
        spinner = Spinner(f"Starting {tool_name}...")
        spinner.start()
        
        try:
            result = tool_manager.run_tool(tool_name)
            spinner.stop()
            
            if result.success:
                print_status(f"{tool_name} completed successfully", "success")
            else:
                print_status(f"{tool_name} failed: {result.error_message}", "error")
                
        except KeyboardInterrupt:
            spinner.stop()
            print_status(f"{tool_name} interrupted by user", "warning")
            tool_manager.stop_tool(tool_name)
        except Exception as e:
            spinner.stop()
            print_status(f"Error running {tool_name}: {str(e)}", "error")
    
    def show_tool_status(self):
        """Show status of running tools"""
        print_header("Tool Status")
        
        running_tools = tool_manager.get_running_tools()
        
        if not running_tools:
            print_status("No tools are currently running", "info")
            return
        
        # Simple table display without external Table class
        print(f"{Fore.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│{Fore.WHITE} Tool Name{' ' * 20} │ Status{' ' * 10} │ PID{' ' * 8} {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────┤")
        
        for tool_name in running_tools:
            status = tool_manager.get_tool_status(tool_name)
            print(f"{Fore.CYAN}│{Fore.WHITE} {tool_name:<30} │ {status:<16} │ N/A{' ' * 8} {Fore.CYAN}│")
        
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────┘")
        
        for tool_name in running_tools:
            status = tool_manager.get_tool_status(tool_name)
            # Note: PID is not directly available, but could be added to ToolManager
            table.add_row([tool_name, status, "N/A"])
        
        table.display()
        
        if confirm_action("Stop all running tools?"):
            tool_manager.stop_all_tools()
            print_status("All tools stopped", "success")
    
    def show_recent_results(self):
        """Show recent tool execution results"""
        print_header("Recent Tool Results")
        
        results = tool_manager.get_tool_results()
        
        if not results:
            print_status("No results available", "info")
            return
        
        # Simple table display without external Table class
        print(f"{Fore.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│{Fore.WHITE} Tool{' ' * 20} │ Status{' ' * 10} │ Start Time{' ' * 8} │ Duration{' ' * 8} {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────┤")
        
        # Show last 10 results
        for result in results[-10:]:
            status = "SUCCESS" if result.success else "FAILED"
            start_time = result.start_time.strftime("%H:%M:%S")
            
            if result.end_time:
                duration = result.end_time - result.start_time
                duration_str = f"{duration.total_seconds():.1f}s"
            else:
                duration_str = "N/A"
            
            print(f"{Fore.CYAN}│{Fore.WHITE} {result.tool_name:<22} │ {status:<16} │ {start_time:<18} │ {duration_str:<16} {Fore.CYAN}│")
        
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────┘")
    
    def export_results(self):
        """Export results to file"""
        print_header("Export Results")
        
        results = tool_manager.get_tool_results()
        
        if not results:
            print_status("No results to export", "warning")
            return
        
        filename = input("Enter filename (or press Enter for default): ").strip()
        if not filename:
            filename = None
        
        try:
            exported_file = tool_manager.export_results(filename)
            print_status(f"Results exported to: {exported_file}", "success")
        except Exception as e:
            print_status(f"Failed to export results: {str(e)}", "error")
    
    def clear_results(self):
        """Clear all stored results"""
        print_header("Clear Results")
        
        if confirm_action("Are you sure you want to clear all results?"):
            tool_manager.clear_results()
            print_status("All results cleared", "success")
    
    def show_system_info(self):
        """Show system information"""
        print_header("System Information")
        
        import platform
        
        info = [
            ("Application", f"{APP_NAME} v{APP_VERSION}"),
            ("Author", APP_AUTHOR),
            ("Python Version", platform.python_version()),
            ("Platform", platform.platform()),
        ]
        
        # Try to get system resources if psutil is available
        try:
            import psutil
            info.extend([
                ("CPU Cores", str(psutil.cpu_count())),
                ("Memory", f"{psutil.virtual_memory().total // (1024**3)} GB"),
            ])
        except ImportError:
            info.append(("System Resources", "psutil not available"))
        
        info.extend([
            ("Available Tools", str(len(tool_manager.get_available_tools()))),
            ("Running Tools", str(len(tool_manager.get_running_tools())))
        ])
        
        # Simple table display without external Table class
        print(f"{Fore.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│{Fore.WHITE} Property{' ' * 20} │ Value{' ' * 35} {Fore.CYAN}│")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────┤")
        
        for property_name, value in info:
            print(f"{Fore.CYAN}│{Fore.WHITE} {property_name:<30} │ {value:<43} {Fore.CYAN}│")
        
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────┘")
    
    def shutdown(self):
        """Application shutdown sequence"""
        self.logger.info("Shutting down QuantumKit...")
        
        # Stop all running tools
        running_tools = tool_manager.get_running_tools()
        if running_tools:
            self.logger.info(f"Stopping {len(running_tools)} running tools...")
            tool_manager.stop_all_tools()
        
        self.running = False
        self.logger.success("QuantumKit shutdown complete")

def main():
    """Main entry point"""
    app = QuantumKit()
    
    try:
        if app.startup():
            app.show_main_menu()
    except KeyboardInterrupt:
        print("\n")
        app.logger.info("Application interrupted by user")
    except Exception as e:
        app.logger.critical(f"Fatal error: {str(e)}")
    finally:
        app.shutdown()

if __name__ == "__main__":
    main() 