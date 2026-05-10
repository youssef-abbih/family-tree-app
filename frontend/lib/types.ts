export type PersonType = 'prophet' | 'companion' | 'leader' | 'poet' | 'scholar';

export interface Person {
  id: string;
  name_ar: string;
  name_en: string;
  title: string | null;
  father_id: string | null;
  children_ids: string[];
  generation: number;
  type: PersonType;
  birth_year: number | null;
  death_year: number | null;
  description_ar: string | null;
  description_en: string | null;
  is_highlighted: boolean;
  highlight_reason: string | null;
}

export interface Stats {
  total: number;
  generations: number;
  by_type: Record<string, number>;
}

export interface LCAResult {
  lca_id: string | null;
  highlighted_ids: string[];
}

export type Language = 'ar' | 'en';
