"""
Main entry point for GenIA-E2ETest.

This script manages the complete E2E test generation flow:
1. Reads test cases from TestCaseExamples folder
2. Restructures using LangGraph
3. Extracts and refines HTML elements
4. Generates Robot Framework scripts
5. Saves results to TestCases folder
"""
import asyncio
from pathlib import Path
from src.graph.workflow import compile_workflow
from src.graph.state import GenIAState
from src.tools.file_system import (
    create_directory_if_not_exists,
    read_test_case_file,
    write_json_file,
    write_robot_file
)
from src.utils.config import get_example_folder, get_output_folder
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def process_test_case(test_case_file: Path, output_folder: Path, num_attempts: int = 1):
    """
    Processes a single test case through the LangGraph workflow.
    
    Args:
        test_case_file: Test case file
        output_folder: Output folder
        num_attempts: Number of attempts (to generate multiple versions)
    """
    logger.info(f"Processing test case: {test_case_file.name}")
    
    # Read test case content
    test_case_content = read_test_case_file(test_case_file)
    
    # Create folder for this test case
    test_case_folder = output_folder / test_case_file.stem
    create_directory_if_not_exists(test_case_folder)
    
    # Compile workflow
    workflow = compile_workflow()
    
    for attempt in range(num_attempts):
        logger.info(f"Attempt {attempt + 1}/{num_attempts}")
        
        # Create folder for this attempt
        attempt_folder = test_case_folder / f"{attempt + 1}.{test_case_file.stem}"
        create_directory_if_not_exists(attempt_folder)
        
        # Initial state
        initial_state: GenIAState = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Process test case: {test_case_file.stem}",
                    "test_case_content": test_case_content
                }
            ],
            "test_plan": None,
            "current_module_index": 0,
            "execution_status": "refactoring",
            "script_robot": None,
            "test_case_name": test_case_file.stem,
            "output_directory": str(attempt_folder),
            "attempt_number": attempt + 1
        }
        
        # Execute workflow
        try:
            final_state = await workflow.ainvoke(initial_state)
            
            # Save restructured test plan (Refined JSON)
            if final_state.get("test_plan"):
                refined_json_path = test_case_folder / f"Refined{test_case_file.stem}.json"
                test_plan_dict = final_state["test_plan"].model_dump()
                write_json_file(refined_json_path, test_plan_dict)
                logger.info(f"Test plan saved to: {refined_json_path}")
            
            # Save extracted and refined data
            if final_state.get("test_plan"):
                extracted_data_path = attempt_folder / "ExtractedData.json"
                refined_data_path = attempt_folder / "RefinedExtractedData.json"
                
                test_plan_dict = final_state["test_plan"].model_dump()
                write_json_file(extracted_data_path, test_plan_dict)
                write_json_file(refined_data_path, test_plan_dict)
                
                logger.info(f"Data saved to: {attempt_folder}")
            
            # Save Robot Framework script
            if final_state.get("script_robot"):
                robot_script_path = attempt_folder / "E2ETest.robot"
                write_robot_file(robot_script_path, final_state["script_robot"])
                logger.info(f"Robot Framework script saved to: {robot_script_path}")
            
            logger.info(f"Attempt {attempt + 1} completed successfully")
            
        except Exception as e:
            logger.error(f"Error in attempt {attempt + 1}: {str(e)}", exc_info=True)
            continue


async def main():
    """
    Main function that processes all test cases.
    """
    logger.info("=== Starting GenIA-E2ETest ===")
    
    # Get folders
    example_folder = get_example_folder()
    output_folder = get_output_folder()
    
    # Create output folder if it doesn't exist
    create_directory_if_not_exists(output_folder)
    
    # Process each file from examples folder
    test_case_files = sorted(example_folder.glob("*.feature"))
    
    if not test_case_files:
        logger.warning(f"No .feature files found in {example_folder}")
        return
    
    logger.info(f"Found {len(test_case_files)} test cases to process")
    
    for test_case_file in test_case_files:
        try:
            await process_test_case(
                test_case_file=test_case_file,
                output_folder=output_folder,
                num_attempts=1  # Can be configurable
            )
        except Exception as e:
            logger.error(f"Error processing {test_case_file.name}: {str(e)}", exc_info=True)
            continue
    
    logger.info("=== Processing completed ===")


if __name__ == "__main__":
    asyncio.run(main())
