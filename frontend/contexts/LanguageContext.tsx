'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { Language } from '@/lib/types';

interface LanguageContextValue {
  lang: Language;
  toggle: () => void;
  dir: 'rtl' | 'ltr';
}

const LanguageContext = createContext<LanguageContextValue>({
  lang: 'ar',
  toggle: () => {},
  dir: 'rtl',
});

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Language>('ar');

  useEffect(() => {
    const stored = localStorage.getItem('lang') as Language | null;
    if (stored === 'ar' || stored === 'en') setLang(stored);
  }, []);

  const toggle = () => {
    setLang(prev => {
      const next: Language = prev === 'ar' ? 'en' : 'ar';
      localStorage.setItem('lang', next);
      return next;
    });
  };

  return (
    <LanguageContext.Provider value={{ lang, toggle, dir: lang === 'ar' ? 'rtl' : 'ltr' }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
