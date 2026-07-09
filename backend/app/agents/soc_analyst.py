# backend/app/agents/soc_analyst.py
from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class SOCAnalystAgent(BaseAgent):
    """Analyzes security events and provides SOC insights"""
    
    def __init__(self, llm_service):
        super().__init__(llm_service)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze events and provide SOC insights"""
        
        # Get events from input
        events = input_data.get('events', [])
        
        # Get attack plan from context (set by AttackPlannerAgent)
        attack_plan = self.get_context('attack_plan')
        if attack_plan is None:
            attack_plan = {}
        
        # Call the analyze_events method from llm_service
        result = await self.llm.analyze_events(
            events=events,
            attack_plan=attack_plan
        )
        
        # Store result in context for other agents
        self.update_context('soc_analysis', result)
        
        return result