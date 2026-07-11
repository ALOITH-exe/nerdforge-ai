// Default team roster for the About page.
//
// To update permanently: edit the array below and redeploy.
// To update without touching code: use the "Edit team" button on the About
// page in the running app - changes save to the browser via localStorage
// and override these defaults (per-device, until "Reset to defaults" is used).
//
// Photo images: drop files into /public/team/ and reference them here as
// "/team/yourfile.jpg", or paste any external image URL.

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  photoUrl: string;
  links: {
    github?: string;
    linkedin?: string;
    email?: string;
  };
}

export const projectInfo = {
  name: 'NerdForge AI',
  tagline: 'Autonomous AI Security Operations Center',
  summary:
    'Built for the DYLP Vibe Coding Hackathon 2026, NerdForge AI combines attack simulation, ' +
    'AI-driven detection, and automated incident reporting into a single console - so a security ' +
    'analyst can go from "generate a scenario" to "here is the incident report" without leaving the browser.',
};

export const teamMembers: TeamMember[] = [
  {
    id: 'member-1',
    name: 'Your Name',
    role: 'Team Lead / Backend',
    bio: 'Add a short bio here - what you built, what you focused on for this project.',
    photoUrl: '',
    links: {},
  },
  {
    id: 'member-2',
    name: 'Teammate Name',
    role: 'Frontend Engineer',
    bio: 'Add a short bio here.',
    photoUrl: '',
    links: {},
  },
];
