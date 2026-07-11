import { useState } from 'react';

export function CodeBlock({ content, language }: { content: string; language?: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className="relative rounded-xl overflow-hidden border border-[var(--border-subtle)] bg-[var(--bg-void)]">
      <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--border-subtle)] bg-[var(--bg-surface-raised)]">
        <span className="text-xs font-mono text-[var(--text-muted)] uppercase tracking-wide">
          {language || 'text'}
        </span>
        <button
          onClick={handleCopy}
          className="text-xs font-medium px-2 py-1 rounded-md text-[var(--text-secondary)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] transition-colors"
        >
          {copied ? 'Copied ✓' : 'Copy'}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-xs leading-relaxed font-mono text-[var(--text-secondary)]">
        <code>{content}</code>
      </pre>
    </div>
  );
}
