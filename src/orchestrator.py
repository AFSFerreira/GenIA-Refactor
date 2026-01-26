from typing import Hashable, cast
from src.env import env_variables
from langgraph.graph import StateGraph
from src.graph.nodes.restructuring import restructuring_node
from src.graph.state import GenIAState, GenIAStateStatus
from src.tools.files import write_file
from src.utils.enums import GenIANodeName
from src.utils.routing_maps import restructuring_routes_map

routes_map: dict[GenIAStateStatus, GenIANodeName] = {
  GenIAStateStatus.EXPLORING: GenIANodeName.EXPLORING_TASK,
}

class GenIAStateOrchestrator:
  # def __init__():
  def _build_graph(self) -> None:
    """..."""
    
    def execute_restructuring(state: GenIAState) -> GenIAState:
      return restructuring_node(state)
    
    def route_after_restructuring(state: GenIAState) -> str:
      refined_test_case = state["refined_test_case"]
      
      # TODO: Melhorar exceção
      if refined_test_case is None:
        raise Exception("erro de test case")
      
      filename = state["test_case_name"]
      new_filename = str(env_variables.test_cases_output_folder / f"Refined-{filename}.json")
      
      write_file(file_path=new_filename, content=refined_test_case.model_dump_json(indent=2))
      
      execution_status = state["execution_status"]
      
      if execution_status == GenIAStateStatus.RESTRUCTURING:
        return GenIAStateStatus.EXPLORING
      else:
        return GenIANodeName.END
    
    # --- INITIAL SETUP ---
    workflow = StateGraph(GenIAState)
    
    workflow.add_node(GenIANodeName.RESTRUCTURING_TASK, execute_restructuring)
    
    workflow.add_conditional_edges(GenIANodeName.RESTRUCTURING_TASK, route_after_restructuring, cast(dict[Hashable, str], restructuring_routes_map))
    
    workflow.add_edge(GenIANodeName.START, GenIANodeName.RESTRUCTURING_TASK)
    workflow.add_edge(GenIANodeName.CODING_TASK, GenIANodeName.END)
    
