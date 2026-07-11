# backend/app/database/models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    operating_system = Column(String(50))
    attack_type = Column(String(100))
    difficulty = Column(String(50))
    environment = Column(String(50))
    
    # AI-generated content
    company_profile = Column(JSON)
    network_topology = Column(JSON)
    assets = Column(JSON)
    security_controls = Column(JSON)
    attack_stages = Column(JSON)
    objectives = Column(JSON)
    indicators = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attacks = relationship("Attack", back_populates="scenario", cascade="all, delete-orphan")

class Attack(Base):
    __tablename__ = "attacks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    scenario_id = Column(String(36), ForeignKey("scenarios.id"))
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    
    # Attack data
    tactics = Column(JSON)
    techniques = Column(JSON)
    timeline = Column(JSON)
    summary = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="attacks")
    events = relationship("Event", back_populates="attack", cascade="all, delete-orphan")
    detections = relationship("Detection", back_populates="attack", cascade="all, delete-orphan")
    iocs = relationship("IOC", back_populates="attack", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="attack", cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    attack_id = Column(String(36), ForeignKey("attacks.id"))
    
    timestamp = Column(DateTime)
    log_source = Column(String(50))
    event_type = Column(String(50))
    event_id = Column(String(20))
    
    log_data = Column(JSON)
    description = Column(Text)
    severity = Column(String(20))
    
    mitre_technique = Column(String(50))
    attack_stage = Column(String(50))
    is_malicious = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attack = relationship("Attack", back_populates="events")

class Detection(Base):
    __tablename__ = "detections"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    attack_id = Column(String(36), ForeignKey("attacks.id"))
    
    rule_name = Column(String(255), nullable=False)
    rule_format = Column(String(50))
    rule_content = Column(Text, nullable=False)
    
    description = Column(Text)
    severity = Column(String(20))
    confidence = Column(Integer)
    
    mitre_technique = Column(String(50))
    mitre_tactic = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attack = relationship("Attack", back_populates="detections")

class IOC(Base):
    __tablename__ = "iocs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    attack_id = Column(String(36), ForeignKey("attacks.id"))
    
    indicator_type = Column(String(50))
    value = Column(String(512), nullable=False)
    
    threat_intel = Column(JSON)
    risk_score = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attack = relationship("Attack", back_populates="iocs")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    attack_id = Column(String(36), ForeignKey("attacks.id"))
    
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    technical_details = Column(JSON)
    recommendations = Column(JSON)
    
    pdf_path = Column(String(255), nullable=True)
    markdown_path = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attack = relationship("Attack", back_populates="reports")