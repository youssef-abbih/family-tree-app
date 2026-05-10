import { api } from '@/lib/api';
import TreeView from '@/components/TreeView';

export default async function TreePage() {
  const [persons, { max_generation }] = await Promise.all([
    api.persons(),
    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'}/api/generations`, { cache: 'no-store' })
      .then(r => r.json()) as Promise<{ max_generation: number }>,
  ]);

  return <TreeView persons={persons} maxGeneration={max_generation} />;
}
