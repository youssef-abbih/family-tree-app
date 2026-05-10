from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE, STATS


# Each entry: (settings key, emoji, translation key)
_STAT_ITEMS = [
    ('generations',   '🕰️',  'stat_generations'),
    ('personalities', '👤',  'stat_personalities'),
    ('companions',    '⭐',  'stat_companions'),
    ('poets',         '📜',  'stat_poets'),
]


def create_stats(language: str = DEFAULT_LANGUAGE) -> None:
    """Four stat cards showing high-level project numbers."""
    direction = 'rtl' if language == 'ar' else 'ltr'

    with ui.element('section').classes(
        'w-full py-20 px-6 bg-white dark:bg-slate-800'
    ).props(f'dir="{direction}"'):

        with ui.element('div').classes(
            'grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto'
        ):
            for stat_key, icon, label_key in _STAT_ITEMS:
                count = STATS.get(stat_key, 0)
                label = get_text(label_key, language)

                with ui.card().classes(
                    'flex flex-col items-center justify-center p-8 '
                    'bg-amber-50 dark:bg-slate-700 rounded-2xl shadow-md '
                    'hover:shadow-xl hover:-translate-y-1 '
                    'transition-all duration-300 '
                    'border border-amber-200 dark:border-slate-600'
                ):
                    ui.label(icon).classes('text-5xl mb-4')
                    ui.label(str(count)).classes(
                        'text-4xl font-extrabold text-amber-600 dark:text-amber-400 mb-2'
                    )
                    ui.label(label).classes(
                        'text-amber-900 dark:text-amber-200 text-sm font-medium text-center'
                    )
