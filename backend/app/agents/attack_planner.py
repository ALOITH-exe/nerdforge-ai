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
        
        # If user provided custom scenario, use it directly
        if custom_scenario:
            result = self._parse_custom_scenario(custom_scenario)
        else:
            # Generate with AI
            result = await self.llm.generate_scenario(
                industry=industry,
                attack_type=attack_type,
                difficulty=difficulty.lower(),
                os=os,
                environment=environment.lower().replace(' ', '-')
            )
        
        # Store in context
        self.update_context('attack_plan', result)
        
        return result
    
    def _parse_custom_scenario(self, custom_scenario: str) -> Dict[str, Any]:
        """Parse user-provided custom scenario"""
        return {
            "company_profile": {
                "name": "Custom Company",
                "employees": 100,
                "industry": "Custom",
                "description": custom_scenario[:200]
            },
            "network_topology": {
                "architecture": "Custom network",
                "segments": ["Internal", "DMZ"],
                "security_controls": ["Firewall", "IDS"]
            },
            "attack_stages": [
                {
                    "stage": "Custom Attack",
                    "technique": "Custom Technique",
                    "mitre_tactic": "TA0001",
                    "mitre_technique": "T0000",
                    "description": custom_scenario,
                    "commands": ["custom command"],
                    "tools": ["custom tool"]
                }
            ],
            "timeline": [
                {
                    "time": "00:00",
                    "action": "Attack Started",
                    "description": custom_scenario[:100]
                }
            ],
            "objectives": ["Custom objective"],
            "indicators": ["Custom indicator"]
        }