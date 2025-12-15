"""
Utility functions for loading and managing Jinja2 templates.
"""
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path


def load_prompt(filename: str) -> Template:
    """
    Loads a Jinja2 template from the prompts directory.
    
    Args:
        filename: Name of the Jinja2 file (e.g., 'level1_restructuring.jinja2')
        
    Returns:
        Loaded Jinja2 template ready for rendering
    """
    prompts_dir = Path(__file__).parent.parent / "prompts"
    env = Environment(loader=FileSystemLoader(prompts_dir))
    return env.get_template(filename)
