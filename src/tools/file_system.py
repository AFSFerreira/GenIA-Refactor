"""
File system utilities for test case processing.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def read_test_case_file(file_path: str | Path) -> str:
    """
    Read a test case file and return its content.
    
    Args:
        file_path: Path to the test case file.
        
    Returns:
        Content of the test case file.
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
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.debug(f"Wrote JSON file: {file_path}")


def read_json_file(file_path: str | Path) -> Dict[str, Any]:
    """
    Read a JSON file and return its content.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Dictionary containing the JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    logger.debug(f"Read JSON file: {file_path}")
    return data


def write_robot_file(file_path: str | Path, content: str) -> None:
    """
    Write content to a Robot Framework file.
    
    Args:
        file_path: Path to the .robot file.
        content: Robot Framework script content.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Wrote Robot Framework file: {file_path}")


def map_extracted_data_to_steps(module: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map extracted HTML elements to their corresponding execution steps.
    
    This function takes extracted elements (which contain step_name field)
    and assigns them to the appropriate execution_step based on matching
    step names.
    
    Args:
        module: Module dictionary containing extracted_data and execution_steps.
        
    Returns:
        Module dictionary with extracted_data mapped to steps.
    """
    extracted_items = module.get("extracted_data", [])
    matched_indices = set()

    for step in module.get("execution_steps", []):
        matched_data = []
        for idx, data in enumerate(extracted_items):
            if data.get("step_name") == step.get("step"):
                matched_data.append({
                    "type": data["type"],
                    "request_description": data["request_description"],
                    "identifier_type": data["identifier_type"],
                    "identifier_tracking": data["identifier_tracking"]
                })
                matched_indices.add(idx)
        if matched_data:
            step["extracted_data"] = matched_data

    # Remove extracted_data from module level if all items were matched
    if len(matched_indices) == len(extracted_items):
        module.pop("extracted_data", None)

    logger.debug(f"Mapped {len(matched_indices)} extracted elements to steps")
    return module
