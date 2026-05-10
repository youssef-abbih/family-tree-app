'use client';

import { Reducer, useCallback, useEffect, useReducer } from 'react';
import { Person } from '@/lib/types';
import { buildPersonMap, findLCA } from '@/lib/treeUtils';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';
import AncestorBar from './AncestorBar';
import Legend from './Legend';
import PersonModal from './PersonModal';
import Sidebar from './Sidebar';
import TreeNode from './TreeNode';

const MAX_GEN = 25;
const MAX_SELECTION = 6;

interface State {
  loadedUpTo: number;
  selectedIds: Set<string>;
  highlightedIds: Set<string>;
  ancestorId: string | null;
  favorites: Set<string>;
  modal: Person | null;
  sidebarOpen: boolean;
}

type Action =
  | { type: 'LOAD_MORE' }
  | { type: 'SELECT'; person: Person; map: Map<string, Person> }
  | { type: 'CLEAR_SELECTION' }
  | { type: 'TOGGLE_FAVORITE'; id: string }
  | { type: 'OPEN_MODAL'; person: Person }
  | { type: 'CLOSE_MODAL' }
  | { type: 'TOGGLE_SIDEBAR' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'LOAD_MORE':
      return { ...state, loadedUpTo: Math.min(state.loadedUpTo + 1, MAX_GEN) };

    case 'SELECT': {
      const pid = action.person.id;
      const wasSelected = state.selectedIds.has(pid);
      const next = new Set(state.selectedIds);

      if (wasSelected) {
        next.delete(pid);
      } else {
        if (next.size >= MAX_SELECTION) return state;
        next.add(pid);
      }

      const ids = [...next];
      const { lcaId, highlighted } = findLCA(ids, action.map);
      return {
        ...state,
        selectedIds: next,
        highlightedIds: highlighted,
        ancestorId: lcaId,
      };
    }

    case 'CLEAR_SELECTION':
      return { ...state, selectedIds: new Set(), highlightedIds: new Set(), ancestorId: null };

    case 'TOGGLE_FAVORITE': {
      const favs = new Set(state.favorites);
      if (favs.has(action.id)) favs.delete(action.id);
      else favs.add(action.id);
      return { ...state, favorites: favs };
    }

    case 'OPEN_MODAL': return { ...state, modal: action.person };
    case 'CLOSE_MODAL': return { ...state, modal: null };
    case 'TOGGLE_SIDEBAR': return { ...state, sidebarOpen: !state.sidebarOpen };

    default: return state;
  }
}

interface Props {
  persons: Person[];
  maxGeneration: number;
}

export default function TreeView({ persons, maxGeneration }: Props) {
  const { lang, dir } = useLanguage();
  const personMap = buildPersonMap(persons);
  const roots = persons.filter(p => p.generation === 1);

  const [state, dispatch] = useReducer<Reducer<State, Action>>(reducer, {
    loadedUpTo: 1,
    selectedIds: new Set(),
    highlightedIds: new Set(),
    ancestorId: null,
    favorites: new Set(),
    modal: null,
    sidebarOpen: false,
  });

  // ESC clears selection
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && state.selectedIds.size > 0) {
        dispatch({ type: 'CLEAR_SELECTION' });
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [state.selectedIds.size]);

  const handleSelect = useCallback((person: Person) => {
    dispatch({ type: 'SELECT', person, map: personMap });
  }, [personMap]);

  const handleInfo = useCallback((person: Person) => {
    dispatch({ type: 'OPEN_MODAL', person });
  }, []);

  const isMaxReached = state.selectedIds.size >= MAX_SELECTION;
  const canLoadMore = state.loadedUpTo < maxGeneration;

  return (
    <div dir={dir} className="w-full flex flex-col min-h-screen bg-amber-50 dark:bg-slate-900">
      <Legend />

      {/* Ancestor bar */}
      <div className="w-full bg-white dark:bg-slate-800 border-b border-amber-100 dark:border-slate-700">
        <AncestorBar
          count={state.selectedIds.size}
          onClear={() => dispatch({ type: 'CLEAR_SELECTION' })}
        />
      </div>

      {/* Sidebar toggle button */}
      <button
        onClick={() => dispatch({ type: 'TOGGLE_SIDEBAR' })}
        className={`fixed ${dir === 'rtl' ? 'left-4' : 'right-4'} bottom-6 z-30 bg-amber-600 hover:bg-amber-700 text-white rounded-full p-3.5 shadow-lg transition-all`}
        aria-label="Toggle sidebar"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
        </svg>
      </button>

      {/* Tree scroll area */}
      <div className="w-full overflow-x-auto flex-1">
        <div className="min-w-full flex flex-col items-center py-8 px-4">

          <div className="tree-children-row">
            {roots.map(root => (
              <TreeNode
                key={root.id}
                person={root}
                depth={0}
                maxDepth={state.loadedUpTo - 1}
                personMap={personMap}
                selectedIds={state.selectedIds}
                highlightedIds={state.highlightedIds}
                ancestorId={state.ancestorId}
                favorites={state.favorites}
                maxReached={isMaxReached}
                onSelect={handleSelect}
                onInfo={handleInfo}
              />
            ))}
          </div>

          {/* Load more / done */}
          <div className="mt-10 flex justify-center">
            {canLoadMore ? (
              <button
                onClick={() => dispatch({ type: 'LOAD_MORE' })}
                className="bg-amber-600 hover:bg-amber-700 text-white font-semibold px-10 py-3 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              >
                {t('load_next', lang)} ({t('generation', lang)} {state.loadedUpTo + 1})
              </button>
            ) : (
              <p className="text-amber-700 dark:text-amber-400 font-medium">{t('no_more', lang)}</p>
            )}
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <Sidebar
        persons={persons}
        favorites={state.favorites}
        isOpen={state.sidebarOpen}
        onClose={() => dispatch({ type: 'TOGGLE_SIDEBAR' })}
        onPersonClick={p => { dispatch({ type: 'OPEN_MODAL', person: p }); dispatch({ type: 'TOGGLE_SIDEBAR' }); }}
      />

      {/* Modal */}
      <PersonModal
        person={state.modal}
        favorites={state.favorites}
        onToggleFavorite={id => dispatch({ type: 'TOGGLE_FAVORITE', id })}
        onClose={() => dispatch({ type: 'CLOSE_MODAL' })}
      />
    </div>
  );
}
