"""
Reviewer Agent - Responsible for reviewing and validating generated scripts.
"""
from src.graph.state import GenIAState
from src.tools.validator import RobotValidator
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReviewerAgent:
    """
    Agent responsible for reviewing and validating Robot Framework scripts.
    
    This agent executes dry-runs and validates syntax of generated scripts,
    ensuring they are ready for execution.
    """
    
    def __init__(self):
        self.name = "Reviewer"
        self.validator = RobotValidator()
    
    def execute(self, state: GenIAState, robot_file_path: str) -> tuple[bool, str]:
        """
        Validates the generated Robot Framework script.
        
        Args:
            state: Current state of the graph
            robot_file_path: Path to the .robot file to be validated
            
        Returns:
            Tuple (valid, message)
        """
        logger.info(f"Validating script: {robot_file_path}")
        
        is_valid, error_msg = self.validator.validate_syntax(robot_file_path)
        
        if is_valid:
            logger.info("Script validated successfully")
            state["messages"].append({
                "role": "assistant",
                "content": "Script validated successfully",
                "node": "reviewer"
            })
            return True, "Valid script"
        else:
            logger.warning(f"Validation error: {error_msg}")
            state["messages"].append({
                "role": "assistant",
                "content": f"Validation error: {error_msg}",
                "node": "reviewer"
            })
            return False, error_msg
