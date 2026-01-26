from src.env import env_variables

from src.graph.state import GenIAState
from src.tools.files import write_file
from src.tools.file_system import create_directory_if_not_exists
from src.utils.enums import GenIANodeName, GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


def route_after_restructuring(state: GenIAState) -> str:
    """
    Determine next node after restructuring completes.
    
    Saves the refined test case to disk and routes to extraction phase.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Next node name as string
    """
    refined_test_case = state["refined_test_case"]
    
    if refined_test_case is None:
        raise ValueError("refined_test_case is required after restructuring")
    
    # TODO: Exportar save pra _save:
    # Save refined test case
    test_case_name = state["test_case_name"]
    
    if test_case_name is None:
        raise ValueError("test_case_name is required after restructuring")
    
    test_case_folder = env_variables.test_cases_output_folder / test_case_name
    create_directory_if_not_exists(test_case_folder)
    
    new_filename = str(test_case_folder / f"Refined{test_case_name}.json")
    write_file(file_path=new_filename, content=refined_test_case.model_dump_json(indent=2))
    
    logger.info(f"Saved refined test case to: {new_filename}")
    
    execution_status = state["execution_status"]
    
    if execution_status == GenIAStateStatus.RESTRUCTURING:
        return GenIANodeName.EXPLORING_TASK.value
    else:
        logger.warning(f"Unexpected status after restructuring: {execution_status}")
        return GenIANodeName.END.value
    