import type { ReactNode } from 'react';

export function Badge({
  children,
  color = 'neutral',
}: {
  children: ReactNode;
  color?: 'neutral' | 'cyan' | 'violet' | 'success';
}) {
  const colorMap = {
    neutral: 'bg-[var(--bg-hover)] text-[var(--text-secondary)] border-[var(--border-strong)]',
    cyan: 'bg-[var(--accent-cyan-soft)] text-[var(--accent-cyan)] border-[var(--accent-cyan)]/30',
    violet: 'bg-[var(--accent-violet-soft)] text-[var(--accent-violet)] border-[var(--accent-violet)]/30',
    success: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30',
  };
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border ${colorMap[color]}`}
    >
      {children}
    </span>
  );
}

const severityStyles: Record<string, { bg: string; text: string; dot: string }> = {
  low: { bg: 'bg-emerald-500/10', text: 'text-emerald-500', dot: 'bg-emerald-500' },
  medium: { bg: 'bg-amber-500/10', text: 'text-amber-500', dot: 'bg-amber-500' },
  high: { bg: 'bg-orange-500/10', text: 'text-orange-500', dot: 'bg-orange-500' },
  critical: { bg: 'bg-rose-500/10', text: 'text-rose-500', dot: 'bg-rose-500' },
};

export function SeverityBadge({ severity }: { severity: string }) {
  const key = (severity || 'medium').toLowerCase();
  const style = severityStyles[key] || severityStyles.medium;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${style.bg} ${style.text}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${style.dot} animate-pulse-slow`} />
      {severity}
    </span>
  );
}
