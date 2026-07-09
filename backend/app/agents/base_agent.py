# backend/app/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, llm_service):
        self.llm = llm_service
        self.context: Dict[str, Any] = {}
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    def update_context(self, key: str, value: Any):
        """Update agent context"""
        self.context[key] = value
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get context value"""
        return self.context.get(key)