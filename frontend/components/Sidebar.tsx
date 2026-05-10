'use client';

import { useState } from 'react';
import { Person } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';
import PersonCard from './PersonCard';

const TYPES = ['all', 'prophet', 'companion', 'leader', 'poet', 'scholar'] as const;

interface Props {
  persons: Person[];
  favorites: Set<string>;
  isOpen: boolean;
  onClose: () => void;
  onPersonClick: (p: Person) => void;
}

export default function Sidebar({ persons, favorites, isOpen, onClose, onPersonClick }: Props) {
  const { lang, dir } = useLanguage();
  const [query, setQuery] = useState('');
  const [activeType, setActiveType] = useState<string>('all');

  const filtered = persons.filter(p => {
    const matchType = activeType === 'all' || p.type === activeType;
    const q = query.trim().toLowerCase();
    const matchQuery = !q
      || p.name_en.toLowerCase().includes(q)
      || p.name_ar.includes(query.trim());
    return matchType && matchQuery;
  });

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30"
          onClick={onClose}
        />
      )}

      {/* Drawer */}
      <aside
        dir={dir}
        className={`
          fixed top-0 z-50 h-full w-80 bg-white dark:bg-slate-800
          border-amber-200 dark:border-slate-700
          shadow-2xl transition-transform duration-300
          flex flex-col
          ${dir === 'rtl'
            ? `left-0 border-r ${isOpen ? 'translate-x-0' : '-translate-x-full'}`
            : `right-0 border-l ${isOpen ? 'translate-x-0' : 'translate-x-full'}`
          }
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-amber-100 dark:border-slate-700">
          <h2 className="font-semibold text-amber-900 dark:text-amber-300">
            {lang === 'ar' ? 'البحث والفلترة' : 'Search & Filter'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-amber-100 dark:border-slate-700">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder={t('search_placeholder', lang)}
            className="w-full px-3 py-2 rounded-lg border border-amber-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        {/* Type filter */}
        <div className="px-4 py-3 border-b border-amber-100 dark:border-slate-700 flex flex-wrap gap-1.5">
          {TYPES.map(type => (
            <button
              key={type}
              onClick={() => setActiveType(type)}
              className={`text-xs px-2.5 py-1 rounded-full border transition-colors ${
                activeType === type
                  ? 'bg-amber-600 text-white border-amber-600'
                  : 'border-amber-200 dark:border-slate-600 text-amber-700 dark:text-amber-300 hover:bg-amber-50 dark:hover:bg-slate-700'
              }`}
            >
              {type === 'all' ? t('filter_all', lang) : t(`legend_${type}`, lang)}
            </button>
          ))}
        </div>

        {/* Results */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {filtered.length === 0 ? (
            <p className="text-center text-gray-400 text-sm py-8">{t('no_results', lang)}</p>
          ) : (
            filtered.map(p => (
              <div key={p.id} onClick={() => onPersonClick(p)} className="cursor-pointer">
                <PersonCard
                  person={p}
                  isFavorite={favorites.has(p.id)}
                />
              </div>
            ))
          )}
        </div>
      </aside>
    </>
  );
}
