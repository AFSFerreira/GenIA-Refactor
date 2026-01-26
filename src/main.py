"""
Main entry point for GenIA E2E Test Generator.

This script processes test case files and generates Robot Framework E2E tests
using the LangGraph workflow orchestrator.
"""
import asyncio
from pathlib import Path

from src.env import env_variables
from src.graph.orchestrator import GenIAStateOrchestrator
from src.tools.file_system import create_directory_if_not_exists, read_test_case_file
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def process_test_cases(
    input_folder: Path,
    output_folder: Path,
    num_attempts: int = 1
) -> None:
    """
    Process all test case files in the input folder.
    
    Args:
        input_folder: Folder containing .feature test case files.
        output_folder: Folder for output files.
        num_attempts: Number of attempts per test case.
    """
    create_directory_if_not_exists(output_folder)
    
    orchestrator = GenIAStateOrchestrator(output_dir=output_folder)
    
    for test_file in input_folder.iterdir():
        if test_file.is_file():
            logger.info(f"Processing test case: {test_file.name}")
            
            test_case_content = read_test_case_file(test_file)
            test_case_name = test_file.stem
            
            for attempt in range(1, num_attempts + 1):
                logger.info(f"Attempt {attempt}/{num_attempts} for {test_case_name}")
                
                try:
                    final_state = await orchestrator.run(
                        test_case=test_case_content,
                        test_case_name=test_case_name,
                        attempt_number=attempt
                    )
                    
                    if final_state.get("script_robot"):
                        logger.info(f"Successfully generated test for {test_case_name}")
                    else:
                        logger.warning(f"No script generated for {test_case_name}")
                        
                except Exception as e:
                    logger.error(f"Error processing {test_case_name}: {e}")
                    raise


async def main():
    """Main entry point."""
    logger.info("Starting GenIA E2E Test Generator...")
    
    input_folder = env_variables.test_cases_examples_folder
    output_folder = env_variables.test_cases_output_folder
    
    await process_test_cases(
        input_folder=input_folder,
        output_folder=output_folder,
        num_attempts=1
    )
    
    logger.info("GenIA E2E Test Generator completed.")


if __name__ == "__main__":
    asyncio.run(main())
