'use client';

import Link from 'next/link';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

export default function Header() {
  const { lang, toggle, dir } = useLanguage();

  return (
    <header
      dir={dir}
      className="sticky top-0 z-50 w-full bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-amber-200 dark:border-slate-700 shadow-sm"
    >
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 shrink-0">
          <span className="text-xl">🌳</span>
          <span className="font-bold text-amber-800 dark:text-amber-400 text-sm sm:text-base">
            {t('app_title', lang)}
          </span>
        </Link>

        {/* Nav + actions */}
        <div className="flex items-center gap-2">
          <Link
            href="/tree"
            className="text-sm text-amber-700 dark:text-amber-300 hover:text-amber-900 dark:hover:text-amber-100 font-medium px-3 py-1.5 rounded-lg hover:bg-amber-50 dark:hover:bg-slate-800 transition-colors"
          >
            {lang === 'ar' ? 'الشجرة' : 'Tree'}
          </Link>

          <button
            onClick={toggle}
            className="text-sm px-3 py-1.5 rounded-lg border border-amber-300 dark:border-slate-600 text-amber-800 dark:text-amber-300 hover:bg-amber-50 dark:hover:bg-slate-800 transition-colors"
          >
            {t('language', lang)}
          </button>
        </div>
      </div>
    </header>
  );
}
