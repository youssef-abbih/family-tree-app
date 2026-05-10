import { LCAResult, Person, Stats } from './types';

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`API ${path} → ${res.status}`);
  return res.json();
}

export const api = {
  persons: (): Promise<Person[]> => get('/api/persons'),
  person: (id: string): Promise<Person> => get(`/api/persons/${id}`),
  stats: (): Promise<Stats> => get('/api/stats'),

  lca: async (ids: string[]): Promise<LCAResult> => {
    const res = await fetch(`${BASE}/api/lca`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids }),
    });
    if (!res.ok) throw new Error('LCA request failed');
    return res.json();
  },
};
