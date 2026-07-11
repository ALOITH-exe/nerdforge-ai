import type { AttackStage, SecurityEvent, TimelineEntry } from './types';

// Mirrors backend/app/api/attacks.py::_build_events_from_scenario so the
// Events view looks the same whether it's showing the just-generated
// response or events reconstructed after navigating back to an attack
// (GET /api/attacks/{id} only returns tactics + timeline, not raw events).
const LOG_SOURCE_BY_KEYWORD: [string, string][] = [
  ['initial access', 'Email Gateway'],
  ['execution', 'Sysmon'],
  ['persistence', 'Windows Event Log'],
  ['privilege escalation', 'Windows Event Log'],
  ['defense evasion', 'EDR'],
  ['credential access', 'Sysmon'],
  ['discovery', 'Windows Event Log'],
  ['lateral movement', 'Firewall'],
  ['collection', 'EDR'],
  ['command and control', 'Network IDS'],
  ['exfiltration', 'Firewall'],
  ['impact', 'EDR'],
];

export function deriveEvents(stages: AttackStage[], timeline: TimelineEntry[]): SecurityEvent[] {
  if (!stages || stages.length === 0) return [];

  const baseTime = new Date();

  return stages.map((stage, i) => {
    const stageName = (stage.stage || '').toLowerCase();
    const logSource = LOG_SOURCE_BY_KEYWORD.find(([kw]) => stageName.includes(kw))?.[1] || 'SIEM';

    let severity: string;
    if (i < stages.length * 0.3) severity = 'Medium';
    else if (i < stages.length * 0.7) severity = 'High';
    else severity = 'Critical';

    const timelineEntry = timeline?.[i];
    const description =
      timelineEntry?.description || stage.description || stage.technique || 'Suspicious activity';

    const ts = new Date(baseTime.getTime() + i * 3 * 60_000);

    return {
      timestamp: ts.toISOString(),
      log_source: logSource,
      event_type: stage.technique || 'Unknown',
      event_id: String(4600 + i),
      description,
      severity,
      mitre_technique: stage.mitre_technique || '',
      attack_stage: stage.stage || '',
    };
  });
}
