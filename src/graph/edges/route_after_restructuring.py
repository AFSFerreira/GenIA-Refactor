from src.graph.state import GenIAState
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
    execution_status = state["execution_status"]
    
    if execution_status == GenIAStateStatus.RESTRUCTURING:
        return GenIANodeName.EXPLORING_TASK.value
    else:
        logger.warning(f"Unexpected status after restructuring: {execution_status}")
        return GenIANodeName.END.value
    