"""
Tools for Robot Framework script validation.
"""
import subprocess
from typing import Tuple, Optional


class RobotValidator:
    """Validator for Robot Framework scripts."""
    
    @staticmethod
    def dry_run(robot_file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Executes a dry-run of the Robot Framework script.
        
        Args:
            robot_file_path: Path to the .robot file
            
        Returns:
            Tuple (success, error_message)
        """
        try:
            result = subprocess.run(
                ['robot', '--dryrun', robot_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout during validation"
        except FileNotFoundError:
            return False, "Robot Framework is not installed"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def validate_syntax(robot_file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validates the syntax of a Robot Framework file.
        
        Args:
            robot_file_path: Path to the .robot file
            
        Returns:
            Tuple (valid, error_message)
        """
        return RobotValidator.dry_run(robot_file_path)
