# backend/app/api/attacks.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

from ..database import get_db, Attack, Event, Scenario
from ..services.llm_service import LLMService
from ..agents.attack_planner import AttackPlannerAgent
from ..agents.soc_analyst import SOCAnalystAgent

router = APIRouter(prefix="/api/attacks", tags=["attacks"])

# Initialize services
llm_service = LLMService()
attack_planner = AttackPlannerAgent(llm_service)
soc_analyst = SOCAnalystAgent(llm_service)

# Request/Response Models
class AttackGenerateRequest(BaseModel):
    name: str
    industry: str = "Technology"
    attack_type: str = "Ransomware"
    difficulty: str = "Medium"
    operating_system: str = "Windows"
    environment: str = "On-Premise"
    custom_scenario: Optional[str] = None

class AttackResponse(BaseModel):
    id: str
    name: str
    description: str
    status: str
    created_at: datetime
    attack_stages: Optional[List[dict]] = None
    timeline: Optional[List[dict]] = None
    events: Optional[List[dict]] = None
    analysis: Optional[dict] = None

@router.post("/generate", response_model=AttackResponse)
async def generate_attack(
    request: AttackGenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate a complete attack scenario with SOC analysis"""
    try:
        # 1. Generate scenario using Attack Planner
        scenario_data = await attack_planner.process(request.dict())
        
        # 2. Create scenario in database
        db_scenario = Scenario(
            id=str(uuid.uuid4()),
            name=request.name,
            industry=request.industry,
            operating_system=request.operating_system,
            attack_type=request.attack_type,
            difficulty=request.difficulty,
            environment=request.environment,
            company_profile=scenario_data.get("company_profile", {}),
            network_topology=scenario_data.get("network_topology", {}),
            assets=scenario_data.get("assets", []),
            security_controls=scenario_data.get("security_controls", []),
            attack_stages=scenario_data.get("attack_stages", [])
        )
        db.add(db_scenario)
        db.commit()
        db.refresh(db_scenario)
        
        # 3. Create attack in database
        db_attack = Attack(
            id=str(uuid.uuid4()),
            scenario_id=db_scenario.id,
            name=request.name,
            description=f"{request.attack_type} attack on {request.industry} environment",
            status="pending",
            tactics=scenario_data.get("attack_stages", []),
            timeline=scenario_data.get("timeline", []),
            summary={}
        )
        db.add(db_attack)
        db.commit()
        db.refresh(db_attack)
        
        # 4. Generate mock events
        events = [
            {
                "timestamp": datetime.now().isoformat(),
                "log_source": "Windows Event Log",
                "event_type": "Process Creation",
                "event_id": "4688",
                "description": "Suspicious PowerShell execution from Word",
                "severity": "High",
                "mitre_technique": "T1059.001"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "log_source": "Sysmon",
                "event_type": "Network Connection",
                "event_id": "3",
                "description": "Outbound connection to malicious domain",
                "severity": "Critical",
                "mitre_technique": "T1071"
            }
        ]
        
        # 5. Analyze with SOC Analyst
        soc_analyst.update_context('attack_plan', scenario_data)
        analysis_result = await soc_analyst.process({"events": events})
        
        # 6. Update attack with analysis
        # Using SQLAlchemy's update method to avoid type issues
        db.query(Attack).filter(Attack.id == db_attack.id).update({
            "summary": analysis_result,
            "status": "completed",
            "completed_at": datetime.now()
        })
        db.commit()
        db.refresh(db_attack)
        
        return {
            "id": db_attack.id,
            "name": db_attack.name,
            "description": db_attack.description,
            "status": db_attack.status,
            "created_at": db_attack.created_at,
            "attack_stages": db_attack.tactics,
            "timeline": db_attack.timeline,
            "events": events,
            "analysis": analysis_result
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[dict])
async def list_attacks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all attacks"""
    attacks = db.query(Attack).offset(skip).limit(limit).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in attacks
    ]

@router.get("/{attack_id}")
async def get_attack(
    attack_id: str,
    db: Session = Depends(get_db)
):
    """Get attack details"""
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    
    return {
        "id": attack.id,
        "name": attack.name,
        "description": attack.description,
        "status": attack.status,
        "created_at": attack.created_at.isoformat() if attack.created_at else None,
        "tactics": attack.tactics,
        "timeline": attack.timeline,
        "summary": attack.summary
    }