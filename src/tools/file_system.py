"""
File system utilities for test case processing.
"""
import json
from pathlib import Path
from typing import Any, Dict

from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_directory_if_not_exists(path: str | Path) -> None:
    """
    Create a directory if it does not exist.
    
    Args:
        path: Path to the directory to create.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directory ensured: {path}")
    

def write_file(file_path: str | Path, content: str) -> None:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file.
        content: File content.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
        
    logger.info(f"Wrote file content: {file_path}")


def read_file(file_path: str | Path) -> str:
    """
    Read a file and return its content.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        Content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    logger.debug(f"Read test case file: {file_path}")
    
    return content


def write_json_file(file_path: str | Path, data: Dict[str, Any]) -> None:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        data: Dictionary to write as JSON.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
    logger.debug(f"Wrote JSON file: {file_path}")
    
    return


def read_json_file(file_path: str | Path) -> Dict[str, Any]:
    """
    Read a JSON file and return its content.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Dictionary containing the JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    logger.debug(f"Read JSON file: {file_path}")
    
    return data

