# backend/app/services/atomic_service.py
import json
import subprocess
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AtomicRedTeamService:
    """Service for interacting with Atomic Red Team"""
    
    def __init__(self):
        self.technique_map = self._load_technique_map()
        logger.info(f"✅ Atomic Red Team loaded with {len(self.technique_map)} techniques")
    
    def _load_technique_map(self) -> Dict:
        """Load MITRE technique mapping"""
        # Basic mapping for now - we'll expand this
        return {
            "T1566.001": "Phishing with Malicious Attachment",
            "T1059.001": "PowerShell Execution",
            "T1547.001": "Registry Run Keys",
            "T1003.001": "LSASS Memory Dumping",
            "T1550.002": "Pass the Hash",
            "T1021": "Remote Services",
            "T1486": "Data Encrypted for Impact"
        }
    
    def get_techniques_for_attack(self, attack_type: str) -> List[str]:
        """Get relevant MITRE techniques for an attack type"""
        technique_map = {
            "ransomware": ["T1566.001", "T1059.001", "T1547.001", "T1003.001", "T1486"],
            "phishing": ["T1566.001", "T1059.001", "T1547.001", "T1003.001"],
            "data_exfiltration": ["T1566.001", "T1059.001", "T1021", "T1041"],
            "lateral_movement": ["T1021", "T1550.002", "T1003.001"],
            "default": ["T1566.001", "T1059.001", "T1547.001"]
        }
        return technique_map.get(attack_type.lower(), technique_map["default"])
    
    def get_atomic_test(self, technique_id: str) -> Dict:
        """Get atomic test details for a technique"""
        # This will be expanded with actual Atomic Red Team data
        atomic_tests = {
            "T1566.001": {
                "name": "Spearphishing Attachment",
                "description": "Send phishing email with malicious attachment",
                "executor": "PowerShell",
                "command": "Send-MailMessage -To victim@company.com -Subject 'Urgent Invoice' -Attachment malicious.doc"
            },
            "T1059.001": {
                "name": "PowerShell Execution",
                "description": "Execute PowerShell commands",
                "executor": "PowerShell",
                "command": "powershell.exe -nop -w hidden -c 'Invoke-Expression'"
            }
        }
        return atomic_tests.get(technique_id, {})
    
    def get_attack_chain(self, attack_type: str) -> List[Dict]:
        """Build attack chain based on attack type"""
        techniques = self.get_techniques_for_attack(attack_type)
        chain = []
        
        for i, tech_id in enumerate(techniques):
            tech_name = self.technique_map.get(tech_id, tech_id)
            atomic_test = self.get_atomic_test(tech_id)
            
            chain.append({
                "step": i + 1,
                "technique_id": tech_id,
                "technique_name": tech_name,
                "description": atomic_test.get("description", "Atomic test"),
                "executor": atomic_test.get("executor", "Unknown"),
                "command": atomic_test.get("command", "")
            })
        
        return chain