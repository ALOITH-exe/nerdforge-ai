import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useTheme } from '../../context/useTheme';

const mobileNavItems = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/generate', label: 'Generate Attack' },
  { to: '/attacks', label: 'Attack History' },
  { to: '/about', label: 'About Us' },
];

export function Topbar({ title, subtitle }: { title: string; subtitle?: string }) {
  const { theme, toggleTheme } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 h-16 flex items-center justify-between gap-4 px-4 lg:px-8 border-b border-[var(--border-subtle)] bg-[var(--bg-void)]/85 backdrop-blur-md">
      <div className="flex items-center gap-3 min-w-0">
        <button
          onClick={() => setMobileOpen((v) => !v)}
          className="lg:hidden shrink-0 w-9 h-9 rounded-lg flex items-center justify-center text-[var(--text-secondary)] hover:bg-[var(--bg-hover)]"
          aria-label="Toggle navigation"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
        <div className="min-w-0">
          <h1 className="font-display font-semibold text-lg text-[var(--text-primary)] truncate">{title}</h1>
          {subtitle && <p className="text-xs text-[var(--text-muted)] truncate">{subtitle}</p>}
        </div>
      </div>

      <button
        onClick={toggleTheme}
        aria-label="Toggle color theme"
        className="relative shrink-0 w-16 h-9 rounded-full bg-[var(--bg-surface-raised)] border border-[var(--border-strong)] flex items-center px-1 transition-colors"
      >
        <span
          className={`absolute w-7 h-7 rounded-full bg-gradient-to-br from-cyan-400 to-violet-500 shadow-md transition-transform duration-300 flex items-center justify-center text-white ${
            theme === 'dark' ? 'translate-x-[28px]' : 'translate-x-0'
          }`}
        >
          {theme === 'dark' ? <MoonIcon /> : <SunIcon />}
        </span>
      </button>

      {mobileOpen && (
        <div className="lg:hidden absolute top-16 left-0 right-0 bg-[var(--bg-surface)] border-b border-[var(--border-subtle)] shadow-[var(--shadow-elevated)] flex flex-col p-3 gap-1">
          {mobileNavItems.map(({ to, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `px-4 py-3 rounded-xl text-sm font-medium ${
                  isActive
                    ? 'bg-[var(--accent-cyan-soft)] text-[var(--accent-cyan)]'
                    : 'text-[var(--text-secondary)] hover:bg-[var(--bg-hover)]'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </div>
      )}
    </header>
  );
}

function SunIcon() {
  return (
    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1.5m0 15V21m8.25-9h-1.5m-15 0H3m15.36-6.36l-1.06 1.06M6.7 17.3l-1.06 1.06m12.72 0L17.3 17.3M6.7 6.7L5.64 5.64M16.5 12a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z" />
    </svg>
  );
}
function MoonIcon() {
  return (
    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.72 9.72 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
    </svg>
  );
}
