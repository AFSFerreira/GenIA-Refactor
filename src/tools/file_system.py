"""
Tools for file system manipulation.
"""
from pathlib import Path
import json
from typing import Any, Dict


def create_directory_if_not_exists(path: str | Path) -> None:
    """
    Creates a directory if it does not exist.
    
    Args:
        path: Directory path to be created
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def read_test_case_file(file_path: str | Path) -> str:
    """
    Reads a test case file.
    
    Args:
        file_path: File path
        
    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_json_file(file_path: str | Path, data: Dict[str, Any]) -> None:
    """
    Writes data to a JSON file.
    
    Args:
        file_path: File path
        data: Data to be written
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json_file(file_path: str | Path) -> Dict[str, Any]:
    """
    Reads a JSON file.
    
    Args:
        file_path: File path
        
    Returns:
        Data from the JSON file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_robot_file(file_path: str | Path, content: str) -> None:
    """
    Writes a Robot Framework file.
    
    Args:
        file_path: File path
        content: Robot script content
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def map_extracted_data_to_steps(module: Dict[str, Any]) -> Dict[str, Any]:
    """
    Maps extracted data to corresponding steps.
    
    Args:
        module: Module containing extracted_data and execution_steps
        
    Returns:
        Module with mapped data
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

    # Remove extracted_data from module level if everything was mapped
    if len(matched_indices) == len(extracted_items):
        module.pop("extracted_data", None)

    return module
