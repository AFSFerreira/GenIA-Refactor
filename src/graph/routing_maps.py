from src.utils.enums import GenIANodeName


restructuring_routes_map: dict[str, str] = {
    GenIANodeName.EXPLORING_TASK.value: GenIANodeName.EXPLORING_TASK.value,
}


extraction_routes_map: dict[str, str] = {
    GenIANodeName.REFINING_TASK.value: GenIANodeName.REFINING_TASK.value,
    GenIANodeName.CODING_TASK.value: GenIANodeName.CODING_TASK.value,
}


refinement_routes_map: dict[str, str] = {
    GenIANodeName.EXPLORING_TASK.value: GenIANodeName.EXPLORING_TASK.value,
    GenIANodeName.CODING_TASK.value: GenIANodeName.CODING_TASK.value,
}
