import { useState } from 'react';
import { motion } from 'framer-motion';
import { AppLayout } from '../components/layout/AppLayout';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { projectInfo, teamMembers as defaultTeam, type TeamMember } from '../data/team';

const STORAGE_KEY = 'nerdforge-team-overrides';

function loadTeam(): TeamMember[] {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore malformed storage */
  }
  return defaultTeam;
}

export function AboutUs() {
  const [team, setTeam] = useState<TeamMember[]>(() => loadTeam());
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState<TeamMember[]>(() => loadTeam());

  const startEditing = () => {
    setDraft(team);
    setEditing(true);
  };

  const save = () => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(draft));
    setTeam(draft);
    setEditing(false);
  };

  const cancel = () => {
    setDraft(team);
    setEditing(false);
  };

  const resetToDefaults = () => {
    window.localStorage.removeItem(STORAGE_KEY);
    setTeam(defaultTeam);
    setDraft(defaultTeam);
    setEditing(false);
  };

  const updateMember = (id: string, patch: Partial<TeamMember>) => {
    setDraft((d) => d.map((m) => (m.id === id ? { ...m, ...patch } : m)));
  };

  const updateLink = (id: string, key: keyof TeamMember['links'], value: string) => {
    setDraft((d) => d.map((m) => (m.id === id ? { ...m, links: { ...m.links, [key]: value } } : m)));
  };

  const addMember = () => {
    setDraft((d) => [
      ...d,
      { id: `member-${Date.now()}`, name: 'New Member', role: 'Role', bio: '', photoUrl: '', links: {} },
    ]);
  };

  const removeMember = (id: string) => {
    setDraft((d) => d.filter((m) => m.id !== id));
  };

  return (
    <AppLayout title="About Us" subtitle="The team behind NerdForge AI">
      <div className="flex flex-col gap-8 max-w-4xl mx-auto">
        <Card>
          <h2 className="font-display text-xl font-semibold text-[var(--text-primary)] mb-2">
            {projectInfo.name}
          </h2>
          <p className="text-sm text-[var(--accent-cyan)] font-medium mb-3">{projectInfo.tagline}</p>
          <p className="text-sm text-[var(--text-secondary)] leading-relaxed">{projectInfo.summary}</p>
        </Card>

        <div className="flex items-center justify-between">
          <h3 className="font-display text-lg font-semibold text-[var(--text-primary)]">Team</h3>
          {!editing ? (
            <Button variant="secondary" size="sm" onClick={startEditing}>
              Edit team
            </Button>
          ) : (
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={resetToDefaults}>
                Reset
              </Button>
              <Button variant="secondary" size="sm" onClick={cancel}>
                Cancel
              </Button>
              <Button size="sm" onClick={save}>
                Save
              </Button>
            </div>
          )}
        </div>

        {!editing ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {team.map((member, i) => (
              <motion.div
                key={member.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
              >
                <Card hoverable className="flex gap-4 items-start h-full">
                  <Avatar name={member.name} photoUrl={member.photoUrl} />
                  <div className="min-w-0">
                    <div className="font-semibold text-[var(--text-primary)]">{member.name}</div>
                    <div className="text-xs font-medium text-[var(--accent-violet)] mb-2">{member.role}</div>
                    {member.bio && <p className="text-sm text-[var(--text-muted)] leading-relaxed">{member.bio}</p>}
                    <div className="flex items-center gap-3 mt-3">
                      {member.links.github && (
                        <a href={member.links.github} target="_blank" rel="noreferrer" className="text-[var(--text-muted)] hover:text-[var(--accent-cyan)]">
                          GitHub
                        </a>
                      )}
                      {member.links.linkedin && (
                        <a href={member.links.linkedin} target="_blank" rel="noreferrer" className="text-[var(--text-muted)] hover:text-[var(--accent-cyan)]">
                          LinkedIn
                        </a>
                      )}
                      {member.links.email && (
                        <a href={`mailto:${member.links.email}`} className="text-[var(--text-muted)] hover:text-[var(--accent-cyan)]">
                          Email
                        </a>
                      )}
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col gap-5">
            {draft.map((member) => (
              <Card key={member.id}>
                <div className="flex items-start gap-4 mb-4">
                  <Avatar name={member.name} photoUrl={member.photoUrl} />
                  <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <EditField label="Name" value={member.name} onChange={(v) => updateMember(member.id, { name: v })} />
                    <EditField label="Role" value={member.role} onChange={(v) => updateMember(member.id, { role: v })} />
                    <EditField
                      label="Photo URL"
                      value={member.photoUrl}
                      onChange={(v) => updateMember(member.id, { photoUrl: v })}
                      placeholder="/team/name.jpg or https://…"
                      className="sm:col-span-2"
                    />
                    <EditField
                      label="Bio"
                      value={member.bio}
                      onChange={(v) => updateMember(member.id, { bio: v })}
                      textarea
                      className="sm:col-span-2"
                    />
                    <EditField
                      label="GitHub URL"
                      value={member.links.github || ''}
                      onChange={(v) => updateLink(member.id, 'github', v)}
                    />
                    <EditField
                      label="LinkedIn URL"
                      value={member.links.linkedin || ''}
                      onChange={(v) => updateLink(member.id, 'linkedin', v)}
                    />
                    <EditField
                      label="Email"
                      value={member.links.email || ''}
                      onChange={(v) => updateLink(member.id, 'email', v)}
                    />
                  </div>
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={() => removeMember(member.id)}
                    className="text-xs font-medium text-rose-400 hover:text-rose-300"
                  >
                    Remove member
                  </button>
                </div>
              </Card>
            ))}
            <button
              onClick={addMember}
              className="border border-dashed border-[var(--border-strong)] rounded-2xl py-4 text-sm font-medium text-[var(--text-muted)] hover:text-[var(--accent-cyan)] hover:border-[var(--accent-cyan)] transition-colors"
            >
              + Add team member
            </button>
            <p className="text-xs text-[var(--text-muted)]">
              Changes save to this browser only. To make them permanent for everyone, update{' '}
              <code className="font-mono px-1 py-0.5 rounded bg-[var(--bg-hover)]">src/data/team.ts</code> in the repo.
            </p>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

function Avatar({ name, photoUrl }: { name: string; photoUrl?: string }) {
  const initials = name
    .split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  if (photoUrl) {
    return (
      <img
        src={photoUrl}
        alt={name}
        className="w-14 h-14 rounded-xl object-cover shrink-0 border border-[var(--border-subtle)]"
        onError={(e) => {
          (e.target as HTMLImageElement).style.display = 'none';
        }}
      />
    );
  }

  return (
    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 border border-[var(--border-subtle)] flex items-center justify-center font-display font-semibold text-[var(--accent-cyan)] shrink-0">
      {initials || '?'}
    </div>
  );
}

function EditField({
  label,
  value,
  onChange,
  placeholder,
  textarea,
  className = '',
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  textarea?: boolean;
  className?: string;
}) {
  const inputClasses =
    'w-full bg-[var(--bg-void)] border border-[var(--border-strong)] rounded-lg px-3 py-2 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] outline-none focus:border-[var(--accent-cyan)] transition-colors';
  return (
    <div className={className}>
      <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">{label}</label>
      {textarea ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          rows={2}
          className={`${inputClasses} resize-none`}
        />
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={inputClasses}
        />
      )}
    </div>
  );
}
