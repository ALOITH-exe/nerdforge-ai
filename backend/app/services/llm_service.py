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


class LLMJSONError(Exception):
    """Raised when the model's output could not be parsed into the requested
    JSON shape even after retries and repair attempts. Callers can catch this
    and surface a clear error, or pass a `fallback` to generate_json to avoid
    raising entirely."""
    pass


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
        system_prompt: Optional[str] = None,
        force_json: bool = False,
    ) -> str:
        """Generate response with Groq primary + Gemini fallback.

        force_json=True asks the provider's native JSON mode to constrain
        output to syntactically valid JSON (Groq's response_format /
        Gemini's response_mime_type). This does NOT guarantee the JSON
        matches our desired *shape* - generate_json() still validates and
        repairs that - but it eliminates most stray prose/markdown wrapping.
        """

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
                        create_kwargs = dict(
                            model="llama-3.1-8b-instant",
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            timeout=60.0,
                        )
                        if force_json:
                            create_kwargs["response_format"] = {"type": "json_object"}

                        try:
                            response = self.groq.chat.completions.create(**create_kwargs)
                        except Exception as inner_e:
                            # Some Groq models/accounts may reject response_format -
                            # fall back to a plain call rather than losing the whole request.
                            if force_json and "response_format" in str(inner_e).lower():
                                create_kwargs.pop("response_format", None)
                                response = self.groq.chat.completions.create(**create_kwargs)
                            else:
                                raise

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
                config: Dict[str, Any] = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
                if force_json:
                    config["response_mime_type"] = "application/json"

                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=full_prompt,
                    config=config,
                )
                if response.text is not None:
                    return response.text
                return ""
            except Exception as e:
                logger.warning(f"Gemini failed: {e}")

        # If both fail
        logger.error("All AI models failed")
        return "Error: No AI model available. Please check your API keys."

    # ------------------------------------------------------------------
    # Structured JSON generation
    # ------------------------------------------------------------------

    def _schema_to_template(self, schema: Dict[str, Any]) -> Any:
        """
        Convert our simplified JSON-schema-like dict into a flat EXAMPLE
        instance rather than JSON-Schema-draft syntax.

        This matters a lot in practice: smaller/faster models (like
        llama-3.1-8b-instant) frequently echo back a literal JSON-Schema
        envelope (`{"type": "object", "properties": {...}}`) when asked to
        "match this schema", instead of producing an instance of it. Showing
        the model something that already looks like the target JSON object -
        with placeholder text marking what to fill in - avoids that failure
        mode almost entirely.
        """
        t = schema.get("type")

        if t == "object":
            return {
                key: self._schema_to_template(val)
                for key, val in schema.get("properties", {}).items()
            }
        if t == "array":
            item_template = self._schema_to_template(schema.get("items", {"type": "string"}))
            return [item_template]
        if t in ("integer", "number"):
            hint = schema.get("description")
            return f"<{t}{': ' + hint if hint else ''}>"
        if t == "boolean":
            return "<true or false>"
        # string (default)
        hint = schema.get("description")
        return f"<string{': ' + hint if hint else ''}>"

    def _extract_json(self, response: str) -> Optional[Dict[str, Any]]:
        """Best-effort extraction + repair of a JSON object from raw model output."""
        text = (response or "").strip()

        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            text = match.group(0)
        text = text.strip()

        if not text:
            return None

        # Attempt 1: parse as-is. strict=False permits literal control
        # characters (raw newlines/tabs) inside strings, which some models
        # emit when writing multi-line rule content instead of escaping them.
        try:
            return json.loads(text, strict=False)
        except json.JSONDecodeError:
            pass

        # Attempt 2: repair invalid backslash escapes. Rule content (YARA
        # regex, Windows paths like C:\Users) often contains backslashes
        # that aren't valid JSON escape sequences (\d, \U, \S, ...). Escape
        # any backslash not already followed by a valid JSON escape char.
        sanitized = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
        try:
            return json.loads(sanitized, strict=False)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON even after sanitization: {e}")
            logger.error(f"Response snippet: {text[:500]}")
            return None

    def _matches_schema_shape(self, value: Any, schema: Dict[str, Any]) -> bool:
        """
        Validate that a parsed value actually matches the *shape* of the
        schema, not just that it's syntactically valid JSON.

        This catches the failure mode where a model echoes JSON-Schema-draft
        structure into a field instead of producing real content - e.g.
        {"rule_name": {"type": "string", "value": "..."}} instead of
        {"rule_name": "..."}. That's syntactically valid JSON, so a plain
        json.loads() success would miss it; only checking primitive types
        against the schema catches it.

        Permissive about missing keys (the model may reasonably omit an
        optional field), strict about keys that ARE present having the
        wrong type.
        """
        t = schema.get("type")

        if t == "object":
            if not isinstance(value, dict):
                return False
            props = schema.get("properties", {})
            if props and not (set(props.keys()) & set(value.keys())):
                # None of the expected fields are present at all - this isn't a
                # partial instance of our schema (a model reasonably omitting
                # one optional field), it's an unrelated or empty object (e.g.
                # {} used as a stub, or a completely different structure).
                return False
            for key, sub_schema in props.items():
                if key in value and not self._matches_schema_shape(value[key], sub_schema):
                    return False
            return True
        if t == "array":
            if not isinstance(value, list):
                return False
            item_schema = schema.get("items", {"type": "string"})
            # Sample-check rather than validating every item, for speed on long lists
            return all(self._matches_schema_shape(v, item_schema) for v in value[:3])
        if t in ("integer", "number"):
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t == "boolean":
            return isinstance(value, bool)
        # string (default)
        return isinstance(value, str)

    async def generate_json(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        temperature: float = 0.3,
        fallback: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output.

        If parsing fails after retrying once, returns `fallback` if provided;
        otherwise raises LLMJSONError so the caller (API layer) can surface a
        clear error instead of silently returning wrong-shaped data.
        """

        # Truncate prompt if too long (Groq has 6000 token limit)
        if len(prompt) > 4000:
            prompt = prompt[:4000] + "\n... [truncated for length]"
            logger.warning("Prompt truncated to avoid token limits")

        template = json.dumps(self._schema_to_template(schema), indent=2)
        base_prompt = f"""{prompt}

Respond with ONLY a single JSON object shaped exactly like this example
(replace every placeholder in angle brackets with real content, and keep
exactly these keys - do not add, remove, or rename keys, and do not include
the words "type" or "properties" anywhere in your answer):

{template}

Output raw JSON only - no markdown code fences, no commentary before or after."""

        last_response = ""
        for attempt in range(2):
            json_prompt = base_prompt
            if attempt == 1:
                json_prompt += (
                    "\n\nYour previous response was not valid JSON matching the shape "
                    "above. Try again - return ONLY the corrected JSON object."
                )

            response = await self.generate(
                json_prompt, model, temperature, max_tokens=2048, force_json=True
            )
            last_response = response

            parsed = self._extract_json(response)
            if parsed is not None and self._matches_schema_shape(parsed, schema):
                return parsed

            if parsed is not None:
                logger.error(
                    f"generate_json attempt {attempt + 1} parsed as valid JSON but didn't "
                    f"match the expected shape (likely a schema echo): {str(parsed)[:300]}"
                )
            else:
                logger.error(f"generate_json attempt {attempt + 1} failed to parse")

        logger.error(f"generate_json giving up after retries. Last response: {last_response[:500]}")

        if fallback is not None:
            return fallback

        raise LLMJSONError(
            "The AI returned output that couldn't be parsed as JSON, even after retrying. "
            "Please try again."
        )

    def _get_fallback_scenario(self) -> Dict[str, Any]:
        """Fallback scenario used only for the top-level generate_scenario call -
        the app's flagship flow should never hard-fail even if the AI output
        can't be parsed after retries."""
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

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Honest fallback for SOC analysis - keeps the overall attack-generation
        flow from hard-failing, but is clearly labeled as unavailable rather
        than silently showing wrong-shaped data."""
        return {
            "summary": (
                "AI analysis could not be generated for this attack after retrying. "
                "You can still review the attack stages and timeline above, or try "
                "regenerating the attack."
            ),
            "detections": [],
            "attack_chain": [],
            "severity_score": 50,
            "priority": "Medium",
            "recommended_actions": [
                "Review the attack stages and timeline manually",
                "Regenerate this attack for a fresh AI analysis",
            ],
        }

    # ------------------------------------------------------------------
    # Feature-specific generators
    # ------------------------------------------------------------------

    async def generate_scenario(
        self,
        industry: str,
        attack_type: str,
        difficulty: str = "medium",
        os: str = "Windows",
        environment: str = "on-premise",
        custom_scenario: Optional[str] = None
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

        custom_instruction = (
            f"\n        The user described this specific scenario - base the attack on it:\n        \"{custom_scenario[:500]}\"\n"
            if custom_scenario else ""
        )
        prompt = f"""
        Generate a realistic cyber attack scenario:
        Industry: {industry}
        Attack Type: {attack_type}
        Difficulty: {difficulty}
        OS: {os}
        Environment: {environment}
        {custom_instruction}
        Include MITRE ATT&CK techniques, commands, and timeline.
        """

        return await self.generate_json(
            prompt, schema, temperature=0.3, fallback=self._get_fallback_scenario()
        )

    async def extract_iocs(
        self,
        scenario: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract and enrich Indicators of Compromise from a scenario + its SOC analysis"""

        schema = {
            "type": "object",
            "properties": {
                "iocs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "indicator_type": {
                                "type": "string",
                                "description": "one of: ip, domain, url, file_hash, email, registry_key, filename"
                            },
                            "value": {"type": "string"},
                            "context": {"type": "string", "description": "why this is suspicious / where it appeared"},
                            "risk_score": {"type": "integer", "description": "0-100"}
                        }
                    }
                }
            }
        }

        raw_indicators = scenario.get("indicators", [])
        attack_stages = scenario.get("attack_stages", [])

        prompt = f"""
        Extract Indicators of Compromise (IOCs) from this attack scenario for a SOC analyst.

        Raw indicators already noted: {json.dumps(raw_indicators)}
        Attack stages: {json.dumps(attack_stages[:6], indent=2)}
        SOC analysis summary: {analysis.get('summary', 'None') if analysis else 'None'}

        For each IOC, classify its type, give brief enrichment context (why it's
        suspicious, which attack stage it relates to), and assign a risk score
        0-100. Include IPs, domains, file hashes, filenames, and registry keys
        where relevant. De-duplicate values.
        """

        # No fallback here: an empty/wrong IOC list silently looks like a
        # legitimate "no IOCs found" result, which is misleading. Better to
        # raise and let the API return a clear error so the user can retry.
        result = await self.generate_json(prompt, schema, temperature=0.2)
        return result.get("iocs", [])

    async def generate_detection_rule(
        self,
        attack_stage: Dict[str, Any],
        rule_format: str = "sigma"
    ) -> Dict[str, Any]:
        """Generate a detection rule (Sigma or YARA) for a given attack stage"""

        schema = {
            "type": "object",
            "properties": {
                "rule_name": {"type": "string"},
                "rule_content": {"type": "string", "description": "the full rule text in valid Sigma YAML or YARA syntax"},
                "description": {"type": "string"},
                "severity": {"type": "string", "description": "low, medium, high, or critical"},
                "confidence": {"type": "integer", "description": "0-100"}
            }
        }

        prompt = f"""
        Write a {rule_format.upper()} detection rule for this attack stage.

        Stage: {attack_stage.get('stage', 'Unknown')}
        Technique: {attack_stage.get('technique', 'Unknown')}
        MITRE Technique ID: {attack_stage.get('mitre_technique', 'Unknown')}
        Description: {attack_stage.get('description', '')}
        Example commands observed: {json.dumps(attack_stage.get('commands', []))}

        The rule_content field must contain a complete, syntactically valid
        {'Sigma rule in YAML' if rule_format == 'sigma' else 'YARA rule'} that
        would realistically detect this behavior. Within rule_content, escape
        backslashes and newlines properly so the surrounding JSON stays valid.
        """

        # No fallback: an empty rule_content silently rendered as a "successful"
        # card is exactly the bug we're fixing. Raise so the batch endpoint can
        # surface a clear error instead.
        result = await self.generate_json(prompt, schema, temperature=0.2)
        result["mitre_technique"] = attack_stage.get("mitre_technique", "")
        result["mitre_tactic"] = attack_stage.get("mitre_tactic", "")
        result["rule_format"] = rule_format
        return result

    async def generate_incident_report(
        self,
        scenario: Dict[str, Any],
        attack_summary: Dict[str, Any],
        analysis: Dict[str, Any],
        iocs: List[Dict[str, Any]],
        detections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a professional incident report from everything gathered so far"""

        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "executive_summary": {"type": "string"},
                "technical_details": {
                    "type": "object",
                    "properties": {
                        "attack_narrative": {"type": "string"},
                        "affected_systems": {"type": "array", "items": {"type": "string"}},
                        "attack_chain": {"type": "array", "items": {"type": "string"}},
                        "root_cause": {"type": "string"}
                    }
                },
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }

        prompt = f"""
        Write a professional cybersecurity incident report based on this data.

        Company: {json.dumps(scenario.get('company_profile', {}))}
        Attack summary: {json.dumps(attack_summary, indent=2)[:1500]}
        SOC analysis: {json.dumps(analysis, indent=2)[:1500] if analysis else 'None'}
        IOCs found: {len(iocs)} indicators - top ones: {json.dumps(iocs[:5])}
        Detection rules written: {len(detections)}

        Produce an executive summary suitable for leadership, a technical
        narrative of how the attack unfolded, affected systems, root cause,
        and concrete, prioritized remediation recommendations.
        """

        # No fallback: a report with an empty summary but a real-looking title
        # is worse than no report at all. Raise so the frontend shows a clear
        # error and the user can regenerate.
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

        # Fallback here (not the scenario one) so a parse failure during
        # attack generation degrades gracefully instead of 500ing the whole
        # request, while being honest that analysis is unavailable.
        return await self.generate_json(
            prompt, schema, temperature=0.3, fallback=self._get_fallback_analysis()
        )
