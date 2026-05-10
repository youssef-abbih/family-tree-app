import type { Metadata } from 'next';
import './globals.css';
import { LanguageProvider } from '@/contexts/LanguageContext';
import Header from '@/components/Header';

export const metadata: Metadata = {
  title: 'شجرة النسب العربية | Arab Genealogy Tree',
  description: 'من إبراهيم الخليل إلى النبي محمد ﷺ | From Ibrahim to the Prophet Muhammad ﷺ',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar">
      <body className="min-h-screen bg-amber-50 dark:bg-slate-900 antialiased">
        <LanguageProvider>
          <Header />
          <main>{children}</main>
        </LanguageProvider>
      </body>
    </html>
  );
}
