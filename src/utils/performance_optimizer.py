"""
Performance Optimizer for QuantumKit
Additional optimizations for faster execution
"""
import os
import sys
import gc
import threading
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
import psutil

class PerformanceOptimizer:
    """Performance optimization utilities"""
    
    def __init__(self):
        self.original_settings = {}
        self.optimizations_applied = False
    
    def apply_system_optimizations(self):
        """Apply system-level optimizations"""
        if self.optimizations_applied:
            return
        
        try:
            # Increase file descriptor limits on Unix systems
            if hasattr(os, 'setrlimit'):
                import resource
                soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
                resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
            
            # Set environment variables for better performance
            os.environ['PYTHONOPTIMIZE'] = '1'
            os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
            os.environ['PYTHONUNBUFFERED'] = '1'
            
            # Disable garbage collection during intensive operations
            gc.disable()
            
            self.optimizations_applied = True
            
        except Exception as e:
            print(f"Warning: Could not apply all system optimizations: {e}")
    
    def restore_system_settings(self):
        """Restore original system settings"""
        if not self.optimizations_applied:
            return
        
        try:
            # Re-enable garbage collection
            gc.enable()
            
            # Restore environment variables
            for key, value in self.original_settings.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            
            self.optimizations_applied = False
            
        except Exception as e:
            print(f"Warning: Could not restore all system settings: {e}")
    
    def optimize_memory_usage(self):
        """Optimize memory usage"""
        try:
            # Force garbage collection
            gc.collect()
            
            # Clear Python's internal caches
            if hasattr(sys, 'intern'):
                sys.intern.clear()
            
            # Clear module cache if possible
            if hasattr(sys, '_clear_type_cache'):
                sys._clear_type_cache()
            
        except Exception as e:
            print(f"Warning: Could not optimize memory usage: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system performance information"""
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_count': cpu_count,
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_free': disk.free,
                'disk_percent': (disk.used / disk.total) * 100
            }
        except ImportError:
            return {'error': 'psutil not available'}
        except Exception as e:
            return {'error': str(e)}
    
    def optimize_thread_pool(self, max_workers: int = None) -> int:
        """Optimize thread pool size based on system resources"""
        try:
            if max_workers is None:
                cpu_count = psutil.cpu_count()
                # Use 2x CPU cores for I/O bound operations
                max_workers = min(cpu_count * 2, 20)
            
            return max_workers
        except ImportError:
            return 10  # Default fallback
        except Exception:
            return 10  # Default fallback
    
    def create_optimized_executor(self, max_workers: int = None):
        """Create an optimized ThreadPoolExecutor"""
        optimal_workers = self.optimize_thread_pool(max_workers)
        return ThreadPoolExecutor(max_workers=optimal_workers)

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer() 