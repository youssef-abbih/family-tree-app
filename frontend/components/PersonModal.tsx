'use client';

import { useEffect } from 'react';
import { Person } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

const TYPE_HEADER: Record<string, string> = {
  prophet:   'from-emerald-600 to-emerald-800',
  companion: 'from-blue-600    to-blue-800',
  poet:      'from-amber-500   to-amber-700',
  leader:    'from-red-600     to-red-800',
  scholar:   'from-purple-600  to-purple-800',
};

interface Props {
  person: Person | null;
  favorites: Set<string>;
  onToggleFavorite: (id: string) => void;
  onClose: () => void;
}

export default function PersonModal({ person, favorites, onToggleFavorite, onClose }: Props) {
  const { lang, dir } = useLanguage();

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [onClose]);

  if (!person) return null;

  const name = lang === 'ar' ? person.name_ar : person.name_en;
  const description = lang === 'ar' ? person.description_ar : person.description_en;
  const isFav = favorites.has(person.id);
  const header = TYPE_HEADER[person.type] ?? 'from-gray-600 to-gray-800';

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={e => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div
        dir={dir}
        className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-md overflow-hidden"
        role="dialog"
      >
        {/* Coloured header */}
        <div className={`bg-gradient-to-br ${header} p-5 text-white`}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold">{name}</h2>
              {person.title && <p className="text-sm opacity-80 mt-0.5">{person.title}</p>}
            </div>
            <button
              onClick={onClose}
              className="text-white/70 hover:text-white transition-colors mt-0.5"
              aria-label="Close"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Dates + generation */}
          <div className="flex flex-wrap gap-3 mt-3 text-sm opacity-90">
            <span>
              {lang === 'ar' ? `الجيل ${person.generation}` : `Generation ${person.generation}`}
            </span>
            {person.birth_year && (
              <span>{t('born', lang)}: {person.birth_year}</span>
            )}
            {person.death_year && (
              <span>{t('died', lang)}: {person.death_year}</span>
            )}
          </div>
        </div>

        {/* Body */}
        <div className="p-5">
          {description && (
            <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{description}</p>
          )}

          <div className="mt-5 flex items-center justify-between">
            <button
              onClick={() => onToggleFavorite(person.id)}
              className="flex items-center gap-1.5 text-sm text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-200 transition-colors"
            >
              <span>{isFav ? '⭐' : '☆'}</span>
              {isFav ? t('remove_favorite', lang) : t('add_favorite', lang)}
            </button>
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded-lg bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-200 text-sm hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
            >
              {t('close', lang)}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
