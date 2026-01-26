"""
Shared state for the LangGraph workflow for E2E test generation.
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages, BaseMessage
from src.models import TestCaseModel
from src.utils.enums import GenIAStateStatus

class GenIAState(TypedDict):
    """
    Main state of the LangGraph graph.
    
    This state is shared across all graph nodes and maintains
    information about the progress of E2E test generation.
    """
    messages: Annotated[List[BaseMessage], add_messages] # Mensagens trocadas entre os agentes
    attempt_number: Optional[int] # Número de tentativas do agente em processar o input
    test_case: str # Input inicial do usuário
    test_case_name: Optional[str] # Nome do caso de teste original
    refined_test_case: Optional[TestCaseModel] # TestCaseModel extraido do prompt inicial do usuário pela LLM
    current_module_index: int # Índice do módulo atual do TestCaseModel percorrido pela LLM
    execution_status: Optional[GenIAStateStatus] # Status da execução do fluxo
    output_directory: Optional[str] # Diretório de saída do script de teste final
    script_robot: Optional[str] # Script robot gerado ao final do fluxo de execução
