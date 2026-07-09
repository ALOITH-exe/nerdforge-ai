# API Contract - NerdForge AI

## POST /api/attacks/generate

**Request:**
{
"name": string,
"industry": string,
"attack_type": string,
"difficulty": string,
"operating_system": string,
"environment": string,
"custom_scenario": string (optional)
}

**Response:**
{
"id": string,
"name": string,
"description": string,
"status": string,
"created_at": datetime,
"attack_stages": list,
"timeline": list,
"events": list,
"analysis": object
}
