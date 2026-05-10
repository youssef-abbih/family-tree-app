'use client';

import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

const MAX = 6;

interface Props {
  count: number;
  onClear: () => void;
}

export default function AncestorBar({ count, onClear }: Props) {
  const { lang, dir } = useLanguage();

  if (count === 0) {
    return (
      <div dir={dir} className="w-full text-center py-2 px-4">
        <p className="text-xs text-amber-600 dark:text-amber-400 italic">
          {t('hint_select', lang)}
        </p>
      </div>
    );
  }

  return (
    <div dir={dir} className="w-full flex items-center justify-center gap-3 py-2 px-4">
      <span className="text-sm font-semibold text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900 px-3 py-1 rounded-full">
        {count} / {MAX} {t('selected_of', lang)}
      </span>
      <button
        onClick={onClear}
        className="flex items-center gap-1 text-sm text-purple-700 dark:text-purple-300 border border-purple-300 dark:border-purple-700 rounded-full px-3 py-1 hover:bg-purple-50 dark:hover:bg-purple-900/40 transition-colors"
      >
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
        {t('clear_all', lang)}
      </button>
    </div>
  );
}
