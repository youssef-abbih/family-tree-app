import { Language } from './types';

const T: Record<string, Record<Language, string>> = {
  app_title:            { ar: 'شجرة النسب العربية',        en: 'Arab Genealogy Tree' },
  app_subtitle:         { ar: 'من إبراهيم الخليل إلى محمد ﷺ', en: 'From Ibrahim to Muhammad ﷺ' },
  view_tree:            { ar: 'استعرض الشجرة',             en: 'View the Tree' },
  stat_generations:     { ar: 'جيلاً',                     en: 'Generations' },
  stat_personalities:   { ar: 'شخصية',                    en: 'Personalities' },
  stat_prophets:        { ar: 'أنبياء',                    en: 'Prophets' },
  stat_companions:      { ar: 'صحابة وأمهات مؤمنين',      en: 'Companions & Wives' },
  about_title:          { ar: 'عن المشروع',                en: 'About This Project' },
  about_body:           { ar: 'تتتبع هذه الشجرة النسب العربي من إبراهيم الخليل عليه السلام مروراً بإسماعيل والعرب العدنانية حتى خاتم الأنبياء محمد ﷺ وصحابته الكرام.', en: 'This tree traces Arab lineage from Ibrahim (PBUH) through Ismail and the Adnanite Arabs to the Seal of the Prophets Muhammad ﷺ and his noble companions.' },
  // Tree page
  load_next:            { ar: 'تحميل الجيل التالي',        en: 'Load Next Generation' },
  generation:           { ar: 'الجيل',                     en: 'Generation' },
  no_more:              { ar: 'تم تحميل كامل الشجرة',      en: 'Full tree loaded' },
  // Legend
  legend_prophet:       { ar: 'نبي',                       en: 'Prophet' },
  legend_companion:     { ar: 'صحابي',                     en: 'Companion' },
  legend_leader:        { ar: 'قائد',                      en: 'Leader' },
  legend_poet:          { ar: 'شاعر',                      en: 'Poet' },
  legend_scholar:       { ar: 'عالم',                      en: 'Scholar' },
  // Ancestor comparison
  hint_select:          { ar: 'انقر على بطاقة لتتبع مسارها، أو اختر أكثر من شخص لإيجاد الجد المشترك', en: 'Click a card to trace its path, or select multiple cards to find their common ancestor' },
  selected_of:          { ar: 'محدد',                      en: 'selected' },
  clear_all:            { ar: 'مسح الكل',                  en: 'Clear All' },
  max_reached:          { ar: 'وصلت للحد الأقصى',          en: 'Maximum reached' },
  // Modal
  born:                 { ar: 'وُلد',                      en: 'Born' },
  died:                 { ar: 'تُوفّي',                    en: 'Died' },
  close:                { ar: 'إغلاق',                     en: 'Close' },
  generation_label:     { ar: 'الجيل',                     en: 'Generation' },
  add_favorite:         { ar: 'أضف للمفضلة',               en: 'Add to favourites' },
  remove_favorite:      { ar: 'إزالة من المفضلة',          en: 'Remove from favourites' },
  // Sidebar
  search_placeholder:   { ar: 'ابحث عن شخص...',            en: 'Search a person...' },
  filter_all:           { ar: 'الكل',                      en: 'All' },
  filter_prophets:      { ar: 'الأنبياء',                  en: 'Prophets' },
  filter_companions:    { ar: 'الصحابة',                   en: 'Companions' },
  filter_leaders:       { ar: 'القادة',                    en: 'Leaders' },
  no_results:           { ar: 'لا توجد نتائج',             en: 'No results' },
  language:             { ar: 'English',                   en: 'العربية' },
  dark_mode:            { ar: 'الوضع الداكن',              en: 'Dark mode' },
};

export function t(key: string, lang: Language): string {
  return T[key]?.[lang] ?? key;
}
