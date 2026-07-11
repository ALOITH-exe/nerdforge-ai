import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { chartPalette, severityColors } from './chartColors';
import type { AttackStage, IOC } from '../../lib/types';

const axisTick = { fill: 'var(--text-muted)', fontSize: 11 };

export function MitreCoverageChart({ stages }: { stages: AttackStage[] }) {
  const counts: Record<string, number> = {};
  stages.forEach((s) => {
    const tactic = s.mitre_tactic || 'Unknown';
    counts[tactic] = (counts[tactic] || 0) + 1;
  });
  const data = Object.entries(counts).map(([tactic, count]) => ({ tactic, count }));

  if (data.length === 0) {
    return <div className="text-sm text-[var(--text-muted)] py-8 text-center">No stages yet</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" vertical={false} />
        <XAxis dataKey="tactic" tick={axisTick} axisLine={{ stroke: 'var(--border-subtle)' }} tickLine={false} />
        <YAxis allowDecimals={false} tick={axisTick} axisLine={false} tickLine={false} />
        <Tooltip
          cursor={{ fill: 'var(--bg-hover)' }}
          contentStyle={{
            background: 'var(--bg-surface-raised)',
            border: '1px solid var(--border-strong)',
            borderRadius: 10,
            fontSize: 12,
          }}
        />
        <Bar dataKey="count" radius={[6, 6, 0, 0]} fill={chartPalette.violet} maxBarSize={40} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function IOCRiskChart({ iocs }: { iocs: IOC[] }) {
  const data = [...iocs]
    .sort((a, b) => b.risk_score - a.risk_score)
    .slice(0, 8)
    .map((i) => ({ value: i.value.length > 18 ? i.value.slice(0, 17) + '…' : i.value, risk: i.risk_score }));

  if (data.length === 0) {
    return <div className="text-sm text-[var(--text-muted)] py-8 text-center">No IOCs yet</div>;
  }

  const colorFor = (risk: number) => {
    if (risk >= 80) return severityColors.Critical;
    if (risk >= 60) return severityColors.High;
    if (risk >= 35) return severityColors.Medium;
    return severityColors.Low;
  };

  return (
    <ResponsiveContainer width="100%" height={Math.max(220, data.length * 34)}>
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" horizontal={false} />
        <XAxis type="number" domain={[0, 100]} tick={axisTick} axisLine={false} tickLine={false} />
        <YAxis
          type="category"
          dataKey="value"
          tick={{ ...axisTick, fontFamily: 'var(--font-mono)' }}
          axisLine={false}
          tickLine={false}
          width={140}
        />
        <Tooltip
          cursor={{ fill: 'var(--bg-hover)' }}
          contentStyle={{
            background: 'var(--bg-surface-raised)',
            border: '1px solid var(--border-strong)',
            borderRadius: 10,
            fontSize: 12,
          }}
        />
        <Bar dataKey="risk" radius={[0, 6, 6, 0]} maxBarSize={16}>
          {data.map((d, i) => (
            <Cell key={i} fill={colorFor(d.risk)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
