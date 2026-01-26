"""
Routing function after refinement node.
"""
from src.graph.state import GenIAState
from src.utils.enums import GenIANodeName, GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


def route_after_refinement(state: GenIAState) -> str:
    """
    Determine next node after refinement completes.
    
    Routes to:
    - EXPLORING_TASK: To extract elements from next module
    - CODING_TASK: If all modules have been refined
    
    Args:
        state: Current state of the graph
        
    Returns:
        Next node name as string
    """
    execution_status = state["execution_status"]
    
    logger.debug(f"Routing after refinement, status: {execution_status}")
    
    if execution_status == GenIAStateStatus.EXPLORING:
        return GenIANodeName.EXPLORING_TASK.value
    elif execution_status == GenIAStateStatus.CODING:
        return GenIANodeName.CODING_TASK.value
    else:
        logger.warning(f"Unexpected status after refinement: {execution_status}")
        return GenIANodeName.END.value
