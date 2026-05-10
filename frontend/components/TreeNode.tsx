'use client';

import { Person } from '@/lib/types';
import { getChildren } from '@/lib/treeUtils';
import PersonCard from './PersonCard';

interface Props {
  person: Person;
  depth: number;
  maxDepth: number;
  personMap: Map<string, Person>;
  selectedIds: Set<string>;
  highlightedIds: Set<string>;
  ancestorId: string | null;
  favorites: Set<string>;
  maxReached: boolean;
  onSelect: (p: Person) => void;
  onInfo: (p: Person) => void;
}

export default function TreeNode({
  person,
  depth,
  maxDepth,
  personMap,
  selectedIds,
  highlightedIds,
  ancestorId,
  favorites,
  maxReached,
  onSelect,
  onInfo,
}: Props) {
  const pid = person.id;
  const parentId = person.father_id;

  const isSelected  = selectedIds.has(pid);
  const isAncestor  = pid === ancestorId;
  const isOnPath    = highlightedIds.has(pid) && !isSelected && !isAncestor;
  const parentHl    = parentId ? highlightedIds.has(parentId) : false;
  const selfHl      = highlightedIds.has(pid);

  const nodeHl = parentHl && selfHl ? 'tree-node-hl' : '';
  const dropHl = selfHl ? 'tree-drop-hl' : '';

  const children = depth < maxDepth ? getChildren(pid, personMap) : [];

  return (
    <div className={`tree-node ${nodeHl}`}>
      {/* Vertical line from parent */}
      {depth > 0 && (
        <div className={`tree-drop-to-card ${dropHl}`} />
      )}

      <PersonCard
        person={person}
        isSelected={isSelected}
        isOnPath={isOnPath}
        isAncestor={isAncestor}
        isMaxReached={maxReached && !isSelected && !isAncestor}
        isFavorite={favorites.has(pid)}
        onClick={onSelect}
        onInfoClick={onInfo}
      />

      {/* Children subtree */}
      {children.length > 0 && (
        <>
          <div className={`tree-drop-from-card ${dropHl}`} />
          <div className="tree-children-row">
            {children.map(child => (
              <TreeNode
                key={child.id}
                person={child}
                depth={depth + 1}
                maxDepth={maxDepth}
                personMap={personMap}
                selectedIds={selectedIds}
                highlightedIds={highlightedIds}
                ancestorId={ancestorId}
                favorites={favorites}
                maxReached={maxReached}
                onSelect={onSelect}
                onInfo={onInfo}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
