// Types mirror backend/API_CONTRACT.md exactly. Keep in sync with the backend.

export type Severity = 'Low' | 'Medium' | 'High' | 'Critical';

export interface AttackStage {
  stage: string;
  technique: string;
  mitre_tactic: string;
  mitre_technique: string;
  description: string;
  commands?: string[];
  tools?: string[];
}

export interface TimelineEntry {
  time: string;
  action: string;
  description: string;
}

export interface SecurityEvent {
  timestamp: string;
  log_source: string;
  event_type: string;
  event_id: string;
  description: string;
  severity: Severity | string;
  mitre_technique: string;
  attack_stage?: string;
}

export interface SOCAnalysis {
  summary?: string;
  detections?: unknown[];
  attack_chain?: string[];
  severity_score?: number;
  priority?: string;
  recommended_actions?: string[];
  [key: string]: unknown;
}

export interface GenerateAttackRequest {
  name: string;
  industry: string;
  attack_type: string;
  difficulty: string;
  operating_system: string;
  environment: string;
  custom_scenario?: string;
}

export interface AttackGenerateResponse {
  id: string;
  name: string;
  description: string;
  status: string;
  created_at: string;
  attack_stages: AttackStage[];
  timeline: TimelineEntry[];
  events: SecurityEvent[];
  analysis: SOCAnalysis;
}

export interface AttackListItem {
  id: string;
  name: string;
  status: string;
  created_at: string;
}

export interface AttackDetail {
  id: string;
  name: string;
  description: string;
  status: string;
  created_at: string;
  tactics: AttackStage[];
  timeline: TimelineEntry[];
  summary: SOCAnalysis;
}

export interface IOC {
  id: string;
  indicator_type: string;
  value: string;
  threat_intel: { context?: string };
  risk_score: number;
  created_at: string;
}

export interface DetectionRule {
  id: string;
  rule_name: string;
  rule_format: 'sigma' | 'yara' | string;
  rule_content: string;
  description: string;
  severity: string;
  confidence: number;
  mitre_technique: string;
  mitre_tactic: string;
  created_at: string;
}

export interface IncidentReport {
  id: string;
  title: string;
  summary: string;
  technical_details?: {
    attack_narrative?: string;
    affected_systems?: string[];
    attack_chain?: string[];
    root_cause?: string;
  };
  recommendations?: string[];
  created_at: string;
}

export interface ReportListItem {
  id: string;
  title: string;
  summary: string;
  created_at: string;
}
