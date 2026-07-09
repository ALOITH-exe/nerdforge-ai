# backend/app/services/llm_service.py
import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional, List
from google import genai
from groq import Groq
from ..config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Unified LLM service with Groq primary + Gemini fallback"""
    
    def __init__(self):
        self.groq = self._init_groq()
        self.gemini_client = self._init_gemini()
        
        logger.info(f"✅ LLM Service initialized. Groq: {bool(self.groq)}, Gemini: {bool(self.gemini_client)}")
    
    def _init_groq(self):
        """Initialize Groq (Primary - Fastest)"""
        if settings.GROQ_API_KEY:
            try:
                client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info("✅ Groq initialized successfully")
                return client
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")
        else:
            logger.warning("⚠️ GROQ_API_KEY not set")
        return None
    
    def _init_gemini(self):
        """Initialize Google Gemini (Fallback)"""
        if settings.GEMINI_API_KEY:
            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("✅ Gemini initialized successfully")
                return client
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        else:
            logger.warning("⚠️ GEMINI_API_KEY not set")
        return None
    
    async def generate(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,  # Reduced to avoid token limits
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate response with Groq primary + Gemini fallback"""
        
        # Try Groq FIRST (fastest)
        if self.groq and (not model or model == "groq"):
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                # Retry logic for rate limits
                for attempt in range(3):
                    try:
                        response = self.groq.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            timeout=60.0
                        )
                        if response.choices and len(response.choices) > 0:
                            content = response.choices[0].message.content
                            if content is not None:
                                return content
                            return ""
                        return ""
                    except Exception as e:
                        if "429" in str(e) and attempt < 2:
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limited, waiting {wait_time}s...")
                            await asyncio.sleep(wait_time)
                            continue
                        raise e
            except Exception as e:
                logger.warning(f"Groq failed after retries: {e}")
        
        # Try Gemini fallback
        if self.gemini_client and (not model or model == "gemini"):
            try:
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                # Using correct model name - gemini-2.0-flash
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",  # Fixed model name
                    contents=full_prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens
                    }
                )
                if response.text is not None:
                    return response.text
                return ""
            except Exception as e:
                logger.warning(f"Gemini failed: {e}")
        
        # If both fail
        logger.error("All AI models failed")
        return "Error: No AI model available. Please check your API keys."
    
    async def generate_json(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """Generate structured JSON output with improved parsing"""
        
        # Truncate prompt if too long (Groq has 6000 token limit)
        if len(prompt) > 4000:
            prompt = prompt[:4000] + "\n... [truncated for length]"
            logger.warning("Prompt truncated to avoid token limits")
        
        json_prompt = f"""
        {prompt}
        
        Return valid JSON matching this schema:
        {json.dumps(schema, indent=2)}
        
        Output ONLY JSON, no other text or explanation.
        """
        
        response = await self.generate(json_prompt, model, temperature, max_tokens=2048)
        
        # Improved JSON extraction
        try:
            # Look for JSON between ```json and ``` markers
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            # Try to find JSON object using regex
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                response = json_match.group(0)
            
            # Parse the JSON
            return json.loads(response.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response: {response[:500]}...")
            
            # Return a fallback response
            return self._get_fallback_scenario()
    
    def _get_fallback_scenario(self) -> Dict[str, Any]:
        """Return a fallback scenario when parsing fails"""
        return {
            "company_profile": {
                "name": "NerdForge Corp",
                "employees": 500,
                "industry": "Technology",
                "description": "A technology company with hybrid work environment"
            },
            "network_topology": {
                "architecture": "Hybrid Cloud",
                "segments": ["Corporate Network", "DMZ", "Cloud VPC"],
                "security_controls": ["Firewall", "IDS/IPS", "SIEM", "MFA"]
            },
            "attack_stages": [
                {
                    "stage": "Initial Access",
                    "technique": "Phishing",
                    "mitre_tactic": "TA0001",
                    "mitre_technique": "T1566.001",
                    "description": "Attacker sends phishing email with malicious attachment",
                    "commands": ["powershell -nop -w hidden -c Invoke-Expression"],
                    "tools": ["PowerShell"]
                },
                {
                    "stage": "Execution",
                    "technique": "PowerShell",
                    "mitre_tactic": "TA0002",
                    "mitre_technique": "T1059.001",
                    "description": "Macro executes PowerShell to download payload",
                    "commands": ["powershell -exec bypass -file payload.ps1"],
                    "tools": ["PowerShell"]
                },
                {
                    "stage": "Persistence",
                    "technique": "Registry Run Keys",
                    "mitre_tactic": "TA0003",
                    "mitre_technique": "T1547.001",
                    "description": "Adds registry key for persistence",
                    "commands": ["reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Update /t REG_SZ /d C:\\Users\\Public\\update.exe"],
                    "tools": ["reg.exe"]
                }
            ],
            "timeline": [
                {"time": "09:00", "action": "Email Delivered", "description": "Phishing email received by user"},
                {"time": "09:03", "action": "Attachment Opened", "description": "User opens malicious Word document"},
                {"time": "09:05", "action": "PowerShell Executed", "description": "Macro executes malicious PowerShell"},
                {"time": "09:08", "action": "Persistence Established", "description": "Registry run key added"}
            ],
            "objectives": ["Steal credentials", "Deploy ransomware", "Establish persistent access"],
            "indicators": ["malicious-domain.com", "185.xxx.xxx.xxx", "powershell.exe", "mimikatz.exe"]
        }
    
    async def generate_scenario(
        self,
        industry: str,
        attack_type: str,
        difficulty: str = "medium",
        os: str = "Windows",
        environment: str = "on-premise"
    ) -> Dict[str, Any]:
        """Generate a complete attack scenario"""
        
        schema = {
            "type": "object",
            "properties": {
                "company_profile": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "employees": {"type": "integer"},
                        "industry": {"type": "string"},
                        "description": {"type": "string"}
                    }
                },
                "network_topology": {
                    "type": "object",
                    "properties": {
                        "architecture": {"type": "string"},
                        "segments": {"type": "array", "items": {"type": "string"}},
                        "security_controls": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "attack_stages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "stage": {"type": "string"},
                            "technique": {"type": "string"},
                            "mitre_tactic": {"type": "string"},
                            "mitre_technique": {"type": "string"},
                            "description": {"type": "string"},
                            "commands": {"type": "array", "items": {"type": "string"}},
                            "tools": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "timeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "time": {"type": "string"},
                            "action": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "objectives": {"type": "array", "items": {"type": "string"}},
                "indicators": {"type": "array", "items": {"type": "string"}}
            }
        }
        
        # Simplified prompt to avoid token limits
        prompt = f"""
        Generate a realistic cyber attack scenario:
        Industry: {industry}
        Attack Type: {attack_type}
        Difficulty: {difficulty}
        OS: {os}
        Environment: {environment}
        
        Include MITRE ATT&CK techniques, commands, and timeline.
        """
        
        return await self.generate_json(prompt, schema, temperature=0.3)
    
    async def analyze_events(
        self,
        events: List[Dict],
        attack_plan: Dict
    ) -> Dict[str, Any]:
        """Analyze security events and provide SOC insights"""
        
        schema = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "detections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "event_id": {"type": "string"},
                            "severity": {"type": "string"},
                            "confidence": {"type": "integer"},
                            "description": {"type": "string"},
                            "mitre_technique": {"type": "string"},
                            "explanation": {"type": "string"}
                        }
                    }
                },
                "attack_chain": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step": {"type": "integer"},
                            "event": {"type": "string"},
                            "mitre_tactic": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "severity_score": {"type": "integer"},
                "priority": {"type": "string"},
                "recommended_actions": {"type": "array", "items": {"type": "string"}}
            }
        }
        
        # Simplified prompt to avoid token limits
        prompt = f"""
        Analyze these security events for a SOC analyst.
        Events: {json.dumps(events[:5], indent=2)}
        Context: {json.dumps(attack_plan, indent=2) if attack_plan else 'None'}
        
        Provide analysis with:
        1. Summary
        2. Detections with severity and explanation
        3. Attack chain
        4. Severity score (0-100)
        5. Priority level
        6. Recommended actions
        """
        
        return await self.generate_json(prompt, schema, temperature=0.3)