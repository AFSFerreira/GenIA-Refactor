from src.env import env_variables
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(env_variables.prompts_dir))

def load_prompt(template_name: str, **kwargs) -> str:
    """
    Load a template and inject variables.
    Example: load_prompt('agents/langgraph/level1_restructuring.jinja2', test_case='...')
    """
    template = env.get_template(template_name)
    return template.render(**kwargs)
