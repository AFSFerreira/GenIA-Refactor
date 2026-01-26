"""
GenIA E2E Test Orchestrator - LangGraph workflow for E2E test generation.

This orchestrator coordinates the following phases:
1. Restructuring (Level 1): Break test case into modules by URL
2. Extraction (Level 2): Extract HTML elements from each page
3. Refinement (Level 2): Refine and validate extracted elements
4. Generation (Level 3): Generate Robot Framework script
"""
from pathlib import Path
from typing import Hashable, Optional, cast

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.env import env_variables
from src.graph.edges import (
    route_after_extraction,
    route_after_refinement,
    route_after_restructuring,
)
from src.graph.nodes import (
    extraction_node,
    generation_node,
    refinement_node,
    restructuring_node,
)
from src.graph.routing_maps import (
    extraction_routes_map,
    refinement_routes_map,
    restructuring_routes_map,
)
from src.graph.state import GenIAState
from src.tools.file_system import (
    create_directory_if_not_exists,
    write_json_file,
    write_robot_file,
)
from src.utils.enums import GenIANodeName, GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GenIAStateOrchestrator:
    """
    Orchestrator for the E2E test generation workflow.
    
    This class builds and manages the LangGraph workflow that processes
    test cases through restructuring, extraction, refinement, and code generation.
    """
    
    def __init__(self, output_dir: Optional[str | Path] = None):
        """
        Initialize the orchestrator.
        
        Args:
            output_dir: Directory for output files. Defaults to env config.
        """
        self.output_dir = Path(output_dir) if output_dir else env_variables.test_cases_output_folder
        self.graph: Optional[CompiledStateGraph] = None
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Build the LangGraph workflow with all nodes and edges."""
        logger.info("Building GenIA workflow graph...")
        
        workflow = StateGraph(GenIAState)
        
        # Add all nodes
        workflow.add_node(GenIANodeName.RESTRUCTURING_TASK, restructuring_node)
        workflow.add_node(GenIANodeName.EXPLORING_TASK, extraction_node)
        workflow.add_node(GenIANodeName.REFINING_TASK, refinement_node)
        workflow.add_node(GenIANodeName.CODING_TASK, generation_node)
        
        # Add conditional edges for routing
        workflow.add_conditional_edges(
            GenIANodeName.RESTRUCTURING_TASK,
            route_after_restructuring,
            cast(dict[Hashable, str], restructuring_routes_map)
        )
        
        workflow.add_conditional_edges(
            GenIANodeName.EXPLORING_TASK,
            route_after_extraction,
            cast(dict[Hashable, str], extraction_routes_map)
        )
        
        workflow.add_conditional_edges(
            GenIANodeName.REFINING_TASK,
            route_after_refinement,
            cast(dict[Hashable, str], refinement_routes_map)
        )
        
        # Add static edges
        workflow.add_edge(GenIANodeName.START, GenIANodeName.RESTRUCTURING_TASK)
        workflow.add_edge(GenIANodeName.CODING_TASK, GenIANodeName.END)
        
        # Compile the graph
        self.graph = workflow.compile()
        
        logger.info("Workflow graph built successfully")
    
    async def run(
        self,
        test_case: str,
        test_case_name: str,
        attempt_number: int = 1
    ) -> GenIAState:
        """
        Run the workflow for a single test case.
        
        Args:
            test_case: Raw test case text content.
            test_case_name: Name identifier for the test case.
            attempt_number: Attempt number (for retries).
            
        Returns:
            Final state after workflow completion.
        """
        if self.graph is None:
            raise RuntimeError("Workflow graph not initialized")
        
        logger.info(f"Starting workflow for test case: {test_case_name}")
        
        # Create output directory structure
        test_case_folder = self.output_dir / test_case_name
        attempt_folder = test_case_folder / f"{attempt_number}.{test_case_name}"
        create_directory_if_not_exists(attempt_folder)
        
        # Initialize state
        initial_state: GenIAState = {
            "messages": [],
            "attempt_number": attempt_number,
            "test_case": test_case,
            "test_case_name": test_case_name,
            "refined_test_case": None,
            "current_module_index": 0,
            "execution_status": GenIAStateStatus.STARTING,
            "output_directory": str(attempt_folder),
            "script_robot": None,
            "extracted_test_case": None,
            "refined_extracted_test_case": None,
            "crawler_context": None,
        }
        
        # Run the workflow
        final_state_raw = await self.graph.ainvoke(initial_state)
        final_state = cast(GenIAState, final_state_raw)
        
        # Save output files
        self._save_outputs(final_state, attempt_folder)
        
        logger.info(f"Workflow completed for test case: {test_case_name}")
        
        return final_state
    
    def _save_outputs(self, state: GenIAState, output_folder: Path) -> None:
        """
        Save workflow outputs to files.
        
        Args:
            state: Final workflow state.
            output_folder: Directory to save outputs.
        """
        logger.info(f"Saving outputs to: {output_folder}")
        
        # Save extracted data (Level 2 first pass)
        extracted_test_case = state.get("extracted_test_case")
        if extracted_test_case is not None:
            extracted_file = output_folder / "ExtractedData.json"
            write_json_file(extracted_file, extracted_test_case)
        
        # Save refined extracted data (Level 2 second pass)
        refined_extracted_test_case = state.get("refined_extracted_test_case")
        if refined_extracted_test_case is not None:
            refined_file = output_folder / "RefinedExtractedData.json"
            write_json_file(refined_file, refined_extracted_test_case)
        
        # Save Robot Framework script (Level 3)
        script_robot = state.get("script_robot")
        if script_robot is not None:
            robot_file = output_folder / "E2ETest.robot"
            write_robot_file(robot_file, script_robot)
        
        logger.info("All outputs saved successfully")

    
