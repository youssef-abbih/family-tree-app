'use client';

import { Person } from '@/lib/types';
import { useLanguage } from '@/contexts/LanguageContext';
import { t } from '@/lib/translations';

const TYPE_CARD: Record<string, string> = {
  prophet:   'border-emerald-500 bg-emerald-50 dark:bg-emerald-950',
  companion: 'border-blue-500    bg-blue-50    dark:bg-blue-950',
  poet:      'border-amber-500   bg-amber-50   dark:bg-amber-950',
  leader:    'border-red-500     bg-red-50     dark:bg-red-950',
  scholar:   'border-purple-500  bg-purple-50  dark:bg-purple-950',
};

const TYPE_BADGE: Record<string, string> = {
  prophet:   'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
  companion: 'bg-blue-100    text-blue-800    dark:bg-blue-900    dark:text-blue-200',
  poet:      'bg-amber-100   text-amber-800   dark:bg-amber-900   dark:text-amber-200',
  leader:    'bg-red-100     text-red-800     dark:bg-red-900     dark:text-red-200',
  scholar:   'bg-purple-100  text-purple-800  dark:bg-purple-900  dark:text-purple-200',
};

interface Props {
  person: Person;
  isSelected?: boolean;
  isOnPath?: boolean;
  isAncestor?: boolean;
  isMaxReached?: boolean;
  isFavorite?: boolean;
  onClick?: (p: Person) => void;
  onInfoClick?: (p: Person) => void;
}

export default function PersonCard({
  person,
  isSelected = false,
  isOnPath = false,
  isAncestor = false,
  isMaxReached = false,
  isFavorite = false,
  onClick,
  onInfoClick,
}: Props) {
  const { lang, dir } = useLanguage();
  const name = lang === 'ar' ? person.name_ar : person.name_en;
  const typeKey = person.type ?? 'leader';
  const genLabel = lang === 'ar' ? `الجيل ${person.generation}` : `Gen ${person.generation}`;
  const typeLabel = t(`legend_${typeKey}`, lang);

  const cardBase = TYPE_CARD[typeKey] ?? 'border-gray-400 bg-gray-50 dark:bg-gray-900';
  const badgeBase = TYPE_BADGE[typeKey] ?? 'bg-gray-100 text-gray-800';

  const ring = isAncestor
    ? 'ring-4 ring-purple-500 ring-offset-2 scale-105'
    : isSelected
    ? 'ring-3 ring-purple-500 ring-offset-1'
    : isOnPath
    ? 'ring-2 ring-purple-300 ring-offset-1'
    : '';

  const dim = isMaxReached && !isSelected && !isAncestor ? 'opacity-40 cursor-not-allowed' : '';

  return (
    <div
      dir={dir}
      onClick={() => onClick?.(person)}
      className={`
        relative border-2 ${cardBase} ${ring} ${dim}
        rounded-xl p-3 cursor-pointer
        hover:shadow-xl hover:-translate-y-1
        transition-all duration-300
        min-w-[140px] max-w-[190px] w-full
        flex flex-col items-center text-center gap-1.5
      `}
    >
      {/* Info button */}
      {onInfoClick && (
        <button
          onClick={e => { e.stopPropagation(); onInfoClick(person); }}
          className={`absolute top-1 ${dir === 'rtl' ? 'left-1' : 'right-1'} text-gray-400 hover:text-purple-600 transition-colors`}
          aria-label="Info"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" strokeWidth="2"/>
            <path strokeLinecap="round" d="M12 16v-4M12 8h.01" strokeWidth="2"/>
          </svg>
        </button>
      )}

      {/* State indicator */}
      {isAncestor && <span className="text-base leading-none">👑</span>}
      {isSelected && !isAncestor && (
        <span className="text-xs font-bold text-purple-600 leading-none">✓</span>
      )}
      {isFavorite && <span className="text-xs leading-none">⭐</span>}

      {/* Name */}
      <span className="font-bold text-gray-900 dark:text-gray-100 text-sm leading-snug pt-1">
        {name}
      </span>

      {/* Title */}
      {person.title && (
        <span className="text-xs text-gray-500 dark:text-gray-400 leading-none">{person.title}</span>
      )}

      {/* Badge */}
      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${badgeBase}`}>
        {typeLabel}
      </span>

      {/* Generation */}
      <span className="text-xs text-gray-400 dark:text-gray-500">{genLabel}</span>
    </div>
  );
}
