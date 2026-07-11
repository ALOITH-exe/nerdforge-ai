// recharts renders raw SVG attributes, so we pass concrete hex values here
// rather than CSS custom properties, keeping them in sync with index.css.
export const severityColors: Record<string, string> = {
  Low: '#34d399',
  Medium: '#fbbf24',
  High: '#fb923c',
  Critical: '#f43f5e',
};

export const chartPalette = {
  cyan: '#22d3ee',
  violet: '#8b5cf6',
  muted: '#6d7690',
};
