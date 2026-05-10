import { Person } from './types';

export function buildPersonMap(persons: Person[]): Map<string, Person> {
  return new Map(persons.map(p => [p.id, p]));
}

export function getChildren(personId: string, map: Map<string, Person>): Person[] {
  const parent = map.get(personId);
  if (!parent) return [];
  return parent.children_ids
    .map(id => map.get(id))
    .filter((p): p is Person => p !== undefined);
}

export function getPathToRoot(personId: string, map: Map<string, Person>): string[] {
  const path: string[] = [];
  const seen = new Set<string>();
  let curr: string | null = personId;
  while (curr && !seen.has(curr)) {
    path.push(curr);
    seen.add(curr);
    curr = map.get(curr)?.father_id ?? null;
  }
  return path;
}

export function findLCA(ids: string[], map: Map<string, Person>): { lcaId: string | null; highlighted: Set<string> } {
  if (ids.length === 0) return { lcaId: null, highlighted: new Set() };
  if (ids.length === 1) {
    return { lcaId: null, highlighted: new Set(getPathToRoot(ids[0], map)) };
  }

  const paths = ids.map(id => getPathToRoot(id, map));
  const sets = paths.map(p => new Set(p));

  let common = new Set(sets[0]);
  for (const s of sets.slice(1)) {
    for (const id of Array.from(common)) {
      if (!s.has(id)) common.delete(id);
    }
  }

  if (common.size === 0) return { lcaId: null, highlighted: new Set(ids) };

  const lcaId = Array.from(common).reduce((best, id) => {
    const gen = map.get(id)?.generation ?? 0;
    return gen > (map.get(best)?.generation ?? 0) ? id : best;
  });

  const highlighted = new Set<string>();
  for (const path of paths) {
    for (const node of path) {
      highlighted.add(node);
      if (node === lcaId) break;
    }
  }

  return { lcaId, highlighted };
}
