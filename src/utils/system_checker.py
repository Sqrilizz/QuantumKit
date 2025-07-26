"""
QuantumKit System Checker
"""
import sys
import os
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

from src.config.settings import BASE_DIR, TOOL_CONFIGS
from src.utils.logger import get_logger

class SystemChecker:
    """System compatibility and dependency checker"""
    
    def __init__(self):
        self.logger = get_logger("system_checker")
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.recommendations: List[str] = []
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        current_version = sys.version_info
        required_version = (3, 7)
        
        if current_version < required_version:
            self.issues.append(
                f"Python {required_version[0]}.{required_version[1]}+ required, "
                f"found {current_version[0]}.{current_version[1]}"
            )
            return False
        
        self.logger.info(f"Python version: {current_version[0]}.{current_version[1]}")
        return True
    
    def check_platform(self) -> bool:
        """Check platform compatibility"""
        system = platform.system()
        if system != "Windows":
            self.warnings.append(f"Tested on Windows, current platform: {system}")
            return False
        
        self.logger.info(f"Platform: {system} {platform.release()}")
        return True
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check required dependencies"""
        dependencies = {
            'colorama': 'Color support for console',
            'requests': 'HTTP requests',
            'discord': 'Discord API integration',
            'aiohttp': 'Async HTTP client',
            'psutil': 'System information',
            'paramiko': 'SSH/SFTP support'
        }
        
        results = {}
        
        for module, description in dependencies.items():
            try:
                __import__(module)
                results[module] = True
                self.logger.info(f"✓ {module}: {description}")
            except ImportError:
                results[module] = False
                self.issues.append(f"Missing dependency: {module} ({description})")
                self.logger.error(f"✗ {module}: {description} - NOT FOUND")
        
        return results
    
    def check_tools_directory(self) -> bool:
        """Check if tools directory exists and contains tools"""
        tools_dir = BASE_DIR / "Tools"
        
        if not tools_dir.exists():
            self.issues.append("Tools directory not found")
            return False
        
        # Check for tool files
        tool_files = list(tools_dir.glob("*.py"))
        if not tool_files:
            self.warnings.append("No Python tool files found in Tools directory")
            return False
        
        self.logger.info(f"Found {len(tool_files)} tool files")
        return True
    
    def check_tool_configurations(self) -> Dict[str, bool]:
        """Check if configured tools exist"""
        results = {}
        
        for tool_name, config in TOOL_CONFIGS.items():
            tool_path = BASE_DIR / config["path"]
            exists = tool_path.exists()
            results[tool_name] = exists
            
            if exists:
                self.logger.info(f"✓ {tool_name}: {config['description']}")
            else:
                self.warnings.append(f"Tool file not found: {tool_name} ({config['path']})")
                self.logger.warning(f"✗ {tool_name}: {config['description']} - FILE NOT FOUND")
        
        return results
    
    def check_directories(self) -> bool:
        """Check and create necessary directories"""
        required_dirs = [
            BASE_DIR / "output",
            BASE_DIR / "logs",
            BASE_DIR / "generated_images"
        ]
        
        for directory in required_dirs:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created directory: {directory}")
                except Exception as e:
                    self.issues.append(f"Cannot create directory {directory}: {e}")
                    return False
        
        return True
    
    def check_permissions(self) -> bool:
        """Check file and directory permissions"""
        test_file = BASE_DIR / "output" / "test.txt"
        
        try:
            # Test write permission
            with open(test_file, 'w') as f:
                f.write("test")
            
            # Test read permission
            with open(test_file, 'r') as f:
                f.read()
            
            # Clean up
            test_file.unlink()
            
            self.logger.info("File permissions: OK")
            return True
            
        except Exception as e:
            self.issues.append(f"Permission error: {e}")
            return False
    
    def check_network_connectivity(self) -> bool:
        """Check basic network connectivity"""
        try:
            import requests
            response = requests.get("https://httpbin.org/get", timeout=5)
            if response.status_code == 200:
                self.logger.info("Network connectivity: OK")
                return True
        except Exception as e:
            self.warnings.append(f"Network connectivity issue: {e}")
            return False
    
    def check_system_resources(self) -> Dict[str, str]:
        """Check system resources"""
        try:
            import psutil
            
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                'cpu_cores': str(cpu_count),
                'memory_total': f"{memory.total // (1024**3)} GB",
                'memory_available': f"{memory.available // (1024**3)} GB",
                'disk_free': f"{disk.free // (1024**3)} GB"
            }
            
            # Check if resources are sufficient
            if cpu_count < 2:
                self.warnings.append("Low CPU cores detected")
            
            if memory.total < 4 * 1024**3:  # 4 GB
                self.warnings.append("Low memory detected")
            
            if disk.free < 1 * 1024**3:  # 1 GB
                self.warnings.append("Low disk space detected")
            
            self.logger.info(f"System resources: {resources}")
            return resources
            
        except ImportError:
            self.warnings.append("psutil not available, cannot check system resources")
            return {}
    
    def run_full_check(self) -> Dict[str, any]:
        """Run complete system check"""
        self.logger.info("Starting system compatibility check...")
        
        results = {
            'python_version': self.check_python_version(),
            'platform': self.check_platform(),
            'dependencies': self.check_dependencies(),
            'tools_directory': self.check_tools_directory(),
            'tool_configurations': self.check_tool_configurations(),
            'directories': self.check_directories(),
            'permissions': self.check_permissions(),
            'network': self.check_network_connectivity(),
            'resources': self.check_system_resources(),
            'issues': self.issues,
            'warnings': self.warnings,
            'recommendations': self.recommendations
        }
        
        # Generate recommendations
        self._generate_recommendations(results)
        
        # Log summary
        self._log_summary(results)
        
        return results
    
    def _generate_recommendations(self, results: Dict[str, any]):
        """Generate recommendations based on check results"""
        if not results['python_version']:
            self.recommendations.append("Install Python 3.7 or higher")
        
        missing_deps = [dep for dep, available in results['dependencies'].items() if not available]
        if missing_deps:
            self.recommendations.append(f"Install missing dependencies: {', '.join(missing_deps)}")
        
        if not results['tools_directory']:
            self.recommendations.append("Ensure Tools directory exists with tool files")
        
        if results['warnings']:
            self.recommendations.append("Review warnings for potential issues")
        
        if not results['network']:
            self.recommendations.append("Check network connectivity for online features")
    
    def _log_summary(self, results: Dict[str, any]):
        """Log check summary"""
        total_issues = len(results['issues'])
        total_warnings = len(results['warnings'])
        
        if total_issues == 0 and total_warnings == 0:
            self.logger.success("System check completed successfully!")
        else:
            self.logger.warning(f"System check completed with {total_issues} issues and {total_warnings} warnings")
        
        if results['issues']:
            self.logger.error("Issues found:")
            for issue in results['issues']:
                self.logger.error(f"  - {issue}")
        
        if results['warnings']:
            self.logger.warning("Warnings:")
            for warning in results['warnings']:
                self.logger.warning(f"  - {warning}")
        
        if results['recommendations']:
            self.logger.info("Recommendations:")
            for rec in results['recommendations']:
                self.logger.info(f"  - {rec}")
    
    def is_system_compatible(self) -> bool:
        """Check if system is compatible for running QuantumKit"""
        results = self.run_full_check()
        return len(results['issues']) == 0

def main():
    """Main function for standalone system check"""
    checker = SystemChecker()
    results = checker.run_full_check()
    
    print("\n" + "="*50)
    print("QUANTUMKIT SYSTEM CHECK RESULTS")
    print("="*50)
    
    if results['issues']:
        print(f"\n❌ {len(results['issues'])} Issues Found:")
        for issue in results['issues']:
            print(f"  - {issue}")
    
    if results['warnings']:
        print(f"\n⚠️  {len(results['warnings'])} Warnings:")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    if results['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  - {rec}")
    
    if not results['issues'] and not results['warnings']:
        print("\n✅ System is fully compatible!")
    elif not results['issues']:
        print("\n⚠️  System is compatible with warnings")
    else:
        print("\n❌ System has compatibility issues")
    
    return len(results['issues']) == 0

if __name__ == "__main__":
    main() 