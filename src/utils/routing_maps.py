from src.utils.enums import GenIANodeName, GenIAStateStatus


restructuring_routes_map: dict[GenIAStateStatus, GenIANodeName] = {
  GenIAStateStatus.RESTRUCTURING: GenIANodeName.EXPLORING_TASK,
}
