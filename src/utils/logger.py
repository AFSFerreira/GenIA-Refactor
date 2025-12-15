"""
Application logging system.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "GenIA-E2ETest", level: int = logging.INFO) -> logging.Logger:
    """
    Configures the application logger.
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # File handler (optional)
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"genia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Gets a logger for a specific module.
    
    Args:
        name: Module name
        
    Returns:
        Configured logger
    """
    return logging.getLogger(f"GenIA-E2ETest.{name}")


# Main logger configuration
main_logger = setup_logger()
