from src.env import env_variables
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(env_variables.langgraph_agents_prompts_dir))

def load_prompt(template_name: str, **kwargs) -> str:
    """
    Load a template and inject variables.
    Example: load_prompt('tdd/test_generation.jinja2', function_name='soma', is_test_review=True)
    """
    template = env.get_template(template_name)
    return template.render(**kwargs)
