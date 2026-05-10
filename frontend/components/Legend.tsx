'use client';

import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

const ITEMS = [
  { key: 'legend_prophet',   dot: 'bg-emerald-500' },
  { key: 'legend_companion', dot: 'bg-blue-500' },
  { key: 'legend_leader',    dot: 'bg-red-500' },
  { key: 'legend_poet',      dot: 'bg-amber-500' },
  { key: 'legend_scholar',   dot: 'bg-purple-500' },
] as const;

export default function Legend() {
  const { lang, dir } = useLanguage();

  return (
    <div dir={dir} className="w-full bg-white dark:bg-slate-800 border-b border-amber-100 dark:border-slate-700 px-4 py-2">
      <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-1">
        {ITEMS.map(({ key, dot }) => (
          <div key={key} className="flex items-center gap-1.5">
            <span className={`w-2.5 h-2.5 rounded-full ${dot} shrink-0`} />
            <span className="text-xs text-gray-600 dark:text-gray-300">{t(key, lang)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
