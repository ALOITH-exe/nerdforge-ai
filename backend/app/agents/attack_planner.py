# backend/app/agents/attack_planner.py
from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class AttackPlannerAgent(BaseAgent):
    """Generates realistic attack scenarios using AI"""
    
    def __init__(self, llm_service):
        super().__init__(llm_service)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate attack scenario from user input"""
        
        # Extract user inputs
        industry = input_data.get('industry', 'Technology')
        attack_type = input_data.get('attack_type', 'Ransomware')
        difficulty = input_data.get('difficulty', 'Medium')
        os = input_data.get('operating_system', 'Windows')
        environment = input_data.get('environment', 'On-Premise')
        custom_scenario = input_data.get('custom_scenario', None)
        
        # If user provided a custom scenario description, still generate a
        # full MITRE-mapped scenario via the AI - just steer it with the
        # user's text instead of ignoring it.
        result = await self.llm.generate_scenario(
            industry=industry,
            attack_type=attack_type,
            difficulty=difficulty.lower(),
            os=os,
            environment=environment.lower().replace(' ', '-'),
            custom_scenario=custom_scenario
        )
        
        # Store in context
        self.update_context('attack_plan', result)
        
        return result