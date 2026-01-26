"""
Routing function after extraction node.
"""
from src.graph.state import GenIAState
from src.utils.enums import GenIANodeName, GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


def route_after_extraction(state: GenIAState) -> str:
    """
    Determine next node after extraction completes.
    
    Routes to:
    - REFINING_TASK: To refine the extracted elements
    - CODING_TASK: If all modules processed (shouldn't normally happen here)
    
    Args:
        state: Current state of the graph
        
    Returns:
        Next node name as string
    """
    execution_status = state["execution_status"]
    
    logger.debug(f"Routing after extraction, status: {execution_status}")
    
    if execution_status == GenIAStateStatus.REFINING:
        return GenIANodeName.REFINING_TASK.value
    elif execution_status == GenIAStateStatus.CODING:
        return GenIANodeName.CODING_TASK.value
    else:
        logger.warning(f"Unexpected status after extraction: {execution_status}")
        return GenIANodeName.END.value
