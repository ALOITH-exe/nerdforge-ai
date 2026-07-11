import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { severityColors } from './chartColors';

export function SeverityDonut({ counts, centerLabel = 'total' }: { counts: Record<string, number>; centerLabel?: string }) {
  const data = Object.entries(counts)
    .filter(([, v]) => v > 0)
    .map(([name, value]) => ({ name, value }));

  if (data.length === 0) {
    return <div className="text-sm text-[var(--text-muted)] py-8 text-center">No data yet</div>;
  }

  const total = data.reduce((sum, d) => sum + d.value, 0);

  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" innerRadius={62} outerRadius={88} paddingAngle={3} strokeWidth={0}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={severityColors[entry.name]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: 'var(--bg-surface-raised)',
              border: '1px solid var(--border-strong)',
              borderRadius: 10,
              fontSize: 12,
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <div className="font-display text-2xl font-semibold text-[var(--text-primary)]">{total}</div>
        <div className="text-xs text-[var(--text-muted)]">{centerLabel}</div>
      </div>
      <div className="flex flex-wrap justify-center gap-3 mt-3">
        {data.map((d) => (
          <div key={d.name} className="flex items-center gap-1.5 text-xs text-[var(--text-secondary)]">
            <span className="w-2 h-2 rounded-full" style={{ background: severityColors[d.name] }} />
            {d.name} ({d.value})
          </div>
        ))}
      </div>
    </div>
  );
}
