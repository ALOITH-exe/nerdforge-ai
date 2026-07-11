import type { ReactNode } from 'react';
import { motion } from 'framer-motion';

export function StatCard({
  label,
  value,
  icon,
  accent = 'cyan',
  trend,
}: {
  label: string;
  value: string | number;
  icon: ReactNode;
  accent?: 'cyan' | 'violet' | 'neutral';
  trend?: string;
}) {
  const accentClasses = {
    cyan: 'text-[var(--accent-cyan)] bg-[var(--accent-cyan-soft)]',
    violet: 'text-[var(--accent-violet)] bg-[var(--accent-violet-soft)]',
    neutral: 'text-[var(--text-secondary)] bg-[var(--bg-hover)]',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-[var(--bg-surface)] border border-[var(--border-subtle)] rounded-2xl p-5 shadow-[var(--shadow-card)]"
    >
      <div className="flex items-center justify-between mb-3">
        <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${accentClasses[accent]}`}>
          {icon}
        </div>
        {trend && <span className="text-xs font-medium text-[var(--text-muted)]">{trend}</span>}
      </div>
      <div className="font-display text-2xl font-semibold text-[var(--text-primary)] tabular-nums">
        {value}
      </div>
      <div className="text-sm text-[var(--text-muted)] mt-0.5">{label}</div>
    </motion.div>
  );
}
