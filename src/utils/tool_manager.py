"""
QuantumKit Tool Manager
"""
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from src.config.settings import TOOL_CONFIGS, BASE_DIR
from src.utils.logger import get_logger

@dataclass
class ToolResult:
    """Result of tool execution"""
    tool_name: str
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    output: Optional[str] = None
    exit_code: Optional[int] = None

class ToolManager:
    """Manages tool execution and monitoring"""
    
    def __init__(self):
        self.logger = get_logger("tool_manager")
        self.running_tools: Dict[str, subprocess.Popen] = {}
        self.tool_results: List[ToolResult] = []
        self._lock = threading.Lock()
        self._available_tools_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 60  # Cache for 60 seconds
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available tools with caching"""
        current_time = time.time()
        
        # Return cached result if still valid
        if (self._available_tools_cache is not None and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._available_tools_cache
        
        available_tools = {}
        
        for tool_name, config in TOOL_CONFIGS.items():
            tool_path = BASE_DIR / config["path"]
            if tool_path.exists():
                available_tools[tool_name] = {
                    **config,
                    "available": True,
                    "path": str(tool_path)
                }
            else:
                available_tools[tool_name] = {
                    **config,
                    "available": False,
                    "path": str(tool_path)
                }
        
        # Update cache
        self._available_tools_cache = available_tools
        self._cache_timestamp = current_time
        
        return available_tools
    
    def get_tools_by_category(self) -> Dict[str, List[str]]:
        """Get tools grouped by category"""
        tools_by_category = {}
        available_tools = self.get_available_tools()
        
        for tool_name, config in available_tools.items():
            if config["available"]:
                category = config["category"]
                if category not in tools_by_category:
                    tools_by_category[category] = []
                tools_by_category[category].append(tool_name)
        
        return tools_by_category
    
    def run_tool(self, tool_name: str, args: Optional[List[str]] = None) -> ToolResult:
        """Run a specific tool with optimized performance"""
        if args is None:
            args = []
        
        available_tools = self.get_available_tools()
        
        if tool_name not in available_tools:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                start_time=datetime.now(),
                error_message=f"Tool '{tool_name}' not found"
            )
        
        tool_config = available_tools[tool_name]
        if not tool_config["available"]:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                start_time=datetime.now(),
                error_message=f"Tool '{tool_name}' file not found: {tool_config['path']}"
            )
        
        tool_path = Path(tool_config["path"])
        start_time = datetime.now()
        
        self.logger.info(f"Starting tool: {tool_name}")
        
        try:
            # Run the tool with optimized settings
            process = subprocess.Popen(
                ["python", "-O", str(tool_path)] + args,  # -O flag for optimization
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=BASE_DIR,
                env={**os.environ, 'PYTHONOPTIMIZE': '1'}  # Enable Python optimizations
            )
            
            # Store running process
            with self._lock:
                self.running_tools[tool_name] = process
            
            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                raise Exception("Tool execution timed out")
            
            end_time = datetime.now()
            
            # Remove from running tools
            with self._lock:
                self.running_tools.pop(tool_name, None)
            
            success = process.returncode == 0
            error_message = stderr if stderr and not success else None
            
            result = ToolResult(
                tool_name=tool_name,
                success=success,
                start_time=start_time,
                end_time=end_time,
                error_message=error_message,
                output=stdout,
                exit_code=process.returncode
            )
            
            if success:
                self.logger.success(f"Tool '{tool_name}' completed successfully")
            else:
                self.logger.failure(f"Tool '{tool_name}' failed with exit code {process.returncode}")
            
            # Store result
            self.tool_results.append(result)
            return result
            
        except Exception as e:
            end_time = datetime.now()
            self.logger.error(f"Error running tool '{tool_name}': {str(e)}")
            
            result = ToolResult(
                tool_name=tool_name,
                success=False,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e)
            )
            
            self.tool_results.append(result)
            return result
    
    def run_tool_async(self, tool_name: str, args: Optional[List[str]] = None) -> threading.Thread:
        """Run a tool asynchronously"""
        def run_async():
            self.run_tool(tool_name, args)
        
        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()
        return thread
    
    def stop_tool(self, tool_name: str) -> bool:
        """Stop a running tool"""
        with self._lock:
            if tool_name in self.running_tools:
                process = self.running_tools[tool_name]
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    self.logger.info(f"Tool '{tool_name}' stopped successfully")
                    return True
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.logger.warning(f"Force killed tool '{tool_name}'")
                    return True
                except Exception as e:
                    self.logger.error(f"Error stopping tool '{tool_name}': {str(e)}")
                    return False
            else:
                self.logger.warning(f"Tool '{tool_name}' is not running")
                return False
    
    def stop_all_tools(self):
        """Stop all running tools"""
        with self._lock:
            tool_names = list(self.running_tools.keys())
        
        for tool_name in tool_names:
            self.stop_tool(tool_name)
    
    def get_running_tools(self) -> List[str]:
        """Get list of currently running tools"""
        with self._lock:
            return list(self.running_tools.keys())
    
    def get_tool_status(self, tool_name: str) -> Optional[str]:
        """Get status of a specific tool"""
        with self._lock:
            if tool_name in self.running_tools:
                process = self.running_tools[tool_name]
                if process.poll() is None:
                    return "running"
                else:
                    return "completed"
            else:
                return "not_running"
    
    def get_tool_results(self, tool_name: Optional[str] = None) -> List[ToolResult]:
        """Get results of tool executions"""
        if tool_name:
            return [result for result in self.tool_results if result.tool_name == tool_name]
        return self.tool_results.copy()
    
    def clear_results(self):
        """Clear all tool results"""
        self.tool_results.clear()
        self.logger.info("Tool results cleared")
    
    def export_results(self, filename: str = None) -> str:
        """Export tool results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tool_results_{timestamp}.txt"
        
        output_path = BASE_DIR / "output" / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("QuantumKit Tool Results\n")
            f.write("=" * 50 + "\n\n")
            
            for result in self.tool_results:
                f.write(f"Tool: {result.tool_name}\n")
                f.write(f"Status: {'SUCCESS' if result.success else 'FAILED'}\n")
                f.write(f"Start Time: {result.start_time}\n")
                if result.end_time:
                    f.write(f"End Time: {result.end_time}\n")
                    duration = result.end_time - result.start_time
                    f.write(f"Duration: {duration}\n")
                if result.exit_code is not None:
                    f.write(f"Exit Code: {result.exit_code}\n")
                if result.error_message:
                    f.write(f"Error: {result.error_message}\n")
                if result.output:
                    f.write(f"Output: {result.output}\n")
                f.write("-" * 30 + "\n\n")
        
        self.logger.success(f"Results exported to {output_path}")
        return str(output_path)

# Global tool manager instance
tool_manager = ToolManager() 