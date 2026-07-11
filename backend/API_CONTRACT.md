# API Contract - NerdForge AI

Base URL (local): http://localhost:8000
Base URL (Railway): set by your deployment

---

## GET /api/health
Health check.

**Response:**
```
{
  "status": "healthy",
  "service": "NerdForge AI Backend",
  "database": "connected",
  "timestamp": datetime
}
```

---

## POST /api/attacks/generate
Generate a full attack scenario + SOC analysis in one call.

**Request:**
```
{
  "name": string,
  "industry": string,
  "attack_type": string,
  "difficulty": string,
  "operating_system": string,
  "environment": string,
  "custom_scenario": string (optional) - if provided, the AI still generates
    a full MITRE-mapped scenario but steers it toward this description
}
```

**Response:**
```
{
  "id": string,
  "name": string,
  "description": string,
  "status": string,
  "created_at": datetime,
  "attack_stages": list,
  "timeline": list,
  "events": list,   // derived from attack_stages, not static
  "analysis": object
}
```

---

## GET /api/attacks/
List all attacks (paginated).

**Query params:** `skip` (default 0), `limit` (default 10)

**Response:** list of `{ id, name, status, created_at }`

---

## GET /api/attacks/{attack_id}
Get full details for one attack.

**Response:**
```
{
  "id": string,
  "name": string,
  "description": string,
  "status": string,
  "created_at": datetime,
  "tactics": list,
  "timeline": list,
  "summary": object   // SOC analysis
}
```

---

## POST /api/attacks/{attack_id}/iocs/generate
Extract and enrich Indicators of Compromise from the attack's scenario + SOC analysis. Stores them.

**Response:** list of
```
{
  "id": string,
  "indicator_type": string,  // ip, domain, url, file_hash, email, registry_key, filename
  "value": string,
  "threat_intel": { "context": string },
  "risk_score": int (0-100),
  "created_at": datetime
}
```

## GET /api/attacks/{attack_id}/iocs
List previously generated IOCs for an attack.

---

## POST /api/attacks/{attack_id}/detections/generate
Generate detection rules (Sigma or YARA) for the attack's stages. Stores them.

**Request:**
```
{
  "rule_format": "sigma" | "yara"  (default "sigma"),
  "max_stages": int (default 5) - caps how many stages get rules, to limit LLM calls
}
```

**Response:** list of
```
{
  "id": string,
  "rule_name": string,
  "rule_format": string,
  "rule_content": string,   // full Sigma YAML or YARA rule text
  "description": string,
  "severity": string,
  "confidence": int (0-100),
  "mitre_technique": string,
  "mitre_tactic": string,
  "created_at": datetime
}
```

## GET /api/attacks/{attack_id}/detections
List previously generated detection rules for an attack.

---

## POST /api/attacks/{attack_id}/reports/generate
Generate a professional incident report from the scenario, SOC analysis, IOCs, and detections gathered so far. Stores it.

**Response:**
```
{
  "id": string,
  "title": string,
  "summary": string,           // executive summary
  "technical_details": {
    "attack_narrative": string,
    "affected_systems": list,
    "attack_chain": list,
    "root_cause": string
  },
  "recommendations": list,
  "created_at": datetime
}
```

## GET /api/attacks/{attack_id}/reports
List previously generated reports (id, title, summary, created_at only).

## GET /api/attacks/{attack_id}/reports/{report_id}
Get one report's full content (same shape as the generate response).

---

## Suggested frontend flow
1. `POST /api/attacks/generate` → shows scenario, timeline, events, SOC analysis immediately
2. User clicks "Extract IOCs" → `POST /api/attacks/{id}/iocs/generate`
3. User clicks "Generate Detection Rules" → `POST /api/attacks/{id}/detections/generate`
4. User clicks "Generate Report" → `POST /api/attacks/{id}/reports/generate` (works best after IOCs/detections exist, but not required)
