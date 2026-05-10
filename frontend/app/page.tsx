'use client';

import Link from 'next/link';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

const STATS = [
  { labelKey: 'stat_generations', value: '25', icon: '🌿' },
  { labelKey: 'stat_personalities', value: '58+', icon: '👤' },
  { labelKey: 'stat_prophets', value: '5', icon: '☪️' },
  { labelKey: 'stat_companions', value: '17', icon: '⭐' },
];

const CATEGORIES = [
  { color: 'bg-emerald-500', labelKey: 'legend_prophet' },
  { color: 'bg-blue-500',    labelKey: 'legend_companion' },
  { color: 'bg-red-500',     labelKey: 'legend_leader' },
  { color: 'bg-amber-500',   labelKey: 'legend_poet' },
  { color: 'bg-purple-500',  labelKey: 'legend_scholar' },
] as const;

export default function LandingPage() {
  const { lang, dir } = useLanguage();

  return (
    <div dir={dir} className="w-full">
      {/* ── Hero ─────────────────────────────────────────────── */}
      <section className="relative w-full min-h-[90vh] flex flex-col items-center justify-center text-center px-4 overflow-hidden bg-gradient-to-b from-amber-800 via-amber-700 to-amber-600">
        {/* Decorative circles */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-10 left-10 w-64 h-64 bg-amber-500/20 rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-10 w-80 h-80 bg-orange-500/20 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 max-w-3xl">
          <div className="text-6xl mb-6 animate-bounce">🌳</div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white drop-shadow-lg leading-tight">
            {t('app_title', lang)}
          </h1>

          <p className="mt-4 text-lg sm:text-xl text-amber-100 max-w-xl mx-auto">
            {t('app_subtitle', lang)}
          </p>

          <Link
            href="/tree"
            className="mt-10 inline-block bg-white text-amber-800 font-bold px-10 py-4 rounded-full shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300 text-lg"
          >
            {t('view_tree', lang)}
          </Link>
        </div>
      </section>

      {/* ── Stats ────────────────────────────────────────────── */}
      <section className="w-full bg-white dark:bg-slate-800 py-12 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4">
          {STATS.map(({ labelKey, value, icon }) => (
            <div
              key={labelKey}
              className="bg-amber-50 dark:bg-slate-700 rounded-2xl p-5 text-center shadow hover:shadow-md transition-shadow"
            >
              <div className="text-3xl mb-2">{icon}</div>
              <div className="text-3xl font-extrabold text-amber-700 dark:text-amber-400">{value}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300 mt-1">{t(labelKey, lang)}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── About ────────────────────────────────────────────── */}
      <section className="w-full bg-amber-50 dark:bg-slate-900 py-16 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-amber-900 dark:text-amber-300 mb-4">
            {t('about_title', lang)}
          </h2>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {t('about_body', lang)}
          </p>

          {/* Category chips */}
          <div className="flex flex-wrap justify-center gap-2 mt-8">
            {CATEGORIES.map(({ color, labelKey }) => (
              <span
                key={labelKey}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white dark:bg-slate-800 shadow text-sm text-gray-700 dark:text-gray-300"
              >
                <span className={`w-2.5 h-2.5 rounded-full ${color}`} />
                {t(labelKey, lang)}
              </span>
            ))}
          </div>

          <Link
            href="/tree"
            className="mt-10 inline-block bg-amber-600 hover:bg-amber-700 text-white font-semibold px-8 py-3 rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            {t('view_tree', lang)}
          </Link>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────────── */}
      <footer className="w-full bg-amber-800 dark:bg-slate-950 py-6 text-center text-amber-200 text-sm">
        <p>🌳 {t('app_title', lang)} © 2024</p>
      </footer>
    </div>
  );
}
